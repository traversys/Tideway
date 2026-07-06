import csv
import os

import tideway
from tideway.reports import Reports
from tideway.results import BatchReportResult, ReportResult


def test_report_returns_result_without_writing(monkeypatch, tmp_path):
    def fake_dispatch(self, name, args, work_dir):
        with open(os.path.join(work_dir, "credential_success.csv"), "w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["Credential", "Count"])
            writer.writerow(["cred1", "2"])

    monkeypatch.setattr(Reports, "_dispatch", fake_dispatch)
    tw = tideway.appliance("host", "token")

    result = tw.reports().credential_success()

    assert isinstance(result, ReportResult)
    assert result.headers == ["Credential", "Count"]
    assert result.rows == [["cred1", "2"]]
    assert result.files == []
    assert list(tmp_path.iterdir()) == []


def test_report_output_file_writes_exact_path(monkeypatch, tmp_path):
    def fake_dispatch(self, name, args, work_dir):
        with open(os.path.join(work_dir, "credential_success.csv"), "w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["Credential", "Count"])
            writer.writerow(["cred1", "2"])

    monkeypatch.setattr(Reports, "_dispatch", fake_dispatch)
    outfile = tmp_path / "custom.csv"
    tw = tideway.appliance("host", "token")

    result = tw.reports().credential_success(output_file=str(outfile))

    assert result.files == [str(outfile)]
    with open(outfile, newline="") as handle:
        assert list(csv.reader(handle)) == [["Credential", "Count"], ["cred1", "2"]]


def test_report_output_dir_uses_canonical_name(monkeypatch, tmp_path):
    def fake_dispatch(self, name, args, work_dir):
        with open(os.path.join(work_dir, "devices.csv"), "w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["Name"])
            writer.writerow(["host1"])

    monkeypatch.setattr(Reports, "_dispatch", fake_dispatch)
    tw = tideway.appliance("host", "token")

    result = tw.reports().devices(output_dir=str(tmp_path))

    assert result.files == [str(tmp_path / "devices.csv")]
    assert (tmp_path / "devices.csv").exists()


def test_report_preserve_existing_skips_write(monkeypatch, tmp_path):
    def fake_dispatch(self, name, args, work_dir):
        with open(os.path.join(work_dir, "devices.csv"), "w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["Name"])
            writer.writerow(["new"])

    monkeypatch.setattr(Reports, "_dispatch", fake_dispatch)
    existing = tmp_path / "devices.csv"
    existing.write_text("Name\nold\n")
    tw = tideway.appliance("host", "token")

    result = tw.reports().devices(output_dir=str(tmp_path), preserve_existing=True)

    assert result.files == [str(existing)]
    assert existing.read_text() == "Name\nold\n"


def test_run_returns_batch(monkeypatch):
    def fake_run_single(self, name, **kwargs):
        return ReportResult(name, ["A"], [[name]])

    monkeypatch.setattr(Reports, "_run_single", fake_run_single)
    tw = tideway.appliance("host", "token")

    result = tw.reports().run(names=["devices", "credential_success"])

    assert isinstance(result, BatchReportResult)
    assert [item.name for item in result.results] == ["devices", "credential_success"]
