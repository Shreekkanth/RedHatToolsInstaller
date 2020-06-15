# Generate Server Name

1. Query techmap db to generate unique server name
2. Return server name

### Requirements
------------

The mssql_query.py module is used to execute the SQL query defined in the vars file.

Must supply all variable to execute MSSQL store procedure.

### Role Variables
--------------

##### Variable Table

| Variable | Defined by |
|----------|------------|
| generate_server_name_hostname | defaults |
| generate_server_name_username | defaults |
| generate_server_name_password | defaults |
| generate_server_name_database | defaults |
| generate_server_name_requestor_id | defaults |
| generate_server_name_model | defaults |
| generate_server_name_machine_type | defaults |
| generate_server_name_serial | defaults |
| generate_server_name_os | defaults |
| generate_server_name_server_type | defaults |
| generate_server_name_primary_contact | defaults |
| generate_server_name_secondary_contact | defaults |
| generate_server_name_tertiary_contact | defaults |
| generate_server_name_assignment_group | defaults |
| generate_server_name_kernel | defaults |
| generate_server_name_cpu_count | defaults |
| generate_server_name_core_count | defaults |
| generate_server_name_application | defaults |
| generate_server_name_patch_group | defaults |
| generate_server_name_location | defaults |
| generate_server_name_server_domain | defaults |
| generate_server_name_server_rack | defaults |
| generate_server_name_server_state | defaults |
| generate_server_name_server_form_factor | defaults |
| generate_server_name_prefix | defaults |
| generate_server_name_cluster_number | defaults |
| generate_server_name_instance_number | defaults |
| server_state_map | vars |
|   beta: | vars |
|   - prefix | vars |
|   - patch_group | vars |
|   development: | vars |
|   - prefi | vars |
|   - patch_group | vars |
|   glb_development: | vars |
|   - prefix | vars |
|   - patch_group | vars |
|   glb_test: | vars |
|   - prefix | vars |
|   - patch_group | vars |
|   release: | vars |
|   - prefix | vars |
|   - patch_group | vars |
|   standby: | vars |
|   - prefix | vars |
|   - patch_group | vars |
|   test: | vars |
|   - prefix | vars |
|   - patch_group | vars |
|   pre_production: | vars |
|   - prefix | vars |
|   - patch_group | vars |
| techmap_query | vars |
| query_return | role |

##### Output Table

| Type | Name |
|------|------|
| fact | generate_server_name_result |

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
    - ansible-role_generate-server-name
  vars:
    generate_server_name_hostname:
    generate_server_name_username:
    generate_server_name_password:
    generate_server_name_database:
    generate_server_name_requestor_id:
    generate_server_name_model:
    generate_server_name_machine_type:
    generate_server_name_serial:
    generate_server_name_os:
    generate_server_name_server_type:
    generate_server_name_primary_contact:
    generate_server_name_secondary_contact:
    generate_server_name_tertiary_contact:
    generate_server_name_assignment_group:
    generate_server_name_kernel:
    generate_server_name_cpu_count:
    generate_server_name_core_count:
    generate_server_name_application:
    generate_server_name_patch_group:
    generate_server_name_location:
    generate_server_name_server_domain:
    generate_server_name_server_rack:
    generate_server_name_server_state: test
    generate_server_name_server_form_factor:
    generate_server_name_prefix:
    generate_server_name_cluster_number:
    generate_server_name_instance_number:
```
### License
-------

All rights reserved. BlueCross BlueShield of Tennessee, Inc.

### Author Information
------------------

William Collins

John Kennedy
