from types import SimpleNamespace

from .dismal import api as dismal_api
from .dismal import builder, taxonomy_browser


class ReportAdmin:
    """Administrative helpers imported from Dismal workflows."""

    def __init__(self, appliance):
        self.appliance = appliance
        self.discovery = appliance.discovery()
        self.search = appliance.data()
        self.credentials = appliance.credentials()

    def query(self, query, limit=500):
        return self.search.search_bulk(query, limit=limit)

    def enable_credential(self, credential_id):
        return dismal_api.update_cred(self.credentials, credential_id)

    def delete_credential(self, credential_id):
        return dismal_api.remove_cred(self.credentials, credential_id)

    def credential_ordering(self, apply=False, output_file=None):
        args = SimpleNamespace(
            target=self.appliance.target,
            output_file=output_file,
            output_csv=False,
            output_null=False,
            output_cli=False,
            excavate=["suggested_cred_opt"],
            reporting_dir=None,
            preserve_existing=False,
        )
        return builder.ordering(self.credentials, self.search, args, apply)

    def kill_run(self, run_id):
        args = SimpleNamespace(a_kill_run=run_id)
        return dismal_api.cancel_run(self.discovery, args)

    def update_schedule_timezone(self, timezone, reset=False):
        args = SimpleNamespace(schedule_timezone=timezone, reset_schedule_timezone=reset)
        return dismal_api.update_schedule_timezone(self.discovery, args)

    def taxonomy_cache(self, cache_path, refresh=False):
        return taxonomy_browser.ensure_taxonomy_cache(self.appliance, cache_path, refresh=refresh)

    def taxonomy_crawl(self, cache_path, refresh=False):
        return taxonomy_browser.crawl_all(self.appliance, cache_path, refresh=refresh)

    def taxonomy(self, node, mode="attributes", related=None, role=None, cache_path=None, refresh=False):
        args = SimpleNamespace(
            taxonomy=node,
            taxonomy_mode=mode,
            taxonomy_related=related,
            taxonomy_role=role,
            taxonomy_cache=cache_path,
            taxonomy_refresh=refresh,
        )
        return taxonomy_browser.run(self.appliance, args, None)
