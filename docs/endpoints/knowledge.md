---
sort: 8
---

# Knowledge

Initiate a Knowledge object for the instance of Discovery you intend to query.

Syntax:

```
tideway.knowledge(__target__, __token__ [, _api_version_ ] [, _ssl_verify_ ])
```

Initiation:

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> knowledge = tw.knowledge()
```

## get_knowledge

Get the current state of the appliance's knowledge, including TKU versions.

Syntax:

```
.get_knowledge
```

Example:

```python
>>> >>> knowledge.get_knowledge.json()['latest_tku']['submission_date']
'2021-05-24T23:06:00.350840+00:00'
```

## get_knowledge_status

Get the current state of a knowledge upload.

Syntax:

```
.get_knowledge_status
```

Example:

```python
>>> upload = knowledge.get_knowledge_status
>>> from pprint import pprint
>>> pprint(upload.json())
{
    "error": "",
    "last_result": "success",
    "messages": [
        "Validate upload: Completed OK",
        "Load TestPattern: Uploaded TestPattern.tpl as \"TestPattern\"",
        "Load TestPattern: Completed OK",
        "Activate Pattern Modules: 1 knowledge upload activated",
        "Activate Pattern Modules: Completed OK"
    ],
    "processing": false,
    "uploading": false
}
```

## post_knowledge()

Upload a TKU or pattern module to the appliance.

Syntax:

```
.post_knowledge(__filename__, __file__ [, _activate_ ] [, _allow_restart_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| filename      | String      | Yes      | N/A           | N/A      |
| file          | String      | Yes      | N/A           | N/A      |
| activate      | Boolean     | No       | True  | <ul><li>True</li><li>False</li></ul> |
| allow_restart | Boolean     | No       | False | <ul><li>True</li><li>False</li></ul> |

Example:

```python
>>> knowledge.post_knowledge("TestPattern.tpl","C:/Users/User001/Documents/TestPattern.tpl").ok
True
```

## get_knowledge_trigger_patterns()

Get a list of trigger patterns.

Syntax:

```
.get_knowledge_trigger_patterns([ _lookup_data_sources_ ])
```

| Parameters          | Type    | Required | Default Value | Options                          |
| ------------------- | ------- | :------: | ------------- | -------------------------------- |
| lookup_data_sources | Boolean | No       | N/A           | <ul><li>True</li><li>False</li></ul> |

## getKnowledgeManagement()

[Deprecated] See [get_knowledge](#get_knowledge) for usage.

Syntax: `.getKnowledgeManagement()`

## getUploadStatus()

[Deprecated] See [get_knowledge_status](#get_knowledge_status) for usage.

Syntax: `.getUploadStatus()`

## uploadKnowledge()

[Deprecated] See [post_knowledge](#post_knowledge) for usage.

Syntax: `.uploadKnowledge(__filename__, __file__ [, _activate_ ] [, _allow_restart_ ])`