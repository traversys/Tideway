---
sort: 6
---

# Knowledge

- Initiate a Knowledge object for the instance of Discovery you intend to query.

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> knowledge = tw.knowledge()
```

## getKnowledgeManagement()

- Get the current state of the appliance's knowledge, including TKU versions.

```python
>>> knowledge.getKnowledgeManagement().json()
{
    "devices": "5.0.2020.09.3",
    "latest_edp": {
        "active_count": 12,
        "inactive_count": 0,
        "modified": false,
        "name": "EDP-2020-09-3-ADDM-12.1+",
        "origin": "TKU",
        "package": "Extended Data Pack",
        "submission_date": "2020-09-11T19:52:15.165794+00:00",
        "superseded_count": 0,
        "upload_id": "fb528ec3f5afe096e4b6e6f776c6564"
    },
...
```

## getUploadStatus()

- Get the current state of a knowledge upload.

```python
>>> knowledge.getUploadStatus().json()
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

- Upload a TKU or pattern module to the appliance.

Syntax: `uploadKnowledge(*filename*, *file* [, activate=*optional* (default=*True*) ] [, allow_restart=*optional* (default=*False*)])`

| Parameters | Type | Use | Options
| - | - | - | -
| **filename** | String | Required | |
| **file** | String | Required | |
| activate=**boolean** | Boolean | | True<br>False |
| allow_restart=**boolean** | Boolean | | True<br>False |

```python
>>> knowledge.uploadKnowledge("TestPattern.tpl","C:/Users/User001/Documents/TestPattern.tpl")
```