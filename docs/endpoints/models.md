---
sort: 9
---

# Models

Initiate a Model object for the instance of Discovery you intend to query.

Syntax:

```
tideway.models(__target__, __token__ [, _api_version_ ] [, _ssl_verify_ ])
```

Initiation:

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> model = tw.models()
```

## get_model()

Retrieve service and application models.

Syntax:

```
.get_model([ _name_ ] [, type ] [, kind ] [, published ] [, review_suggested ] [, version ] [, favorite ] [, compatibility ] [, results_id ] [, delete ])
```

| Parameters   | Type        | Required | Default Value | Options  |
| ------------ | ----------- | :------: | ------------- | -------- |
| name         | String      | No       | N/A           | N/A      |
| type         | String      | No       | N/A           | <ul><li>"rules_template"</li><li>"rules"</li><li>"sam"</li><li>"static"</li><li>"instance"</li><li>"imported"</li></ul> |
| kind         | String      | No       | N/A           | <ul><li>"BusinessService"</li><li>"TechnicalService"</li><li>"BusinessApplicationInstance"</li></ul> |
| published    | Boolean     | No       | N/A           | <ul><li>True</li><li>False</li></ul> |
| review_suggested | Boolean | No       | N/A           | <ul><li>True</li><li>False</li></ul> |
| version      | String      | No       | N/A           | N/A      |
| favorite     | Boolean     | No       | N/A           | <ul><li>True</li><li>False</li></ul> |
| compatibility | String     | No       | N/A           | N/A      |
| results_id   | String      | No       | N/A           | N/A      |
| delete       | Boolean     | No       | False         | <ul><li>True</li><li>False</li></ul> |

## get_models

Retrieve all models. See [get_model](#get_model).

Syntax: `.get_models`

## post_model()

Create a new model.

Syntax:

```
.post_model(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

## post_model_multi()

Create multiple new models.

Syntax:

```
.post_model_multi(__json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| json          | JSON Object | Yes      | N/A           | N/A      |

## get_model_key()

Get model definition for the specified key.

Syntax:

```
.get_model_key(__key__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| key           | String      | Yes      | N/A           | N/A      |

## delete_model()

Delete a model.

Syntax:
```
.delete_model(__key__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| key           | String      | Yes      | N/A           | N/A      |

## patch_model()

Update a model.

Syntax:
```
.patch_model(__key__, __json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| key           | String      | Yes      | N/A           | N/A      |
| json          | JSON Object | Yes      | N/A           | N/A      |

## get_model_topology()

Get topology for the model definition specified by key.

Syntax:

```
.get_model_topology(__key__ [, attributes ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| key           | String      | Yes      | N/A           | N/A      |
| attributes    | String (CSV) | No      | N/A           | N/A      |

## get_model_nodecount()

Get node count for the model definition specified by key.

Syntax:

```
.get_model_nodecount(__key__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| key           | String      | Yes      | N/A           | N/A      |

## get_model_nodes()

Retrieve service and application models.

Syntax:

```
.get_model_nodes(__key__ [, results_id ] [, delete ] [, kind ])
```

| Parameters   | Type        | Required | Default Value | Options  |
| ------------ | ----------- | :------: | ------------- | -------- |
| key          | String      | Yes      | N/A           | N/A      |
| results_id   | String      | No       | N/A           | N/A      |
| delete       | Boolean     | No       | False         | <ul><li>True</li><li>False</li></ul> |
| kind         | String      | No       | N/A           | N/A      |

## get_model_by_node_id()

Get model definition for the specified node id.

Syntax:
```
.get_model_by_node_id(__node_id__ [, expand_related ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| node_id       | String      | Yes      | N/A           | N/A      |
| expand_related | Boolean    | Yes      | N/A           | <ul><li>True</li><li>False</li></ul> |

## delete_model_by_node_id()

Delete a model.

Syntax:
```
.delete_model_by_node_id(__node_id__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| node_id       | String      | Yes      | N/A           | N/A      |

## patch_model_by_node_id()

Delete a model.

Syntax:
```
.patch_model_by_node_id(__node_id__, __json__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| node_id       | String      | Yes      | N/A           | N/A      |
| json          | JSON Object | Yes      | N/A           | N/A      |

## get_topology_by_node_id()

Delete a model.

Syntax:
```
.get_topology_by_node_id(__node_id__ [, attributes ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| node_id       | String      | Yes      | N/A           | N/A      |
| attributes    | String (CSV) | No      | N/A           | N/A      |

## get_nodecount_by_node_id()

Get node count for the model definition specified by node id.

Syntax:
```
.get_nodecount_by_node_id(__node_id__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| node_id       | String      | Yes      | N/A           | N/A      |

## get_nodes_by_node_id()

Get nodes for the model definition specified by node id.

Syntax:

```
.get_nodes_by_node_id(__node_id__ [, results_id ] [, delete ] [, kind ])
```

| Parameters   | Type        | Required | Default Value | Options  |
| ------------ | ----------- | :------: | ------------- | -------- |
| key          | String      | Yes      | N/A           | N/A      |
| results_id   | String      | No       | N/A           | N/A      |
| delete       | Boolean     | No       | False         | <ul><li>True</li><li>False</li></ul> |
| kind         | String      | No       | N/A           | N/A      |