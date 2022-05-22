# -*- coding: utf-8 -*-

import tideway

dr = tideway.discoRequests
appliance = tideway.main.Appliance

class Taxonomy(appliance):
    '''Retrieve taxonomy data.'''

    @property
    def get_taxonomy_sections(self):
        '''Get list of taxonomy model sections.'''
        req = dr.discoRequest(self, "/taxonomy/sections")
        return req

    @property
    def get_taxonomy_locales(self):
        '''Get list of known taxonomy locales.'''
        req = dr.discoRequest(self, "/taxonomy/locales")
        return req

    def get_taxonomy_nodekind(self, format=None, section=None, locale=None, kind=None, fieldlists=False):
        '''Get list of defined node kinds with kind info.'''
        if format:
            self.params['format']=format
            self.params['section']=section
            self.params['locale']=locale
            req = dr.discoRequest(self, "/taxonomy/nodekinds")
        elif kind:
            self.params['locale']=locale
            if fieldlists:
                req = dr.discoRequest(self, "/taxonomy/nodekinds/{}/fieldlists".format(kind))
            else:
                req = dr.discoRequest(self, "/taxonomy/nodekinds/{}".format(kind))
        else:
            req = dr.discoRequest(self, "/taxonomy/nodekinds")
        return req
    get_taxonomy_nodekinds = property(get_taxonomy_nodekind)

    def get_taxonomy_nodekind_fieldlist(self, kind, fieldlist):
        '''Get list of fields for a node kind field list.'''
        req = dr.discoRequest(self, "/taxonomy/nodekinds/{}/fieldlists/{}".format(kind,fieldlist))
        return req

    def get_taxonomy_relkind(self, format=None, locale=None, kind=None):
        '''Get list of defined node kinds with kind info.'''
        if format:
            self.params['format']=format
            self.params['locale']=locale
            req = dr.discoRequest(self, "/taxonomy/relkinds")
        elif kind:
            self.params['locale']=locale
            req = dr.discoRequest(self, "/taxonomy/relkinds/{}".format(kind))
        else:
            req = dr.discoRequest(self, "/taxonomy/relkinds")
        return req
    get_taxonomy_relkinds = property(get_taxonomy_relkind)