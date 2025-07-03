# -*- coding: utf-8 -*-

import tideway

dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Discovery(appliance):
    '''Control scanning and view results.'''

    def getDiscoveryStatus(self):
        '''Get the current status of the discovery process. JSON Output.'''
        response = dr.discoRequest(self, "/discovery")
        return response
    get_discovery = property(getDiscoveryStatus)

    def patch_discovery(self, body):
        '''Alternate API call for PATCH /discovery.'''
        response = dr.discoPatch(self, "/discovery", body)
        return response

    def setDiscoveryStatus(self, body):
        '''
            Set the Discovery status using JSON format.
        '''
        response = dr.discoPatch(self, "/discovery", body)
        return response.ok

    def getApiProviderMetadata(self):
        '''
            Get metadata for the API providers currently supported by BMC
            Discovery. This can be used as a reference when interacting with the
            /discovery/runs and /vault/credentials endpoints. Support for new
            API providers is available in TKU knowledge updates.
        '''
        response = dr.discoRequest(self, "/discovery/api_provider_metadata")
        return response
    get_discovery_api_provider_metadata = property(getApiProviderMetadata)

    def getDiscoveryCloudMetaData(self):
        '''
            Get metadata for the cloud providers currently supported by BMC
            Discovery.
        '''
        response = dr.discoRequest(self, "/discovery/cloud_metadata")
        return response
    get_discovery_api_cloud_metadata = property(getDiscoveryCloudMetaData)

    def get_discovery_exclude(self, exclude_id=None):
        '''Get a list of all excludes or specific.'''
        if exclude_id:
            req = dr.discoRequest(self, "/discovery/excludes/{}".format(exclude_id))
        else:
            req = dr.discoRequest(self, "/discovery/excludes")
        return req
    get_discovery_excludes = property(get_discovery_exclude)

    def post_discovery_exclude(self, body):
        '''Create an exclude.'''
        response = dr.discoPost(self, "/discovery/excludes", body)
        return response

    def delete_discovery_exclude(self, exclude_id):
        '''Delete an exclude.'''
        response = dr.discoDelete(self, "/discovery/excludes/{}".format(exclude_id))
        return response

    def patch_discovery_exclude(self, exclude_id, body):
        '''Update an exclude.'''
        response = dr.discoPatch(self, "/discovery/excludes/{}".format(exclude_id), body)
        return response

    def get_discovery_run(self, run_id=None):
        '''Get details of all or specific currently processing discovery runs.'''
        if run_id:
            req = dr.discoRequest(self, "/discovery/runs/{}".format(run_id))
        else:
            req = dr.discoRequest(self, "/discovery/runs")
        return req
    get_discovery_runs = property(get_discovery_run)

    def getDiscoveryRuns(self):
        '''Get details of all currently processing discovery runs.'''
        response = dr.discoRequest(self, "/discovery/runs")
        return response

    def getDiscoveryRun(self, runid):
        '''Get details of specific currently processing discovery run.'''
        response = dr.discoRequest(self, "/discovery/runs/{}".format(runid))
        return response

    def post_discovery_run(self, body):
        '''Alternative API call for POST /discovery/runs.'''
        response = dr.discoPost(self, "/discovery/runs", body)
        return response

    def discoveryRun(self, body):
        '''Create a new snapshot discovery run.'''
        response = dr.discoPost(self, "/discovery/runs", body)
        return response

    def patch_discovery_run(self, run_id, body):
        '''Alternate API call for PATCH /discovery/runs.'''
        response = dr.discoPatch(self, "/discovery/runs/{}".format(run_id), body)
        return response

    def updateDiscoveryRun(self, runid, body):
        '''Update the state of a specific discovery run.'''
        response = dr.discoPatch(self, "/discovery/runs/{}".format(runid), body)
        return response

    def get_discovery_run_results(self, run_id, result=None, offset=None, results_id=None, format=None, limit = 100, delete = False):
        '''Get a summary of the results from scanning all endpoints in the run that had a specific type of result.'''
        if result:
            self.params['offset'] = offset
            self.params['results_id'] = results_id
            self.params['format'] = format
            self.params['limit'] = limit
            self.params['delete'] = delete
            response = dr.discoRequest(self, "/discovery/runs/{}/results/{}".format(run_id,result))
        else:
            response = dr.discoRequest(self, "/discovery/runs/{}/results".format(run_id))
        return response

    def getDiscoveryRunResults(self, runid):
        '''Get a summary of the results from scanning all endpoints in the run, partitioned by result type.'''
        response = dr.discoRequest(self, "/discovery/runs/{}/results".format(runid))
        return response

    def getDiscoveryRunResult(self, runid, result="Success", offset=None, results_id=None, format=None, limit = 100, delete = False):
        '''Get a summary of the results from scanning all endpoints in the run that had a specific type of result.'''
        self.params['offset'] = offset
        self.params['results_id'] = results_id
        self.params['format'] = format
        self.params['limit'] = limit
        self.params['delete'] = delete
        response = dr.discoRequest(self, "/discovery/runs/{}/results/{}".format(runid,result))
        return response

    def get_discovery_run_inferred(self, run_id, inferred_kind, offset=None, results_id=None, format=None, limit = 100, delete = False):
        '''Get a summary of the devices inferred by a discovery run which have a specific inferred kind.'''
        if inferred_kind:
            self.params['offset'] = offset
            self.params['results_id'] = results_id
            self.params['format'] = format
            self.params['limit'] = limit
            self.params['delete'] = delete
            response = dr.discoRequest(self, "/discovery/runs/{}/inferred/{}".format(run_id,inferred_kind))
        else:
            response = dr.discoRequest(self, "/discovery/runs/{}/inferred".format(run_id))
        return response

    def getDiscoveryRunInferred(self, runid):
        '''Get a summary of all inferred devices from a discovery run, partitioned by device type.'''
        response = dr.discoRequest(self, "/discovery/runs/{}/inferred".format(runid))
        return response

    def getDiscoveryRunInferredKind(self, runid, inferred_kind, offset=None, results_id=None, format=None, limit = 100, delete = False):
        '''Get a summary of the devices inferred by a discovery run which have a specific inferred kind.'''
        self.params['offset'] = offset
        self.params['results_id'] = results_id
        self.params['format'] = format
        self.params['limit'] = limit
        self.params['delete'] = delete
        response = dr.discoRequest(self, "/discovery/runs/{}/inferred/{}".format(runid,inferred_kind))
        return response

    def get_discovery_run_schedule(self, run_id=None):
        '''Get a list of all scheduled runs or specific.'''
        if run_id:
            req = dr.discoRequest(self, "/discovery/runs/scheduled/{}".format(run_id))
        else:
            req = dr.discoRequest(self, "/discovery/runs/scheduled")
        return req
    get_discovery_run_schedules = property(get_discovery_run_schedule)

    def post_discovery_run_schedule(self, body):
        '''Add a new scheduled run.'''
        response = dr.discoPost(self, "/discovery/runs/scheduled", body)
        return response

    def delete_discovery_run_schedule(self, run_id):
        '''Delete a specific scheduled discovery run.'''
        response = dr.discoDelete(self, "/discovery/runs/scheduled/{}".format(run_id))
        return response

    def patch_discovery_run_schedule(self, run_id, body):
        '''Update the parameters of a specific scheduled discovery run.'''
        response = dr.discoPatch(self, "/discovery/runs/scheduled/{}".format(run_id), body)
        return response

    def get_discovery_outpost(self, outpost_id=None):
        '''Get all configured Outposts or a specific one.'''
        if outpost_id:
            req = dr.discoRequest(self, "/discovery/outposts/{}".format(outpost_id))
        else:
            req = dr.discoRequest(self, "/discovery/outposts")
        return req
    get_discovery_outposts = property(get_discovery_outpost)

    def post_discovery_outpost(self, body):
        '''Register a new Outpost.'''
        response = dr.discoPost(self, "/discovery/outposts", body)
        return response

    def delete_discovery_outpost(self, outpost_id):
        '''Delete an Outpost.'''
        response = dr.discoDelete(self, "/discovery/outposts/{}".format(outpost_id))
        return response
