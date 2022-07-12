---
sort: 10
---

# Taxonomy

Initiate a Taxonomy object for the instance of Discovery you intend to query.

Syntax:

```
tideway.taxonomy(__target__, __token__ [, _api_version_ ] [, _ssl_verify_ ])
```

Initiation:

```python
>>> import tideway
>>> tw = tideway.appliance('appliance-hostname','auth-token')
>>> taxonomy = tw.taxonomy()
```

## get_taxonomy_sections

Get list of taxonomy model sections.

Syntax:

```
.get_taxonomy_sections
```

## get_taxonomy_locales

Get list of known taxonomy locales.

Syntax:

```
.get_taxonomy_locales
```

## get_taxonomy_nodekind()

Get list of defined node kinds with kind info.

Syntax:
```
.get_taxonomy_nodekind([ format ] [, section ] [, locale ] [, kind ] [, fieldlists ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| format        | String      | No       | N/A           | N/A      |
| section       | String      | No       | N/A           | N/A      |
| kind          | String      | No       | N/A           | N/A      |
| fieldlists    | Boolean     | No       | False         | <ul><li>True</li><li>False</li></ul> |

## get_taxonomy_nodekinds

Get list of all node kinds with kind info. See [get_taxonomy_nodekind](#get_taxonomy_nodekind).

Syntax: `.get_taxonomy_nodekinds`

## get_taxonomy_nodekind_fieldlist()

Get list of fields for a node kind field list.

Syntax:
```
.get_taxonomy_nodekind_fieldlist(__kind__, __fieldlists__)
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| kind          | String      | Yes      | N/A           | N/A      |
| fieldlists    | String      | Yes      | N/A           | N/A      |

## get_taxonomy_relkind()

Get list of defined node kinds with kind info.

Syntax:
```
.get_taxonomy_relkind( [ format, locale ] [, kind ])
```

| Parameters    | Type        | Required | Default Value | Options  |
| ------------- | ----------- | :------: | ------------- | -------- |
| format        | String      | No       | N/A           | N/A      |
| locale        | String      | No       | N/A           | N/A      |
| kind          | String      | No       | N/A           | N/A      |

## get_taxonomy_relkinds

Get list of all node kinds with kind info. See [get_taxonomy_relkinds](#get_taxonomy_relkinds).

Syntax: `.get_taxonomy_relkinds`