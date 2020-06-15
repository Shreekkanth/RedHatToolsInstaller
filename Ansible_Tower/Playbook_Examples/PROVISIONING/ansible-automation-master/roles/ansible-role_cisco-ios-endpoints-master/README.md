# Cisco IOS Endpoints


Parses the output of the Cisco IOS command "show ip arp" to capture which switch a particular network device is connected to.

### Requirements
------------

This role uses the command-parser module.  Commound output parsing is done via the show_ip_arp.yml parser template included with the role.

### Role Variables
--------------

Variable Table

| Variable | Defined by |
|----------|------------|
| output   | output of ios command |
| parser output | command-parser module |
| cisco_ios_endpoint_location_ip | Playbook (optional) |
| cisco_ios_endpoint_location_mac | Playbook (optional) |

Output Table

| Type | Name | Description |
| ---- | ---- | ---- |
| fact | arp_entries | Single entry of matching interface if cisco_ios_endpoint_location_ip/cisco_ios_endpoint_location_mac is defined.  Otherwise, list of { ip, mac, interface} |
| fact | sanitized_mac |


### Dependencies
------------

This role imports the ansible-networ.network-engine role.
[https://galaxy.ansible.com/ansible-network/network-engine]

### Example Playbook
----------------

```
---
- hosts: localhost
  remote_user: root
  include role:
    - ansible-role_cisco_ios-endpoints
  
```
### License
-------

All rights reserved. BlueCross BlueShield of Tennessee, Inc.

### Author Information
------------------

William Collins

John Kennedy
