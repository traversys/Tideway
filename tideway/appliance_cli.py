import csv
import os
from typing import Optional

import paramiko

from .dismal import defaults
from .results import ReportResult, TextResult


def _read_secret(value: Optional[str], filename: Optional[str]) -> Optional[str]:
    if value is not None:
        return value
    if filename:
        with open(filename, encoding="utf-8") as handle:
            return handle.read().strip()
    return None


def _output_path(
    name: str,
    suffix: str,
    output_file: Optional[str],
    output_dir: Optional[str],
    filename: Optional[str],
) -> Optional[str]:
    if output_file:
        return output_file
    if output_dir:
        return os.path.join(output_dir, filename or f"{name}.{suffix}")
    return None


class ApplianceCLI:
    """SSH-backed BMC Discovery appliance commands."""

    def __init__(
        self,
        target,
        password=None,
        password_file=None,
        username="tideway",
        system_username=None,
        system_password=None,
        system_password_file=None,
        ssl_verify=False,
        client=None,
    ):
        self.target = target
        self.username = username
        self.password = _read_secret(password, password_file)
        self.system_username = system_username
        self.system_password = _read_secret(system_password, system_password_file)
        self.ssl_verify = ssl_verify
        self.client = client

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc, traceback):
        self.close()

    def connect(self):
        if self.client is not None:
            return self
        if not self.password:
            raise ValueError("An appliance SSH password or password_file is required.")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.target, username=self.username, password=self.password)
        self.client = client
        return self

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def run_command(self, command):
        self.connect()
        client = self.client
        if client is None:
            raise RuntimeError("SSH client is not connected.")
        _, stdout, stderr = client.exec_command(command)
        out = "".join(stdout.readlines())
        err = "".join(stderr.readlines())
        return out if out else err

    def _write_text(self, result, output_file=None, output_dir=None, filename=None):
        files = []
        path = _output_path(result.name, "txt", output_file, output_dir, filename)
        if path:
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(result.text)
            files.append(path)
        result.files = files
        return result

    def _write_report(self, result, output_file=None, output_dir=None, filename=None):
        files = []
        path = _output_path(result.name, "csv", output_file, output_dir, filename)
        if path:
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
            with open(path, "w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                if result.headers:
                    writer.writerow(result.headers)
                writer.writerows(result.rows)
            files.append(path)
        result.files = files
        return result

    @staticmethod
    def _colon_rows(text, headers):
        rows = []
        for line in text.replace("\r\n", "\n").splitlines():
            if not line:
                continue
            parts = [part.strip() for part in line.split(":")]
            rows.append(parts)
        return ReportResult(name="", headers=headers, rows=rows, raw=text)

    @staticmethod
    def _csv_text_rows(text):
        rows = list(csv.reader(text.replace("\r\n", "\n").splitlines()))
        headers = rows[0] if rows else []
        return headers, rows[1:]

    @staticmethod
    def _percent(value):
        try:
            return int(str(value).strip().rstrip("%"))
        except (TypeError, ValueError):
            return 0

    def certificates(self, output_file=None, output_dir=None):
        command = f"{defaults.tls_certificates_cmd} {self.target}:443"
        result = TextResult("certificates", self.run_command(command))
        return self._write_text(result, output_file, output_dir, defaults.tls_certificates_filename)

    def cli_users(self, output_file=None, output_dir=None):
        text = self.run_command(defaults.etc_passwd_cmd)
        result = self._colon_rows(text, defaults.etc_passwd_header)
        result.name = "cli_users"
        return self._write_report(result, output_file, output_dir, defaults.etc_passwd_filename)

    def disk_info(self, output_file=None, output_dir=None):
        text = self.run_command(defaults.df_h_cmd)
        headers, rows = self._csv_text_rows(text)
        result = ReportResult("disk_info", headers or defaults.df_h_header, rows, raw=text)
        return self._write_report(result, output_file, output_dir, defaults.disk_filename)

    def disk_usage_alerts(self, threshold=70, output_file=None, output_dir=None):
        text = self.run_command(defaults.disk_alerts_cmd)
        rows = []
        for row in csv.reader(text.replace("\r\n", "\n").splitlines()):
            if len(row) < 2:
                continue
            mount, used = [part.strip() for part in row[:2]]
            if self._percent(used) > int(threshold):
                rows.append([mount, used])
        result = ReportResult(
            "disk_usage_alerts",
            defaults.disk_alerts_header,
            rows,
            raw=text,
        )
        return self._write_report(result, output_file, output_dir, defaults.disk_alerts_filename)

    def clustering(self, output_file=None, output_dir=None):
        result = TextResult("clustering", self.run_command(defaults.cluster_cmd))
        return self._write_text(result, output_file, output_dir, defaults.cluster_filename)

    def cmdb_errors(self, output_file=None, output_dir=None):
        result = TextResult("cmdb_errors", self.run_command(defaults.cmdb_errors_cmd))
        return self._write_text(result, output_file, output_dir, defaults.cmdb_errors_filename)

    def core_dumps(self, output_file=None, output_dir=None):
        result = TextResult("core_dumps", self.run_command(defaults.core_dumps_cmd))
        return self._write_text(result, output_file, output_dir, defaults.core_dumps_filename)

    def dns_resolution(self, output_file=None, output_dir=None):
        result = TextResult("dns_resolution", self.run_command(defaults.resolv_conf_cmd))
        return self._write_text(result, output_file, output_dir, defaults.resolv_conf_filename)

    def ds_status(self, output_file=None, output_dir=None):
        text = self.run_command(defaults.ds_status_off_cmd)
        text += "\n" + self.run_command(defaults.ds_status_on_cmd)
        result = TextResult("ds_status", text)
        return self._write_text(result, output_file, output_dir, defaults.tw_ds_compact_filename)

    def host_info(self, output_file=None, output_dir=None):
        text = self.run_command(defaults.uname_cmd)
        text += "\n" + self.run_command(defaults.hostname_cmd)
        text += "\n" + self.run_command(defaults.ipaddr_cmd)
        result = TextResult("host_info", text)
        return self._write_text(result, output_file, output_dir, defaults.hostname_filename)

    def health_check(self, output_file=None, output_dir=None):
        system_username = self.system_username or "system"
        command = f"{defaults.health_check_cmd} -u {system_username}"
        if self.system_password:
            command = f"{command} -p {self.system_password}"
        result = TextResult("health_check", self.run_command(command))
        return self._write_text(result, output_file, output_dir, defaults.health_check_filename)

    def ldap(self, output_file=None, output_dir=None):
        result = TextResult("ldap", self.run_command(defaults.ldap_cmd))
        return self._write_text(result, output_file, output_dir, defaults.ldap_filename)

    def ntp(self, output_file=None, output_dir=None):
        text = self.run_command(defaults.ntp_cmd)
        text += "\n" + self.run_command(defaults.tz_cmd)
        result = TextResult("ntp", text)
        return self._write_text(result, output_file, output_dir, defaults.ntp_filename)

    def playback_data(self, output_file=None, output_dir=None):
        text = self.run_command(defaults.playback_data_cmd)
        result = TextResult("playback_data", text)
        return self._write_text(result, output_file, output_dir, defaults.playback_data_filename)

    def tw_config_dump(self, output_file=None, output_dir=None):
        result = TextResult("tw_config_dump", self.run_command(defaults.tw_config_dump_cmd))
        return self._write_text(result, output_file, output_dir, defaults.config_dump_filename)

    def tw_crontab(self, output_file=None, output_dir=None):
        result = TextResult("tw_crontab", self.run_command(defaults.tw_crontab_cmd))
        return self._write_text(result, output_file, output_dir, defaults.crontab_filename)

    def tw_options(self, output_file=None, output_dir=None):
        if not self.system_username or not self.system_password:
            raise ValueError("system_username and system_password are required for tw_options.")
        command = f"{defaults.tw_options_cmd} -u {self.system_username} -p {self.system_password}"
        result = TextResult("tw_options", self.run_command(command))
        return self._write_text(result, output_file, output_dir, defaults.tw_options_filename)

    def syslog(self, output_file=None, output_dir=None):
        command = defaults.rsyslog_cmd
        if self.password:
            command = f"{defaults.rsyslog_cmd} || echo {self.password} | sudo -S /sbin/service rsyslog status"
        text = self.run_command(command)
        text += "\n" + self.run_command(defaults.rsyslog_conf_cmd)
        result = TextResult("syslog", text)
        return self._write_text(result, output_file, output_dir, defaults.syslog_filename)

    def baseline(self, output_file=None, output_dir=None):
        text = self.run_command(defaults.baseline_cmd)
        result = TextResult("baseline", text)
        return self._write_text(result, output_file, output_dir, defaults.baseline_filename)

    def vmware_tools(self, output_file=None, output_dir=None):
        command = defaults.vmware_tools_cmd
        if self.password:
            command = f"{defaults.vmware_tools_cmd} || echo {self.password} | sudo -S /sbin/service vmware-tools status"
        result = TextResult("vmware_tools", self.run_command(command))
        return self._write_text(result, output_file, output_dir, defaults.vmware_tools_filename)

    def clear_queue(self, confirm=False):
        if not confirm:
            raise ValueError("clear_queue is destructive; call clear_queue(confirm=True).")
        outputs = [
            self.run_command("tw_service_control --stop"),
            self.run_command("rm -rfv /usr/tideway/var/persist/reasoning/engine/queue/*.pq"),
            self.run_command("rm -rfv /usr/tideway/var/persist/reasoning/engine/queue/*.rc"),
            self.run_command("tw_service_control --start"),
        ]
        return TextResult("clear_queue", "\n".join(outputs))


def appliance_cli(
    target,
    password=None,
    password_file=None,
    username="tideway",
    system_username=None,
    system_password=None,
    system_password_file=None,
    ssl_verify=False,
):
    return ApplianceCLI(
        target,
        password=password,
        password_file=password_file,
        username=username,
        system_username=system_username,
        system_password=system_password,
        system_password_file=system_password_file,
        ssl_verify=ssl_verify,
    )
