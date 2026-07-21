import importlib

import tideway
from tideway.dismal import defaults
from tideway.appliance_cli import ApplianceCLI
from tideway.results import ReportResult, TextResult


class FakeStream:
    def __init__(self, text):
        self.text = text

    def readlines(self):
        return self.text.splitlines(True)


class FakeChannel:
    def __init__(self, exit_status):
        self.exit_status = exit_status

    def recv_exit_status(self):
        return self.exit_status


class FakeClient:
    def __init__(self):
        self.commands = []
        self.closed = False

    def exec_command(self, command):
        self.commands.append(command)
        if command == defaults.disk_alerts_cmd:
            return None, FakeStream("/,50%\n/usr,71%\n/data,90%\n"), FakeStream("")
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


def test_disk_info_uses_default_headers_when_command_has_no_header_row():
    class HeaderlessDiskClient(FakeClient):
        def exec_command(self, command):
            if command.startswith("df -h"):
                return None, FakeStream("/dev/sda1,/,10G,5G,5G,50%\n"), FakeStream("")
            return super().exec_command(command)

    result = ApplianceCLI("app.example", client=HeaderlessDiskClient()).disk_info()

    assert result.headers == ["fs", "mount", "size", "used", "available", "Used %"]
    assert result.rows == [["/dev/sda1", "/", "10G", "5G", "5G", "50%"]]


def test_run_command_raises_when_ssh_command_fails():
    class FailingClient(FakeClient):
        def exec_command(self, command):
            stdout = FakeStream("")
            stdout.channel = FakeChannel(1)
            return None, stdout, FakeStream("command failed\n")

    cli = ApplianceCLI("app.example", client=FailingClient())

    try:
        cli.run_command("failing-command")
    except RuntimeError as exc:
        assert str(exc) == "SSH command failed with exit status 1: command failed"
    else:
        raise AssertionError("A failed SSH command should raise RuntimeError")


def test_disk_usage_alerts_filters_by_threshold(tmp_path):
    client = FakeClient()
    cli = ApplianceCLI("app.example", client=client)

    result = cli.disk_usage_alerts(threshold=70)

    assert client.commands == [defaults.disk_alerts_cmd]
    assert isinstance(result, ReportResult)
    assert result.headers == ["mount", "Used %"]
    assert result.rows == [["/usr", "71%"], ["/data", "90%"]]
    assert result.files == []
    assert list(tmp_path.iterdir()) == []


def test_disk_usage_alerts_writes_when_requested(tmp_path):
    outfile = tmp_path / "disk_check.csv"
    cli = ApplianceCLI("app.example", client=FakeClient())

    result = cli.disk_usage_alerts(output_file=str(outfile))

    assert result.files == [str(outfile)]
    assert outfile.read_text().splitlines() == ["mount,Used %", "/usr,71%", "/data,90%"]


def test_text_command_writes_when_requested(tmp_path):
    outfile = tmp_path / "certs.txt"
    cli = ApplianceCLI("app.example", client=FakeClient())

    result = cli.certificates(output_file=str(outfile))

    assert isinstance(result, TextResult)
    assert result.files == [str(outfile)]
    assert outfile.read_text() == "ok\n"


def test_health_check_uses_default_system_user():
    client = FakeClient()
    cli = ApplianceCLI("app.example", client=client)

    result = cli.health_check()

    assert client.commands == [f"{defaults.health_check_cmd} -u system"]
    assert isinstance(result, TextResult)
    assert result.text == "ok\n"


def test_health_check_uses_configured_system_credentials():
    client = FakeClient()
    cli = ApplianceCLI(
        "app.example",
        system_username="admin",
        system_password="secret",
        client=client,
    )

    cli.health_check()

    assert client.commands == [f"{defaults.health_check_cmd} -u admin -p secret"]


def test_playback_data_runs_no_expiry_count():
    client = FakeClient()
    cli = ApplianceCLI("app.example", client=client)

    result = cli.playback_data()

    assert client.commands == [defaults.playback_data_cmd]
    assert isinstance(result, TextResult)
    assert result.text == "ok\n"


def test_service_checks_do_not_embed_ssh_password_in_commands():
    client = FakeClient()
    cli = ApplianceCLI("app.example", password="secret", client=client)

    cli.syslog()
    cli.vmware_tools()

    assert client.commands == [
        defaults.rsyslog_cmd,
        defaults.rsyslog_conf_cmd,
        defaults.vmware_tools_cmd,
    ]


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
