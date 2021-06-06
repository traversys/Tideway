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
                    topology

# Main declaration to create an appliance object
appliance = main.Appliance

# For the previous version classes single file - moved to main.py
# Method 1: tideway._________(appliance,token)
# method 2: tideway.________.func(appliance)
discovery = discovery.Discovery
data = data.Data
vault = vault.Vault
credentials = credentials.Credentials
knowledge = knowledge.Knowledge
events = events.Events
admin = admin.Admin
topology = topology.Topology
