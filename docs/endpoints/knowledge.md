---
sort: 7
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

## getKnowledgeManagement()

Get the current state of the appliance's knowledge, including TKU versions.

Syntax:

```
.getKnowledgeManagement()
```

Example:

```python
>>> >>> knowledge.getKnowledgeManagement().json()['latest_tku']['submission_date']
'2021-05-24T23:06:00.350840+00:00'
```

## getUploadStatus()

Get the current state of a knowledge upload.

Syntax:

```
.getUploadStatus()
```

Example:

```python
>>> upload = knowledge.getUploadStatus()
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

## uploadKnowledge()

Upload a TKU or pattern module to the appliance.

Syntax:

```
.uploadKnowledge(__filename__, __file__ [, _activate_ ] [, _allow_restart_ ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| filename      | String      | Yes      | N/A           | N/A      |
| file          | String      | Yes      | N/A           | N/A      |
| activate      | Boolean     | No       | True  | <ul><li>True</li><li>False</li></ul> |
| allow_restart | Boolean     | No       | False | <ul><li>True</li><li>False</li></ul> |

Example:

```python
>>> knowledge.uploadKnowledge("TestPattern.tpl","C:/Users/User001/Documents/TestPattern.tpl").ok
True
```