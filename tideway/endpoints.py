#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tabulate import tabulate

docTable = [
                [
                    "/swagger.json",
                    "swagger()",
                    "Get swagger file."
                    ],
                [
                    "/about",
                    "about()",
                    "Return about info for API."
                    ],
                [
                    "/admin/baseline",
                    "baseline()",
                    "Get a summary of the appliance status, and details of which baseline checks have passed or failed."
                    ],
                [
                    "/admin/about",
                    "admin()",
                    "Get information about the appliance, like its version and versions of the installed packages."
                    ],
                [
                    "/admin/licensing",
                    "licensing()",
                    "Get the latest signed licensing report."
                    ],
                [
                    "/admin/licensing/raw",
                    "licensing(content_type='raw')",
                    "Download the encrypted raw license data on this appliance for import on another appliance."
                    ],
                [
                    "/admin/licensing/csv",
                    "licensing(content_type='csv')",
                    "Download raw license data in CSV format as a zip file for offline analysis."
                    ],
                [
                    "/vault/credential_types",
                    "listCredentialTypes()",
                    "Get a list of all credential types and filter by group and/or category."
                    ],
                [
                    "/vault/credential_types/{cred_type_name}",
                    "credentialType(cred_type_name)",
                    "Get the properties of a specific credential type."
                    ],
                [
                    "/vault/credentials",
                    "listCredentials()",
                    "Get a list of all credentials."
                    ],
                [
                    "/vault/credentials",
                    "newCredential(body)",
                    "Create a new credential."
                    ],
                [
                    "/vault/credentials/{cred_id}",
                    "deleteCredential(cred_id)",
                    "Delete a credential."
                    ],
                [
                    "/vault/credentials/{cred_id}",
                    "listCredentials(cred_id)",
                    "Get the properties of a specific credential."
                    ],
                [
                    "/vault/credentials/{cred_id}",
                    "updateCredential(cred_id, body)",
                    "Updates partial resources of a credential. Missing properties are left unchanged."
                    ],
                [
                    "/vault/credentials/{cred_id}",
                    "replaceCredential(cred_id, body)",
                    """Replaces a single credential. All required credential properties must be present."""
                    ],
                [
                    "/data/search",
                    "search('query')",
                    "Run a search query, receiving paginated results."
                    ],
                [
                    "/data/search",
                    "search(body)",
                    "An alternative to GET /data/search, for search queries which are too long for urls."
                    ],
                [
                    "/data/search?format=object",
                    "search('query',format='object')",
                    "As /data/search but returns results as objects instead of rows of values."
                    ],
                [
                    "/data/search?format=object",
                    "search(body,format='object')",
                    "An alternative to GET /data/search?format=object, for search queries which are too long for urls."
                    ],
                [
                    "/data/search?format=tree",
                    "search('query',format='tree')",
                    "As /data/search but returns results as a tree of objects."
                    ],
                [
                    "/data/search?format=tree",
                    "search(body,format='tree')",
                    "An alternative to GET /data/search?format=tree, for search queries which are too long for urls."
                    ],
                [
                    "/data/search",
                    "search_bulk(query/body)",
                    "Run a bulk search query - loops through paginated results and returns a set of JSON results."
                    ],
                [
                    "/data/candidate",
                    "candidate(body)",
                    "The node object of the best candidate based on the provided parameters."
                    ],
                [
                    "/data/candidates",
                    "candidates(body)",
                    "Enter parameters to identify a device, the response is a list of candidate nodes ordered by descending score"
                    ],
                [
                    "/data/nodes/{node_id}",
                    "nodeLookup(node_id)",
                    "Get the state of a node with specified id"
                    ],
                [
                    "/data/nodes/{node_id}?relationships=true",
                    "nodeLookup(node_id,relationships=True)",
                    "Get the state of a node with specified id, along with the traversal specs of all current relationships it has."
                    ],
                [
                    "/data/nodes/{node_id}?traverse={traverse_spec}",
                    "nodeLookup(node_id,traverse='traverse_spec')",
                    "Get the state of a node with specified id, along with the IDs of all nodes reached by following a traversal spec."
                    ],
                [
                    "/data/nodes/{node_id}?traverse={attributes}",
                    "nodeLookup(node_id,attributes='attributes')",
                    "Get the state of a node with specified id, with only the attributes specified."
                    ],
                [
                    "/data/nodes/{node_id}/graph",
                    "graphNode(node_id)",
                    "Graph data represents a set of nodes and relationships that are associated to the given node."
                    ],
                [
                    "/data/kinds/{kind}",
                    "lookupNodeKind(kind)",
                    "Finds all nodes of a specified node kind."
                    ],
                [
                    "/data/kinds/{kind}?format=object",
                    "lookupNodeKind(kind,format='object')",
                    "As /data/kinds/{kind} but returns found nodes as objects instead of rows of attribute values."
                    ],
                [
                    "/data/partitions",
                    "partitions()",
                    "Get names and ids of partitions."
                    ],
                [
                    "/data/import",
                    "twImport(body)",
                    "Imports data. Returns the import UUID."
                    ],
                [
                    "/data/write",
                    "twWrite(body)",
                    "Perform arbitrary write operations."
                    ],
                [
                    "/discovery",
                    "getDiscoveryStatus()",
                    "Get the current status of the discovery process."
                    ],
                [
                    "/discovery",
                    "setDiscoveryStatus(body)",
                    "Either start or stop the discovery process. Note this call can return before the desired state has been reached."
                    ],
                [
                    "/discovery/api_provider_metadata",
                    "getApiProviderMetadata()",
                    """Get metadata for the API providers currently supported by BMC Discovery"""
                    ],
                [
                    "/discovery/cloud_metadata",
                    "getDiscoveryCloudMetaData()",
                    """Get metadata for the cloud providers currently supported by BMC Discovery."""
                    ],
                [
                    "/discovery/runs",
                    "getDiscoveryRuns()",
                    """Get details of all currently processing discovery runs."""
                    ],
                [
                    "/discovery/runs",
                    "discoveryRun(body)",
                    """Create a new snapshot discovery run."""
                    ],
                [
                    "/discovery/runs/{run_id}",
                    "getDiscoveryRun(runid)",
                    """Get details of specific currently processing discovery run."""
                    ],
                [
                    "/discovery/runs/{run_id}",
                    "updateDiscoveryRun(runid, body)",
                    """Update the state of a specific discovery run"""
                    ],
                [
                    "/discovery/runs/{run_id}/results",
                    "getDiscoveryRunResults(runid):",
                    """Get a summary of the results from scanning all endpoints in the run, partitioned by result type."""
                    ],
                [
                    "/discovery/runs/{run_id}/results/{result_type}",
                    "getDiscoveryRunResult(runid, result='result_type')",
                    """Get a summary of the results from scanning all endpoints in the run that had a specific type of result."""
                    ],
                [
                    "/discovery/runs/{run_id}/results/{result_type}?format=object",
                    "getDiscoveryRunResult(runid, format='object')",
                    """As /discovery/runs/{run_id}/results/{result_type} but returns found nodes as objects instead of rows of attribute values."""
                    ],
                [
                    "/discovery/runs/{run_id}/inferred",
                    "getDiscoveryRunInferred(runid)",
                    """Get a summary of all inferred devices from a discovery run, partitioned by device type."""
                    ],
                [
                    "/discovery/runs/{run_id}/inferred/{inferred_kind}",
                    "getDiscoveryRunInferredKind(runid, inferred_kind)",
                    """Get a summary of the devices inferred by a discovery run which have a specific inferred kind."""
                    ],
                [
                    "/discovery/runs/{run_id}/inferred/{inferred_kind}?format=object",
                    "getDiscoveryRunInferredKind(runid, inferred_kind, format='object')",
                    """As /discovery/runs/{run_id}/inferred/{inferred_kind} but returns found nodes as objects instead of rows of attribute values."""
                    ],
                [
                    "/events",
                    "status(body)",
                    """Returns a unique ID if the event has been recorded, otherwise an empty string is returned e.g. if the event source has been disabled."""
                    ],
                [
                    "/knowledge",
                    "getKnowledgeManagement()",
                    """Get the current state of the appliance's knowledge, including TKU versions."""
                    ],
                [
                    "/knowledge/{filename}",
                    "uploadKnowledge(filename, file)",
                    """Upload a TKU or pattern module to the appliance."""
                    ],
                [
                    "/knowledge/status",
                    "getUploadStatus()",
                    """Get the current state of a knowledge upload"""
                    ],
                [
                    "/data/nodes/{node_id}/graph",
                    "graphNode(node_id)",
                    """Graph data represents a set of nodes and relationships that are associated to the given node."""
                    ],
                [
                    "/topology/nodes",
                    "getNodes(body)",
                    """Get topology data from one or more starting nodes."""
                    ],
                [
                    "/topology/nodes/kinds",
                    "getNodeKinds(body)",
                    """Get nodes of the specified kinds which are related to a given set of nodes."""
                    ],
                [
                    "/topology/visualization_state",
                    "visualizationState()",
                    """Get the current state of the visualization for the authenticated user."""
                    ],
                [
                    "/topology/visualization_state",
                    "updateVizState(body)",
                    """Update one or more attributes of the current state of the visualization for the authenticated user."""
                    ],
                [
                    "/topology/visualization_state",
                    "replaceVizState(body)",
                    """Update any or all of the attributes of the current state of the visualization for the authenticated user."""
                    ],
                [
                    "/vault",
                    "getVault()",
                    """Get details of the state of the vault."""
                    ],
                [
                    "/vault",
                    "updateVault(body)",
                    """Change the state of the vault."""
                ]
            ]

heads = [ "Endpoint", "Function", "Description" ]

def docs(*endpoints):
    # Endpoint Docs
    if endpoints:
        tab = list()
        endpoint = endpoints[0]
        for line in docTable:
            if line[0] == endpoint:
                tab.append(line)
        if len(tab) > 0:
            print(tabulate(tab, headers=heads))
        else:
            print("API endpoint not found or not yet documented.")
    else:
        # display table
        print(tabulate(docTable, headers=heads))
