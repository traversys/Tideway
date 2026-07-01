# -*- coding: utf-8 -*-

import tideway

appliance = tideway.main.Appliance

class Taxonomy(appliance):
    '''Retrieve taxonomy data.'''

    @property
    def get_taxonomy_sections(self):
        '''Get list of taxonomy model sections.'''
        req = self.get("/taxonomy/sections")
        return req

    @property
    def get_taxonomy_locales(self):
        '''Get list of known taxonomy locales.'''
        req = self.get("/taxonomy/locales")
        return req

    def get_taxonomy_nodekind(self, format=None, section=None, locale=None, kind=None, fieldlists=False):
        '''Get list of defined node kinds with kind info.'''
        if format:
            self.params['format']=format
            self.params['section']=section
            self.params['locale']=locale
            req = self.get("/taxonomy/nodekinds")
        elif kind:
            self.params['locale']=locale
            if fieldlists:
                req = self.get("/taxonomy/nodekinds/{}/fieldlists".format(kind))
            else:
                req = self.get("/taxonomy/nodekinds/{}".format(kind))
        else:
            req = self.get("/taxonomy/nodekinds")
        return req
    get_taxonomy_nodekinds = property(get_taxonomy_nodekind)

    def get_taxonomy_nodekind_fieldlist(self, kind, fieldlist):
        '''Get list of fields for a node kind field list.'''
        req = self.get("/taxonomy/nodekinds/{}/fieldlists/{}".format(kind,fieldlist))
        return req

    def get_taxonomy_relkind(self, format=None, locale=None, kind=None):
        '''Get list of defined node kinds with kind info.'''
        if format:
            self.params['format']=format
            self.params['locale']=locale
            req = self.get("/taxonomy/relkinds")
        elif kind:
            self.params['locale']=locale
            req = self.get("/taxonomy/relkinds/{}".format(kind))
        else:
            req = self.get("/taxonomy/relkinds")
        return req
    get_taxonomy_relkinds = property(get_taxonomy_relkind)
