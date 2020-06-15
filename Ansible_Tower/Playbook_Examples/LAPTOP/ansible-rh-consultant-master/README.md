Role Name
=========

General laptop setup for RH network usage when not using the RH CSB.

Requirements
------------

Ansible to be installed...

Role Variables
--------------

Check the defaults/main.yml

Dependencies
------------

NIL

Example Playbook
----------------

```yaml
---
- name: setup a consultant's laptop
  hosts: localhost
  connection: local
  become: true

  roles:
    - role: ansible-rh-consultant
```

Then execute the playbook with something like the following, to prompt for SUDO password:
```
ansible-playbook -K consultant.yml
```
  
License
-------

MIT (Unless otherwise stated...)

Author Information
------------------

Originally authored by Ben Lewis.
Turned into a role by Ben Colby-Sexton.
 
