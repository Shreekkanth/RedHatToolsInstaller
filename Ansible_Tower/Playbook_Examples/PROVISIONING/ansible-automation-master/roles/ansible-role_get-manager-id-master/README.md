# Get Manager ID from Techmap DB

1. Query techmap db for User and Manager ID and email addresses.
2. Return User and Manager ID and email addresses values

### Requirements
------------

The mssql_query.py module is used to execute the SQL query defined in the vars file.

### Role Variables
--------------

##### Variable Table

| Variable | Defined by |
|----------|------------|
| get_manager_id_hostname | defaults |
| get_manager_id_username | defaults |
| get_manager_id_password | defaults |
| get_manager_id_database | defaults |
| get_manager_id_user_id | defaults |
| techmap_query | vars |
| query_return | role |

##### Output Table

| Type | Name |
|------|------|
| fact | get_manager_id.user_id |
| fact | get_manager_id.user_email |
| fact | get_manager_id.manager_id |
| fact | get_manager_id.manager_email |

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
  connection: local
  gather_facts: false

  vars:
    user_id:
    manager_id:
    env:

  tasks:
    - name: Get Manager ID
      include_role:
        name: ansible-role_get-manager-id
      vars:
        get_manager_id_user_id: "{{ user_id }}"
        get_manager_id_env: "{{ env }}"

    - name: Assert return value
      assert:
        that:
          - get_manager_id['manager_id'] == "{{ manager_id }}"
```
### License
-------

All rights reserved. BlueCross BlueShield of Tennessee, Inc.

### Author Information
------------------

William Collins

John Kennedy
