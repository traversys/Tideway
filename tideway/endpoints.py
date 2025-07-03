#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tabulate import tabulate

docTable = [
                [
                    "GET", "/swagger.json", "- swagger()\n- api_swagger", "Get swagger file."
                    ],
                [
                    "GET", "/about", "- about()\n- api_about", "Return about info for API."
                    ],
                [
                    "GET",
                    "/admin/baseline",
                    "- baseline()\n- get_admin_baseline",
                    "Get a summary of the appliance status, and details of which baseline checks have passed or failed."
                    ],
                [
                    "GET",
                    "/admin/about",
                    "- admin()\n- get_admin_about",
                    "Get information about the appliance, like its version and versions of the installed packages."
                    ],
                [
                    "GET",
                    "/admin/licensing",
                    "- licensing()\n- get_admin_licensing",
                    "Get the latest signed licensing report."
                    ],
                [
                    "GET",
                    "/admin/licensing/raw",
                    "- licensing(content_type='raw')\n- get_admin_licensing_raw",
                    "Download the encrypted raw license data on this appliance for import on another appliance."
                    ],
                [
                    "GET",
                    "/admin/licensing/csv",
                    "- licensing(content_type='csv')\n- get_admin_licensing_csv",
                    "Download raw license data in CSV format as a zip file for offline analysis."
                    ],
                [
                    "GET",
                    "/admin/instance",
                    "- instance()\n- get_admin_instance",
                    "Get details about the appliance instance."
                    ],
                [
                    "GET",
                    "/admin/cluster",
                    "- cluster()\n- get_admin_cluster",
                    "Get cluster configuration and status."
                    ],
                [
                    "GET",
                    "/admin/organizations",
                    "- organizations()\n- get_admin_organizations",
                    "Get configured organizations."
                    ],
                [
                    "GET",
                    "/admin/preferences",
                    "- preferences()\n- get_admin_preferences",
                    "Get global appliance preferences."
                    ],
                [
                    "GET",
                    "/admin/builtin_reports",
                    "- builtin_reports()\n- get_admin_builtin_reports",
                    "Get built-in report definitions."
                    ],
                [
                    "GET",
                    "/admin/custom_reports",
                    "- custom_reports()\n- get_admin_custom_reports",
                    "Get custom report definitions."
                    ],
                [
                    "GET",
                    "/admin/smtp",
                    "- smtp()\n- get_admin_smtp",
                    "Get SMTP configuration."
                    ],
                [
                    "GET",
                    "/vault/credential_types",
                    "- listCredentialTypes()\n- get_vault_credential_type(group, cagetory)\n- get_vault_credential_types",
                    "Get a list of all credential types and filter by group and/or category."
                    ],
                [
                    "GET",
                    "/vault/credential_types/{cred_type_name}",
                    "- credentialType(cred_type_name)\n- get_vault_credential_type_name(cred_type_name)",
                    "Get the properties of a specific credential type."
                    ],
                [
                    "GET",
                    "/vault/credentials",
                    "- listCredentials()\n- get_vault_credential()\n- get_vault_credentials",
                    "Get a list of all credentials."
                    ],
                [
                    "POST",
                    "/vault/credentials",
                    "- newCredential(body)\n- post_vault_credential(body)",
                    "Create a new credential."
                    ],
                [
                    "DELETE",
                    "/vault/credentials/{cred_id}",
                    "- deleteCredential(cred_id)\n- delete_vault_credential(cred_id)",
                    "Delete a credential."
                    ],
                [
                    "GET",
                    "/vault/credentials/{cred_id}",
                    "- listCredentials(cred_id)\n- get_vault_credential(cred_id)",
                    "Get the properties of a specific credential."
                    ],
                [
                    "PATCH",
                    "/vault/credentials/{cred_id}",
                    "- updateCredential(cred_id, body)\n- patch_vault_credential(cred_id, body)",
                    "Updates partial resources of a credential. Missing properties are left unchanged."
                    ],
                [
                    "PUT",
                    "/vault/credentials/{cred_id}",
                    "- replaceCredential(cred_id, body)\n- put_vault_credential(cred_id, body)",
                    """Replaces a single credential. All required credential properties must be present."""
                    ],
                [
                    "GET",
                    "/data/search",
                    "- search('query')\n- get_data_search('query')",
                    "Run a search query, receiving paginated results."
                    ],
                [
                    "POST",
                    "/data/search",
                    "- search('query')\n- post_data_search('query')",
                    "An alternative to GET /data/search, for search queries which are too long for urls."
                    ],
                [
                    "GET",
                    "/data/search?format=object",
                    "- search('query',format='object')\n- get_data_search_object('query',format='object')",
                    "As /data/search but returns results as objects instead of rows of values."
                    ],
                [
                    "POST",
                    "/data/search?format=object",
                    "- search('query',format='object')\n- post_data_search_object('query',format='object')",
                    "An alternative to GET /data/search?format=object, for search queries which are too long for urls."
                    ],
                [
                    "GET",
                    "/data/search?format=tree",
                    "- search('query',format='tree')\n- get_data_search_tree('query',format='tree')",
                    "As /data/search but returns results as a tree of objects."
                    ],
                [
                    "POST",
                    "/data/search?format=tree",
                    "- search('query',format='tree')\n- post_data_search_tree('query',format='tree')",
                    "An alternative to GET /data/search?format=tree, for search queries which are too long for urls."
                    ],
                [
                    "GET/POST",
                    "/data/search",
                    "- search_bulk(query/body)",
                    "Run a bulk search query - loops through paginated results and returns a set of JSON results."
                    ],
                [
                    "POST",
                    "/data/condition",
                    "- post_data_condition('query')",
                    "Search using a condition, retrieving tabular data as arrays."
                    ],
                [
                    "POST",
                    "/data/condition?format=object",
                    "- post_data_condition('query',format='object')",
                    "Search using a condition, returning results as objects."
                    ],
                [
                    "POST",
                    "/data/condition?format=tree",
                    "- post_data_condition('query',format='tree')",
                    "Search using a condition, returning results as tree of objects."
                    ],
                [
                    "POST",
                    "/data/condition/param_values",
                    "- post_data_condition_param_values(body)",
                    "Get possible parameter values for a condition."
                    ],
                [
                    "GET",
                    "/data/condition/params",
                    "- get_data_condition_params()",
                    "Get the list of available condition parameters.",
                    ],
                [
                    "GET",
                    "/data/condition/templates",
                    "- get_data_condition_templates\n- get_data_condition_template()",
                    "Get a list of all templates."
                    ],
                [
                    "GET",
                    "/data/condition/templates/{template_id}",
                    "- get_data_condition_template(template_id)",
                    "Get the properties of a specific template."
                    ],
                [
                    "POST",
                    "/data/candidate",
                    "- best_candidate(body)\n- post_data_candidate(body)",
                    "The node object of the best candidate based on the provided parameters."
                    ],
                [
                    "POST",
                    "/data/candidates",
                    "- top_candidates(body)\n- post_data_candidates(body)",
                    "Enter parameters to identify a device, the response is a list of candidate nodes ordered by descending score"
                    ],
                [
                    "GET",
                    "/data/nodes/{node_id}",
                    "- nodeLookup(node_id)\n- get_data_nodes(node_id)",
                    "Get the state of a node with specified id"
                    ],
                [
                    "GET",
                    "/data/nodes/{node_id}?relationships=true",
                    "- nodeLookup(node_id,relationships=True)\n- get_data_nodes(node_id,relationships=True)",
                    "Get the state of a node with specified id, along with the traversal specs of all current relationships it has."
                    ],
                [
                    "GET",
                    "/data/nodes/{node_id}?traverse={traverse_spec}",
                    "- nodeLookup(node_id,traverse='traverse_spec')\n- get_data_nodes(node_id,traverse='traverse_spec')",
                    "Get the state of a node with specified id, along with the IDs of all nodes reached by following a traversal spec."
                    ],
                [
                    "GET",
                    "/data/nodes/{node_id}?traverse={attributes}",
                    "- nodeLookup(node_id,attributes='attributes')\n- get_data_nodes(node_id,attributes='attributes')",
                    "Get the state of a node with specified id, with only the attributes specified."
                    ],
                [
                    "GET",
                    "/data/nodes/{node_id}/graph",
                    "- graphNode(node_id)\n- get_data_nodes_graph(node_id)",
                    "Graph data represents a set of nodes and relationships that are associated to the given node."
                    ],
                [
                    "GET",
                    "/data/kinds/{kind}",
                    "- lookupNodeKind(kind)\n- get_data_kinds(kind)",
                    "Finds all nodes of a specified node kind."
                    ],
                [
                    "GET",
                    "/data/kinds/{kind}?format=object",
                    "- lookupNodeKind(kind,format='object')\n- get_data_kinds(kind,format='object')",
                    "As /data/kinds/{kind} but returns found nodes as objects instead of rows of attribute values."
                    ],
                [
                    "GET",
                    "/data/kinds/{kind}/values/{attribute}",
                    "- get_data_kinds_values(kind, attribute)",
                    "Retrieve values for an attribute of a node kind.",
                    ],
                [
                    "GET",
                    "/data/partitions",
                    "- partitions()\n- get_data_partitions",
                    "Get names and ids of partitions."
                    ],
                [
                    "POST",
                    "/data/partitions",
                    "- post_data_partitions(body)",
                    "Create a partition."
                    ],
                [
                    "POST",
                    "/data/import",
                    "- twImport(body)\n- post_data_import(body)",
                    "Imports data. Returns the import UUID."
                    ],
                [
                    "POST",
                    "/data/import/graph",
                    "- post_data_import_graph(body)",
                    "Import graph data. Returns the import UUID.",
                    ],
                [
                    "POST",
                    "/data/write",
                    "- twWrite(body)\n- post_data_write(body)",
                    "Perform arbitrary write operations."
                    ],
                [
                    "GET",
                    "/data/external_consumers",
                    "- get_data_external_consumers\n- get_data_external_consumer()",
                    "Retrieve external consumers.",
                    ],
                [
                    "POST",
                    "/data/external_consumers",
                    "- post_data_external_consumer(body)",
                    "Create an external consumer.",
                    ],
                [
                    "GET",
                    "/data/external_consumers/{consumer}",
                    "- get_data_external_consumer(consumer)",
                    "Retrieve an external consumer.",
                    ],
                [
                    "PATCH",
                    "/data/external_consumers/{consumer}",
                    "- patch_data_external_consumer(consumer, body)",
                    "Update an external consumer.",
                    ],
                [
                    "DELETE",
                    "/data/external_consumers/{consumer}",
                    "- delete_data_external_consumer(consumer)",
                    "Delete an external consumer.",
                    ],
                [
                    "GET",
                    "/data/external_consumers/{consumer}/{path}",
                    "- get_data_external_consumer(consumer, path)",
                    "Retrieve external consumer sub-resource.",
                    ],
                [
                    "POST",
                    "/data/external_consumers/{consumer}/{path}",
                    "- post_data_external_consumer(body, consumer, path)",
                    "Create or update external consumer sub-resource.",
                    ],
                [
                    "PATCH",
                    "/data/external_consumers/{consumer}/{path}",
                    "- patch_data_external_consumer(consumer, body, path)",
                    "Update external consumer sub-resource.",
                    ],
                [
                    "DELETE",
                    "/data/external_consumers/{consumer}/{path}",
                    "- delete_data_external_consumer(consumer, path)",
                    "Delete external consumer sub-resource.",
                    ],
                [
                    "GET",
                    "/discovery",
                    "- getDiscoveryStatus()\n- get_discovery",
                    "Get the current status of the discovery process."
                    ],
                [
                    "PATCH",
                    "/discovery",
                    "- setDiscoveryStatus(body)\n- patch_discovery(body)",
                    "Either start or stop the discovery process. Note this call can return before the desired state has been reached."
                    ],
                [
                    "GET",
                    "/discovery/api_provider_metadata",
                    "- getApiProviderMetadata()\n- get_discovery_api_provider_metadata",
                    """Get metadata for the API providers currently supported by BMC Discovery"""
                    ],
                [
                    "GET",
                    "/discovery/cloud_metadata",
                    "- getDiscoveryCloudMetaData()\n- get_discovery_api_cloud_metadata",
                    """Get metadata for the cloud providers currently supported by BMC Discovery."""
                    ],
                [
                    "GET",
                    "/discovery/excludes",
                    "- get_discovery_excludes\n- get_discovery_exclude()",
                    """Get a list of all excludes."""
                    ],
                [
                    "POST",
                    "/discovery/excludes",
                    "- post_discovery_exclude(body)",
                    """Create an exclude."""
                    ],
                [
                    "DELETE",
                    "/discovery/excludes/{exclude_id}",
                    "- delete_discovery_exclude(exclude_id)",
                    """Delete an exclude."""
                    ],
                [
                    "GET",
                    "/discovery/excludes/{exclude_id}",
                    "- get_discovery_exclude(exclude_id)",
                    """Get a specific exclude."""
                    ],
                [
                    "PATCH",
                    "/discovery/excludes/{exclude_id}",
                    "- patch_discovery_exclude(exclude_id, body)",
                    """Updates partial resources of an exclude. Missing properties are left unchanged."""
                    ],
                [
                    "GET",
                    "/discovery/runs",
                    "- getDiscoveryRuns()\n- get_discovery_run()\n- get_discovery_runs",
                    """Get details of all currently processing discovery runs."""
                    ],
                [
                    "POST",
                    "/discovery/runs",
                    "- discoveryRun(body)\n- post_discovery_run(body)",
                    """Create a new snapshot discovery run."""
                    ],
                [
                    "GET",
                    "/discovery/runs/{run_id}",
                    "- getDiscoveryRun(run_id)\n- get_discovery_run(run_id)",
                    """Get details of specific currently processing discovery run."""
                    ],
                [
                    "PATCH",
                    "/discovery/runs/{run_id}",
                    "- updateDiscoveryRun(run_id, body)\n- post_discovery_run(run_id, body)",
                    """Update the state of a specific discovery run"""
                    ],
                [
                    "GET",
                    "/discovery/runs/{run_id}/results",
                    "- getDiscoveryRunResults(run_id)\n- get_discovery_run_results(run_id)",
                    """Get a summary of the results from scanning all endpoints in the run, partitioned by result type."""
                    ],
                [
                    "GET",
                    "/discovery/runs/{run_id}/results/{result_type}",
                    "- getDiscoveryRunResult(run_id, result='result_type')\n- get_discovery_run_results(run_id, result='result_type')",
                    """Get a summary of the results from scanning all endpoints in the run that had a specific type of result."""
                    ],
                [
                    "GET",
                    "/discovery/runs/{run_id}/results/{result_type}?format=object",
                    "- getDiscoveryRunResult(run_id, format='object')\n- get_discovery_run_results(run_id, format='object')",
                    """As /discovery/runs/{run_id}/results/{result_type} but returns found nodes as objects instead of rows of attribute values."""
                    ],
                [
                    "GET",
                    "/discovery/runs/{run_id}/inferred",
                    "- getDiscoveryRunInferred(run_id)\n- get_discovery_run_inferred(run_id)",
                    """Get a summary of all inferred devices from a discovery run, partitioned by device type."""
                    ],
                [
                    "GET",
                    "/discovery/runs/{run_id}/inferred/{inferred_kind}",
                    "- getDiscoveryRunInferredKind(run_id, inferred_kind)\n- get_discovery_run_inferred(run_id, inferred_kind)",
                    """Get a summary of the devices inferred by a discovery run which have a specific inferred kind."""
                    ],
                [
                    "GET",
                    "/discovery/runs/{run_id}/inferred/{inferred_kind}?format=object",
                    "- getDiscoveryRunInferredKind(run_id, inferred_kind, format='object')\n- get_discovery_run_inferred(run_id, inferred_kind, format='object')",
                    """As /discovery/runs/{run_id}/inferred/{inferred_kind} but returns found nodes as objects instead of rows of attribute values."""
                    ],
                [
                    "GET",
                    "/discovery/runs/scheduled",
                    "- get_discovery_run_schedules\n- get_discovery_run_schedule()",
                    """Get details of all scheduled discovery runs."""
                    ],
                [
                    "POST",
                    "/discovery/runs/scheduled",
                    "- post_discovery_run_schedule(body)",
                    """Create a new scheduled discovery run."""
                    ],
                [
                    "DELETE",
                    "/discovery/runs/scheduled/{run_id}",
                    "- delete_discovery_run_schedule(run_id)",
                    """Delete a specific scheduled discovery run."""
                    ],
                [
                    "GET",
                    "/discovery/runs/scheduled/{run_id}",
                    "- get_discovery_run_schedule(run_id)",
                    """Get details of a specific scheduled discovery run."""
                    ],
                [
                    "PATCH",
                    "/discovery/runs/scheduled/{run_id}",
                    "- patch_discovery_run_schedule(run_id, body)",
                    """Get details of a specific scheduled discovery run."""
                    ],
                [
                    "POST",
                    "/events",
                    "- status(body)\n- post_events(body)",
                    """Returns a unique ID if the event has been recorded, otherwise an empty string is returned e.g. if the event source has been disabled."""
                    ],
                [
                    "GET",
                    "/vault/kerberos/realms",
                    "- get_vault_kerberos_realms\n- get_vault_kerberos_realm()",
                    """Retrieve all available realms."""
                    ],
                [
                    "DELETE",
                    "/vault/kerberos/realms/{realm_name}",
                    "- delete_vault_kerberos_realm(realm_name)",
                    """Delete a Kerberos realm."""
                    ],
                [
                    "GET",
                    "/vault/kerberos/realms/{realm_name}",
                    "- get_vault_kerberos_realm(realm_name)",
                    """Retrieve a Kerberos realm by name."""
                    ],
                [
                    "PATCH",
                    "/vault/kerberos/realms/{realm_name}",
                    "- patch_vault_kerberos_realm(realm_name)",
                    """Update a Kerberos realm."""
                    ],
                [
                    "POST",
                    "/vault/kerberos/realms/{realm_name}",
                    "- post_vault_kerberos_realm(realm_name, body)",
                    """Create a Kerberos realm."""
                    ],
                [
                    "POST",
                    "/vault/kerberos/realms/{realm_name}/test",
                    "- post_vault_kerberos_realm(realm_name, body, test=True)",
                    """Test user credentials by attempting to acquire a new Kerberos Ticket Granting Ticket (TGT)."""
                    ],
                [
                    "GET",
                    "/vault/kerberos/realms/{realm_name}/keytabs",
                    "- get_vault_kerberos_keytabs(realm_name)",
                    """Return a list of users with a Kerberos keytab file."""
                    ],
                [
                    "POST",
                    "/vault/kerberos/realms/{realm_name}/keytabs",
                    "- post_vault_kerberos_keytab(realm_name, username, keytab)",
                    """Upload a Kerberos keytab file."""
                    ],
                [
                    "DELETE",
                    "/vault/kerberos/realms/{realm_name}/keytabs",
                    "- delete_vault_kerberos_keytab(realm_name, username)",
                    """Delete the keytab file for a user."""
                    ],
                [
                    "GET",
                    "/vault/kerberos/realms/{realm_name}/ccaches",
                    "- get_vault_kerberos_ccaches(realm_name)",
                    """Return a list of users with a Kerberos credential cache file."""
                    ],
                [
                    "POST",
                    "/vault/kerberos/realms/{realm_name}/ccaches",
                    "- post_vault_kerberos_ccache(realm_name, username, ccache)",
                    """Upload a Kerberos credential cache file."""
                    ],
                [
                    "DELETE",
                    "/vault/kerberos/realms/{realm_name}/ccaches",
                    "- delete_vault_kerberos_ccache(realm_name, username)",
                    """Deletes the credential cache file for a user."""
                    ],
                [
                    "GET",
                    "/knowledge",
                    "- getKnowledgeManagement()\n- get_knowledge",
                    """Get the current state of the appliance's knowledge, including TKU versions."""
                    ],
                [
                    "POST",
                    "/knowledge/{filename}",
                    "- uploadKnowledge(filename, file)\n- post_knowledge(filename, file)",
                    """Upload a TKU or pattern module to the appliance."""
                    ],
                [
                    "GET",
                    "/knowledge/status",
                    "- getUploadStatus()\n- get_knowledge_status",
                    """Get the current state of a knowledge upload."""
                    ],
                [
                    "GET",
                    "/models",
                    "- get_models\n- get_model()",
                    """Get model definitions."""
                    ],
                [
                    "POST",
                    "/models",
                    "- post_model(body)",
                    """Create a new model."""
                    ],
                [
                    "DELETE",
                    "/models/{key}",
                    "- delete_model(key)",
                    """Delete a model."""
                    ],
                [
                    "GET",
                    "/models/{key}",
                    "- get_model_key(key)",
                    """Get model definition for the specified key."""
                    ],
                [
                    "PATCH",
                    "/models/{key}",
                    "- patch_model(key, body)",
                    """Modify a model."""
                    ],
                [
                    "GET",
                    "/models/{key}/topology",
                    "- get_model_topology(key)",
                    """Get topology for the model definition specified by key."""
                    ],
                [
                    "GET",
                    "/models/{key}/nodecount",
                    "- get_model_nodecount(key)",
                    """Get node count for the model definition specified by key."""
                    ],
                [
                    "GET",
                    "/models/{key}/nodes",
                    "- get_model_nodes(key)",
                    """Get nodes for the model definition specified by key."""
                    ],
                [
                    "GET",
                    "/models/{key}/nodes/{kind}",
                    "- get_model_nodes(key, kind='kind')",
                    """Get nodes by kind for the model definition specified by key."""
                    ],
                [
                    "DELETE",
                    "/models/by_node_id/{node_id}",
                    "- delete_model_by_node_id(node_id)",
                    """Delete a model."""
                    ],
                [
                    "GET",
                    "/models/by_node_id/{node_id}",
                    "- get_model_by_node_id(node_id)",
                    """Get model definition for the specified node id."""
                    ],
                [
                    "PATCH",
                    "/models/by_node_id/{node_id}",
                    "- patch_model_by_node_id(node_id, body)",
                    """Modify a model."""
                    ],
                [
                    "GET",
                    "/models/by_node_id/{node_id}/topology",
                    "- get_topology_by_node_id(node_id)",
                    """Get topology for the model definition specified by node id."""
                    ],
                [
                    "GET",
                    "/models/by_node_id/{node_id}/nodecount",
                    "- get_nodecount_by_node_id(node_id)",
                    """Get node count for the model definition specified by node id."""
                    ],
                [
                    "GET",
                    "/models/by_node_id/{node_id}/nodes",
                    "- get_nodes_by_node_id(node_id)",
                    """Get nodes for the model definition specified by node id."""
                    ],
                [
                    "GET",
                    "/models/by_node_id/{node_id}/nodes/{kind}",
                    "- get_nodes_by_node_id(node_id, kind='kind')",
                    """Get nodes by kind for the model definition specified by node id."""
                    ],
                [
                    "POST",
                    "/models/multi",
                    "- post_model_multi(body)",
                    """Manipulate multiple models in a single request."""
                    ],
                [
                    "GET",
                    "/taxonomy/sections",
                    "- get_taxonomy_sections",
                    """Get list of taxonomy model sections."""
                    ],
                [
                    "GET",
                    "/taxonomy/sections",
                    "- get_taxonomy_locales",
                    """Get list of known taxonomy locales."""
                    ],
                [
                    "GET",
                    "/taxonomy/nodekinds",
                    "- get_taxonomy_nodekinds\n- get_taxonomy_nodekind()",
                    """Get list of defined node kind names."""
                    ],
                [
                    "GET",
                    "/taxonomy/nodekinds?format=info",
                    "- get_taxonomy_nodekind(format='info')",
                    """Get list of defined node kind names."""
                    ],
                [
                    "GET",
                    "/taxonomy/nodekinds/{kind}",
                    "- get_taxonomy_nodekind(kind='kind')",
                    """Get defined node kind details."""
                    ],
                [
                    "GET",
                    "/taxonomy/nodekinds/{kind}/fieldlists",
                    "- get_taxonomy_nodekind(kind='kind', fieldlists=True)",
                    """Get list of node kind field lists."""
                    ],
                [
                    "GET",
                    "/taxonomy/nodekinds/{kind}/fieldlists/{fieldlist}",
                    "- get_taxonomy_nodekind_fieldlist(kind, fieldlist)",
                    """Get list of node kind field lists."""
                    ],
                [
                    "GET",
                    "/taxonomy/relkinds",
                    "- get_taxonomy_relkinds\n- get_taxonomy_relkind()",
                    """Get list of defined relationship kinds."""
                    ],
                [
                    "GET",
                    "/taxonomy/relkinds?format=info",
                    "- get_taxonomy_relkind(format='info')",
                    """Get list of defined relationship kinds with kind info."""
                    ],
                [
                    "GET",
                    "/taxonomy/relkinds/{kind}",
                    "- get_taxonomy_relkind(kind='kind')",
                    """Get defined relationship kind details."""
                    ],
                [
                    "GET",
                    "/data/nodes/{node_id}/graph",
                    "- graphNode(node_id)\n- get_data_nodes_graph(node_id)",
                    """Graph data represents a set of nodes and relationships that are associated to the given node."""
                    ],
                [
                    "POST",
                    "/topology/nodes",
                    "- getNodes(body)\n- post_topology_nodes",
                    """Get topology data from one or more starting nodes."""
                    ],
                [
                    "POST",
                    "/topology/nodes/kinds",
                    "- getNodeKinds(body)\n- post_topology_nodes_kinds",
                    """Get nodes of the specified kinds which are related to a given set of nodes."""
                    ],
                [
                    "GET",
                    "/topology/visualization_state",
                    "- visualizationState()\n- get_topology_viz_state",
                    """Get the current state of the visualization for the authenticated user."""
                    ],
                [
                    "PATCH",
                    "/topology/visualization_state",
                    "- updateVizState(body)\n- patch_topology_viz_state(body)",
                    """Update one or more attributes of the current state of the visualization for the authenticated user."""
                    ],
                [
                    "PUT",
                    "/topology/visualization_state",
                    "- replaceVizState(body)\n- put_topology_viz_state",
                    """Update any or all of the attributes of the current state of the visualization for the authenticated user."""
                    ],
                [
                    "GET",
                    "/vault",
                    "- getVault()\n- get_vault",
                    """Get details of the state of the vault."""
                    ],
                [
                    "PATCH",
                    "/vault",
                    "- updateVault(body)\n- patch_vault",
                    """Change the state of the vault."""
                ]
            ]

heads = [ "Method", "Endpoint", "Function Calls", "Description" ]

def docs(*endpoints):
    # Endpoint Docs
    if endpoints:
        tab = list()
        endpoint = endpoints[0]
        for line in docTable:
            if line[1] == endpoint:
                tab.append(line)
        if len(tab) > 0:
            print(tabulate(tab, headers=heads),"\n")
        else:
            print("API endpoint not found or not yet documented.\n")
    else:
        # display table
        print(tabulate(docTable, headers=heads, tablefmt="fancy_grid"),"\n")
