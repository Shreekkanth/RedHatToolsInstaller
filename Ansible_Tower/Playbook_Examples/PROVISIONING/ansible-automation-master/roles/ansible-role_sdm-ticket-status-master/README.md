# CA Service Desk Manager Check Ticket Status

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
- name: Check ticket status of closed request
  include_role:
    name: ansible-role_sdm-ticket-status
  vars:
    sdm_ticket_status_api_base_url: "{{ ca_sdm_url }}"
    sdm_ticket_status_api_key: "{{ ca_sdm_key }}"
    sdm_ticket_status_ticket_id: "{{ closed_request_id }}"

- name: Check ticket status of open request
  include_role:
    name: ansible-role_sdm-ticket-status
  vars:
    sdm_ticket_status_api_base_url: "{{ ca_sdm_url }}"
    sdm_ticket_status_api_key: "{{ ca_sdm_key }}"
    sdm_ticket_status_ticket_id: "{{ open_request_id }}"

- name: Check ticket status of open request until closed
  include_role:
    name: ansible-role_sdm-ticket-status
  vars:
    sdm_ticket_status_api_base_url: "{{ ca_sdm_url }}"
    sdm_ticket_status_api_key: "{{ ca_sdm_key }}"
    sdm_ticket_status_ticket_id: "{{ open_request_id }}"
    sdm_ticket_status_wait: true
```
### License
-------

All rights reserved. BlueCross BlueShield of Tennessee, Inc.

### Author Information
------------------

William Collins

John Kennedy
