# Add CI to CA CMDB master


1. Obtains an acces token
2. Queries the CMDB database via a REST call
3. Verifies an entry doesn't already exist for the new server
4. Adds a new record to the CMDB
5. Updates the new record with additional information
6. Deletes the access token

### Requirements
------------

This role includes two jinja2 templates:
    create_ci.j2
    update_server_ci.j2

### Role Variables
--------------

##### Variable Table

| Variable | Defined by |
|----------|------------|
| cmdb_add_ci_api_base_url | defaults |
| cmdb_add_ci_api_key | defaults |
| cmdb_add_ci_server_name | defaults |
| cmdb_add_ci_assign_group | defaults |
| cmdb_add_ci_requestor_id | defaults |
| cmdb_add_ci_manager_id | defaults |
| cmdb_add_ci_class_name | defaults |
| cmdb_add_ci_is_ci | defaults |
| cmdb_add_ci_is_asset | defaults |
| cmdb_add_ci_delete_flag | defaults |
| cmdb_add_ci_server_state | defaults |
| cmdb_add_ci_server_application | defaults |
| cmdb_add_ci_server_core_count | defaults |
| cmdb_add_ci_server_patch_group | defaults |
| cmdb_add_ci_z_is_backup | defaults |
| server_state_map: | vars |
| beta: | vars |
| -  prefix | vars |
| -  patch_group | vars |
| development: | vars |
| -  prefix | vars |
| -  patch_group | vars |
| glb_development: | vars |
| -  prefix | vars |
| -  patch_group | vars |
| glb_test: | vars |
| -  prefix | vars |
| -  patch_group | vars |
| release: | vars |
| -  prefix | vars |
| -  patch_group | vars |
| standby: | vars |
| -  prefix | vars |
| -  patch_group | vars |
| test: | vars |
| -  prefix | vars |
| -  patch_group | vars |
| pre_production: | vars |
| -  prefix | vars |
| -  patch_group | vars |
| auth_key_result | role |
| server_name_query | role |
| assignment_group_query | role |
| manager_query | role |
| create_ci_result | role |
| update_ci_result | role |
| delete_access_key_result | role |


### Dependencies
------------

### Example Playbook
----------------
NOTE: some portions of the playbook have been replaced by ... for brevity.

```
---
- hosts: localhost
  remote_user: root
  tasks:
    - name: Include role
      include_role:
        name: ansible-role_cmdb-add-ci
      vars:
        cmdb_add_ci_api_base_url:
        cmdb_add_ci_api_key:
        cmdb_add_ci_server_name:
        cmdb_add_ci_assign_group:
        cmdb_add_ci_requestor_id:
        cmdb_add_ci_manager_id:
        cmdb_add_ci_class_name:
        cmdb_add_ci_is_ci:
        cmdb_add_ci_is_asset:
        cmdb_add_ci_delete_flag:
        cmdb_add_ci_server_state:
        cmdb_add_ci_server_application:
        cmdb_add_ci_server_core_count:
        cmdb_add_ci_server_patch_group:
        cmdb_add_ci_z_is_backup:
```
### License
-------

All rights reserved. BlueCross BlueShield of Tennessee, Inc.

### Author Information
------------------

William Collins

John Kennedy
