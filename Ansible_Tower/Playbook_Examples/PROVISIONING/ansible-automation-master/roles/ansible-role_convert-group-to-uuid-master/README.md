# Convert group to UUID


1. Query techmap db for UUID
2. Return UUID value

### Requirements
------------

This role requires a mssql query defined in the vars file.

### Role Variables
--------------

##### Variable Table

| Variable | Defined by |
|----------|------------|
| convert_group_to_uuid_hostname | defaults |
| convert_group_to_uuid_username | defaults |
| convert_group_to_uuid_password | defaults |
| convert_group_to_uuid_database | defaults |
| convert_group_to_uuid_group_name | defaults |
| techmap_query | vars |
| query_return | role |

##### Output Table

| Type | Name |
|------|------|
| fact | convert_group_to_uuid |

### Dependencies
------------
- mssql_query Ansible module [https://github.com/melmorabity/ansible-mssql-query](https://github.com/melmorabity/ansible-mssql-query)
- pymssql Python module


### Example Playbook
----------------
NOTE: some portions of the playbook have been replaced by ... for brevity.

```
---
- hosts: localhost
  remote_user: root
  include role:
    - ansible-role_convert-group-to-uuid
  vars:
    convert_group_to_uuid_hostname:
    convert_group_to_uuid_username:
    convert_group_to_uuid_password:
    convert_group_to_uuid_database:
    convert_group_to_uuid_group_name:
```
### License
-------

All rights reserved. BlueCross BlueShield of Tennessee, Inc.

### Author Information
------------------

William Collins

John Kennedy
