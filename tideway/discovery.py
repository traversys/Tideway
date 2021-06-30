# -*- coding: utf-8 -*-

import requests
import tideway

dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Discovery(appliance):
    '''Control scanning and view results.'''

    def getDiscoveryStatus(self):
        '''Get the current status of the discovery process.'''
        response = dr.discoRequest(self, "/discovery")
        return response

    def setDiscoveryStatus(self, body):
        '''
            Either start or stop the discovery process. Note this call can
            return before the desired state has been reached.
        '''
        response = dr.discoPatch(self, "/discovery", body)
        return response

    def getApiProviderMetadata(self):
        '''
            Get metadata for the API providers currently supported by BMC
            Discovery. This can be used as a reference when interacting with the
            /discovery/runs and /vault/credentials endpoints. Support for new
            API providers is available in TKU knowledge updates.
        '''
        response = dr.discoRequest(self, "/discovery/api_provider_metadata")
        return response

    def getDiscoveryCloudMetaData(self):
        '''
            Get metadata for the cloud providers currently supported by BMC
            Discovery.
        '''
        response = dr.discoRequest(self, "/discovery/cloud_metadata")
        return response

    def getDiscoveryRuns(self):
        '''Get details of all currently processing discovery runs.'''
        response = dr.discoRequest(self, "/discovery/runs")
        return response

    def getDiscoveryRun(self, runid):
        '''Get details of specific currently processing discovery run.'''
        response = dr.discoRequest(self, "/discovery/runs/{}".format(runid))
        return response

    def discoveryRun(self, body):
        '''Create a new snapshot discovery run.'''
        response = dr.discoPost(self, "/discovery/runs", body)
        return response

    def updateDiscoveryRun(self, runid, body):
        '''Update the state of a specific discovery run.'''
        response = dr.discoPatch(self, "/discovery/runs/{}".format(runid), body)
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
