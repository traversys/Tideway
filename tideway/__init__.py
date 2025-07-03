#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tideway import main, \
                    admin, \
                    discovery, \
                    data, \
                    vault, \
                    credentials, \
                    knowledge, \
                    events, \
                    kerberos, \
                    security, \
                    models, \
                    taxonomy, \
                    topology

# Main declaration to create an appliance object
appliance = main.Appliance
outpost = main.Appliance

# For the previous version classes single file - moved to main.py
# Method 1: tideway._________(appliance,token)
# method 2: tideway.________.func(appliance)
admin = admin.Admin
credentials = credentials.Credentials
data = data.Data
discovery = discovery.Discovery
events = events.Events
kerberos = kerberos.Kerberos
knowledge = knowledge.Knowledge
models = models.Models
taxonomy = taxonomy.Taxonomy
topology = topology.Topology
vault = vault.Vault
security = security.Security
