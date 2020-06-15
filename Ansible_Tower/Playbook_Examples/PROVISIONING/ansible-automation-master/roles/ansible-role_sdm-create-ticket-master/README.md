# CA Service Desk Manager Create Ticket

1. Get sdm authentication key
2. Get requestor account UUID
3. Create ticket
4. Delete authentication key

### Requirements
------------

### Role Variables
--------------

##### Variable Table

| Variable | Defined by |
|----------|------------|
| sdm_create_ticket_api_base_url | defaults |
| sdm_create_ticket_api_key | defaults |
| sdm_create_ticket_requestor_id | defaults |
| sdm_create_ticket_description | defaults |
| sdm_create_ticket_summary | defaults |
| sdm_create_ticket_ci | defaults |
| sdm_create_ticket_fds_category | defaults |
| auth_key_result | role |
| user_id_result | role |
| create_ticket_result | role |
| delete_access_key_result | role |

##### Output Table
| Type | Name |
|------|------|
| fact | session_id |
| fact | subscription_id |
| fact | current_status |


### Dependencies
------------
This role uses the following jinja2 templates included with the role:
  create_request.j2

### Example Playbook
----------------

```
---
- name: Include sdm_create_ticket role
  include_role:
    name: ansible-role_sdm-create-ticket
  vars:
    sdm_create_ticket_api_base_url: "{{ ca_sdm_url }}"
    sdm_create_ticket_api_key: "{{ ca_sdm_key }}"
    sdm_create_ticket_requestor_id:
    sdm_create_ticket_description: 
    sdm_create_ticket_summary: DNS Request
    sdm_create_ticket_ci:
    sdm_create_ticket_fds_category: Catalog.Servers.Linux.DNSRecord.Create

- name: Output raw result
  debug:
    var: sdm_create_ticket.raw_result
```
### License
-------

All rights reserved. BlueCross BlueShield of Tennessee, Inc.

### Author Information
------------------

William Collins

John Kennedy
