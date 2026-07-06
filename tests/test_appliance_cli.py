import importlib

import tideway
from tideway.appliance_cli import ApplianceCLI
from tideway.results import ReportResult, TextResult


class FakeStream:
    def __init__(self, text):
        self.text = text

    def readlines(self):
        return self.text.splitlines(True)


class FakeClient:
    def __init__(self):
        self.commands = []
        self.closed = False

    def exec_command(self, command):
        self.commands.append(command)
        if command.startswith("df -h"):
            return None, FakeStream("fs,mount,size,used,available,Used %\n/dev/sda1,/,10G,5G,5G,50%\n"), FakeStream("")
        return None, FakeStream("ok\n"), FakeStream("")

    def close(self):
        self.closed = True


def test_appliance_cli_uses_tideway_user_by_default(monkeypatch):
    calls = {}

    class FakeSSHClient(FakeClient):
        def set_missing_host_key_policy(self, policy):
            calls["policy"] = policy

        def connect(self, target, username=None, password=None):
            calls["target"] = target
            calls["username"] = username
            calls["password"] = password

    cli_module = importlib.import_module("tideway.appliance_cli")
    monkeypatch.setattr(cli_module.paramiko, "SSHClient", FakeSSHClient)
    monkeypatch.setattr(cli_module.paramiko, "AutoAddPolicy", lambda: "policy")

    cli = tideway.appliance_cli("app.example", password="secret").connect()

    assert calls == {
        "policy": "policy",
        "target": "app.example",
        "username": "tideway",
        "password": "secret",
    }
    cli.close()


def test_disk_info_returns_report_without_writing(tmp_path):
    cli = ApplianceCLI("app.example", client=FakeClient())

    result = cli.disk_info()

    assert isinstance(result, ReportResult)
    assert result.headers == ["fs", "mount", "size", "used", "available", "Used %"]
    assert result.rows == [["/dev/sda1", "/", "10G", "5G", "5G", "50%"]]
    assert result.files == []
    assert list(tmp_path.iterdir()) == []


def test_text_command_writes_when_requested(tmp_path):
    outfile = tmp_path / "certs.txt"
    cli = ApplianceCLI("app.example", client=FakeClient())

    result = cli.certificates(output_file=str(outfile))

    assert isinstance(result, TextResult)
    assert result.files == [str(outfile)]
    assert outfile.read_text() == "ok\n"


def test_context_manager_closes_client():
    client = FakeClient()

    with ApplianceCLI("app.example", client=client) as cli:
        assert cli.client is client

    assert client.closed is True


def test_clear_queue_requires_confirmation():
    cli = ApplianceCLI("app.example", client=FakeClient())

    try:
        cli.clear_queue()
    except ValueError as exc:
        assert "confirm=True" in str(exc)
    else:
        raise AssertionError("clear_queue should require confirmation")
