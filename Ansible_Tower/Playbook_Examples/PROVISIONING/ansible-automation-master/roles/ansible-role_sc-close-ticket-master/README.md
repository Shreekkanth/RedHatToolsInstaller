# Service Catalog (ISDirect) Close Ticket

1. Login to the Service Catalog
2. Get session ID
3. Get subscription ID
4. Get catalog status
5. Update the catalog

### Requirements
------------

### Role Variables
--------------

##### Variable Table

| Variable | Defined by |
|----------|------------|
| sc_close_ticket_api_base_url: | defaults |
| sc_close_ticket_api_username: | defaults |
| sc_close_ticket_api_password: | defaults |
| sc_close_ticket_request_item_id: | defaults |
| sc_close_ticket_status_code: 2000 | defaults |
| return_login | role |
| login_return | role |
| return_form_id | role |
| form_id_return | role |
| catalog_status | role |
| status_catalog | role |
| update_catalog | role |


##### Output Table
| Type | Name |
|------|------|
| fact | session_id |
| fact | subscription_id |
| fact | current_status |


### Dependencies
------------
This role uses the following jinja2 templates included with the role:
  get_form_id.j2
  get_status.j2
  login.j2
  update_status.j2

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
        name: ansible-role_sc-close-ticket
      vars:
        sc_close_ticket_api_base_url:
        sc_close_ticket_api_username:
        sc_close_ticket_api_password:
        sc_close_ticket_request_item_id:
        sc_close_ticket_status_code:
```
### License
-------

All rights reserved. BlueCross BlueShield of Tennessee, Inc.

### Author Information
------------------

William Collins

John Kennedy
