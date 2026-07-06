import csv
import os
import shutil
import tempfile
from types import SimpleNamespace

from .results import BatchReportResult, ReportResult, TextResult
from .dismal import api as dismal_api
from .dismal import builder, cache, defaults, output, reporting


_DEFAULT_REPORTS = [
    "devices",
    "device_ids",
    "suggested_cred_opt",
    "credential_success",
    "schedules",
    "excludes",
    "ip_analysis",
    "discovery_run_analysis",
    "active_scans",
    "sensitive_data",
    "eca_errors",
    "open_ports",
    "host_utilisation",
    "orphan_vms",
    "missing_vms",
    "near_removal",
    "removed",
    "os_lifecycle",
    "software_lifecycle",
    "db_lifecycle",
    "unrecognised_snmp",
    "capture_candidates",
    "installed_agents",
    "expected_agents",
    "si_user_accounts",
    "pattern_modules",
    "outpost_creds",
    "tku",
    "vault",
    "hostname",
]


_REPORT_FILES = {
    "active_scans": defaults.active_scans_filename,
    "api_version": defaults.api_filename,
    "audit": defaults.audit_filename,
    "baseline": defaults.baseline_filename,
    "capture_candidates": defaults.capture_candidates_filename,
    "cmdbsync": defaults.cmdbsync_filename,
    "credential_success": "credential_success.csv",
    "db_lifecycle": defaults.db_lifecycle_filename,
    "device_ids": "device_ids.csv",
    "devices": "devices.csv",
    "discovery_analysis": "discovery_analysis.csv",
    "discovery_run_analysis": "discovery_run_analysis.csv",
    "eca_errors": defaults.eca_errors_filename,
    "excludes": defaults.exclude_ranges_filename,
    "expected_agents": "expected_agents.csv",
    "host_utilisation": defaults.host_util_filename,
    "hostname": "hostname.txt",
    "installed_agents": defaults.installed_agents_filename,
    "ip_analysis": "ip_analysis.csv",
    "ipaddr": "ipaddr.txt",
    "knowledge": defaults.tw_knowledge_filename,
    "licensing": defaults.tw_license_zip_filename,
    "missing_vms": defaults.missing_vms_filename,
    "near_removal": defaults.near_removal_filename,
    "open_ports": defaults.open_ports_filename,
    "orphan_vms": defaults.orphan_vms_filename,
    "os_lifecycle": defaults.os_lifecycle_filename,
    "outpost_creds": defaults.outpost_creds_filename,
    "pattern_modules": defaults.tku_filename,
    "removed": defaults.removed_filename,
    "schedules": "schedules.csv",
    "sensitive_data": defaults.sensitive_data_filename,
    "si_user_accounts": defaults.si_user_accounts_filename,
    "software_lifecycle": defaults.si_lifecycle_filename,
    "suggested_cred_opt": "suggested_cred_opt.csv",
    "tku": defaults.tku_filename,
    "unrecognised_snmp": defaults.snmp_unrecognised_filename,
    "vault": defaults.vault_filename,
}


_QUERY_REPORTS = {
    "api_version": (dismal_api.admin, defaults.api_filename),
    "audit": (dismal_api.audit, defaults.audit_filename),
    "baseline": (dismal_api.baseline, defaults.baseline_filename),
    "cmdbsync": (dismal_api.cmdb_config, defaults.cmdbsync_filename),
    "knowledge": (dismal_api.modules, defaults.tw_knowledge_filename),
    "licensing": (dismal_api.licensing, defaults.tw_license_zip_filename),
}


class _AdminCompat:
    def __init__(self, appliance):
        self.admin_endpoint = appliance.admin()

    def admin(self):
        return self.admin_endpoint.get_admin_about()

    def baseline(self):
        return self.admin_endpoint.get_admin_baseline()

    def licensing(self, content_type="text/plain"):
        return self.admin_endpoint.get_admin_licensing(content_type)


class Reports:
    """Dismal-style reports exposed as Tideway library calls."""

    def __init__(self, appliance):
        self.appliance = appliance
        self.discovery = appliance.discovery()
        self.search = appliance.data()
        self.credentials = appliance.credentials()
        self.vault_endpoint = appliance.vault()
        self.knowledge = appliance.knowledge()
        self.admin_endpoint = _AdminCompat(appliance)

    def _options(self, reporting_dir, report_name=None, **options):
        cache.configure(options.get("cache_dir"), enabled=not options.get("no_cache", False))
        excavate = [report_name] if report_name else None
        if report_name == "ipaddr" and options.get("ip_address"):
            excavate = [report_name, options.get("ip_address")]
        return SimpleNamespace(
            target=self.appliance.target,
            token=self.appliance.token,
            username=options.get("username"),
            password=options.get("password"),
            f_passwd=options.get("password_file"),
            output_csv=False,
            output_file=None,
            output_null=False,
            output_cli=False,
            output_path=None,
            reporting_dir=reporting_dir,
            excavate=excavate,
            preserve_existing=options.get("preserve_existing", False),
            include_endpoints=options.get("include_endpoints"),
            endpoint_prefix=options.get("endpoint_prefix"),
            max_identities=options.get("max_identities"),
            max_threads=options.get("max_threads", 2),
            resolve_hostnames=options.get("resolve_hostnames", False),
            use_export=options.get("use_export", False),
            debugging=options.get("debug", False),
            schedule_timezone=options.get("schedule_timezone"),
            reset_schedule_timezone=options.get("reset_schedule_timezone", False),
            a_query=options.get("query"),
            a_kill_run=options.get("run_id"),
            a_enable=options.get("credential_id"),
            a_removal=options.get("credential_id"),
            weigh=options.get("apply", False),
        )

    def _materialize(self, name, work_dir, output_file=None, output_dir=None, preserve_existing=False):
        expected = _REPORT_FILES.get(name)
        candidates = []
        if expected:
            candidates.append(os.path.join(work_dir, expected))
        for root, _, files in os.walk(work_dir):
            for filename in files:
                path = os.path.join(root, filename)
                if path not in candidates:
                    candidates.append(path)

        if not candidates:
            return ReportResult(name=name)

        files = []
        primary = candidates[0]
        destinations = []
        if output_file:
            destinations = [(primary, output_file)]
        elif output_dir:
            os.makedirs(output_dir, exist_ok=True)
            for path in candidates:
                destinations.append((path, os.path.join(output_dir, os.path.basename(path))))

        for src, dest in destinations:
            if preserve_existing and os.path.exists(dest):
                files.append(dest)
                continue
            os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
            shutil.copyfile(src, dest)
            files.append(dest)

        return self._read_result(name, primary, files)

    @staticmethod
    def _read_result(name, path, files):
        if path.lower().endswith(".csv"):
            with open(path, newline="", encoding="utf-8") as handle:
                rows = list(csv.reader(handle))
            headers = rows[0] if rows else []
            return ReportResult(name=name, headers=headers, rows=rows[1:], files=files)
        try:
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
        except UnicodeDecodeError:
            with open(path, "rb") as handle:
                raw = handle.read()
            return ReportResult(name=name, raw=raw, files=files)
        return TextResult(name=name, text=text, files=files)

    def _run_single(self, name, output_file=None, output_dir=None, preserve_existing=False, **options):
        if output_file and output_dir:
            raise ValueError("Use output_file or output_dir, not both.")
        if name == "export_tpl" and output_file:
            raise ValueError("export_tpl creates multiple files; use output_dir.")

        with tempfile.TemporaryDirectory(prefix="tideway-report-") as work_dir:
            args = self._options(work_dir, name, preserve_existing=preserve_existing, **options)
            self._dispatch(name, args, work_dir)
            return self._materialize(
                name,
                work_dir,
                output_file=output_file,
                output_dir=output_dir,
                preserve_existing=preserve_existing,
            )

    def _dispatch(self, name, args, work_dir):
        if name in _QUERY_REPORTS:
            func, _ = _QUERY_REPORTS[name]
            if name in {"api_version", "baseline", "licensing"}:
                func(self.admin_endpoint, args, work_dir)
            else:
                func(self.search, args, work_dir)
            return

        dispatch = {
            "active_scans": lambda: dismal_api.discovery_runs(self.discovery, args, work_dir),
            "capture_candidates": lambda: dismal_api.capture_candidates(self.search, args, work_dir),
            "credential_success": lambda: dismal_api.success(self.credentials, self.search, args, work_dir),
            "db_lifecycle": lambda: dismal_api.dblc(self.search, args, work_dir),
            "devices": lambda: reporting.devices(self.search, self.credentials, args),
            "discovery_analysis": lambda: reporting.discovery_analysis(self.search, self.credentials, args),
            "discovery_run_analysis": lambda: reporting.discovery_run_analysis(self.search, self.credentials, args),
            "eca_errors": lambda: dismal_api.eca_errors(self.search, args, work_dir),
            "excludes": lambda: dismal_api.excludes(self.search, args, work_dir),
            "expected_agents": lambda: dismal_api.expected_agents(self.search, args, work_dir),
            "export_tpl": lambda: dismal_api.tpl_export(self.search, args, work_dir),
            "host_utilisation": lambda: dismal_api.host_util(self.search, args, work_dir),
            "hostname": lambda: dismal_api.hostname(args, work_dir),
            "installed_agents": lambda: dismal_api.agents(self.search, args, work_dir),
            "ip_analysis": lambda: builder.ip_analysis(self.search, args),
            "ipaddr": lambda: reporting.ipaddr(self.search, self.credentials, args),
            "missing_vms": lambda: dismal_api.missing_vms(self.search, args, work_dir),
            "near_removal": lambda: dismal_api.near_removal(self.search, args, work_dir),
            "open_ports": lambda: dismal_api.open_ports(self.search, args, work_dir),
            "orphan_vms": lambda: dismal_api.orphan_vms(self.search, args, work_dir),
            "os_lifecycle": lambda: dismal_api.oslc(self.search, args, work_dir),
            "outpost_creds": lambda: dismal_api.outpost_creds(self.credentials, self.search, args, work_dir),
            "pattern_modules": lambda: dismal_api.tku(self.knowledge, args, work_dir),
            "removed": lambda: dismal_api.removed(self.search, args, work_dir),
            "schedules": lambda: builder.scheduling(self.credentials, self.search, args),
            "sensitive_data": lambda: dismal_api.sensitive(self.search, args, work_dir),
            "si_user_accounts": lambda: dismal_api.software_users(self.search, args, work_dir),
            "software_lifecycle": lambda: dismal_api.slc(self.search, args, work_dir),
            "suggested_cred_opt": lambda: builder.ordering(self.credentials, self.search, args, False),
            "tku": lambda: dismal_api.tku(self.knowledge, args, work_dir),
            "unrecognised_snmp": lambda: dismal_api.snmp(self.search, args, work_dir),
            "vault": lambda: dismal_api.vault(self.vault_endpoint, args, work_dir),
        }
        if name == "device_ids":
            identities = builder.unique_identities(
                self.search,
                args.include_endpoints,
                args.endpoint_prefix,
                args.max_identities,
            )
            rows = [
                [
                    identity["originating_endpoint"],
                    identity["list_of_ips"],
                    identity["list_of_names"],
                ]
                for identity in identities
            ]
            output.report(
                rows,
                ["Origating Endpoint", "List of IPs", "List of Names"],
                args,
                name="device_ids",
            )
            return
        try:
            dispatch[name]()
        except KeyError:
            raise ValueError(f"Unknown Tideway report: {name}") from None

    def run(self, names=None, output_dir=None, preserve_existing=False, queries=False, **options):
        if queries:
            if not output_dir:
                raise ValueError("queries=True writes multiple raw query files; use output_dir.")
            with tempfile.TemporaryDirectory(prefix="tideway-queries-") as work_dir:
                args = self._options(work_dir, "queries", preserve_existing=preserve_existing, **options)
                args.queries = True
                dismal_api.run_queries(self.search, args, work_dir)
                results = []
                files = []
                for root, _, filenames in os.walk(work_dir):
                    for filename in filenames:
                        src = os.path.join(root, filename)
                        dest = os.path.join(output_dir, filename)
                        if preserve_existing and os.path.exists(dest):
                            files.append(dest)
                        else:
                            os.makedirs(output_dir, exist_ok=True)
                            shutil.copyfile(src, dest)
                            files.append(dest)
                        results.append(self._read_result(filename, src, [dest]))
                return BatchReportResult(results=results, files=files)

        report_names = _DEFAULT_REPORTS if names is None or names == ["default"] else names
        if isinstance(report_names, str):
            report_names = [report_names]
        results = []
        files = []
        for name in report_names:
            result = self._run_single(
                name,
                output_dir=output_dir,
                preserve_existing=preserve_existing,
                queries=queries,
                **options,
            )
            results.append(result)
            files.extend(getattr(result, "files", []))
        return BatchReportResult(results=results, files=files)

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)

        def report_method(output_file=None, output_dir=None, preserve_existing=False, **options):
            return self._run_single(
                name,
                output_file=output_file,
                output_dir=output_dir,
                preserve_existing=preserve_existing,
                **options,
            )

        return report_method
