# Cisco IOS Get Ports


Parses the output of the Cisco IOS commands "show interfaces" and "show macro auto interface" to capture which ports are available on a particular network device.
Must supply one of the optional variables to match search.

### Requirements
------------

This role uses the command-parser module.  Command output parsing is done via the show_interfaces.yml and show_macro_auto_interface.yml parser templates included with the role.

### Role Variables
--------------

##### Variable Table

| Variable | Defined by |
|----------|------------|
| output   | output of ios commands |
| macro_info | command_parser module |
| interface_info | command_parser module |
| cisco_ios_get_ports_interface_type | Interface type to match (optional) |
| cisco_ios_get_ports_available_only | True if only match available port (optional) |
| cisco_ios_get_ports_name | Name of port to match (optional) |

##### Output Table

| Type | Name |
| ---- | ---- |
| fact | macro_details |
| fact | cisco_ports |
| fact | cisco_ios_get_ports.ports |


### Dependencies
------------

This role imports the ansible-networ.network-engine role.
[https://galaxy.ansible.com/ansible-network/network-engine]

### Example Playbook
----------------

```
---
- hosts: cisco
  gather_facts: false
  connection: network_cli
  vars:
    test_port: GigabitEthernet1/38

  tasks:
    - name: Get details of a specific port
      include_role:
        name: cisco_ios_get_ports
      vars:
        cisco_ios_get_ports_name: "{{ test_port }}"

    - name: Show return value for single-port query
      debug:
        var: cisco_ios_get_ports
```
### License
-------

All rights reserved. BlueCross BlueShield of Tennessee, Inc.

### Author Information
------------------

William Collins

John Kennedy
