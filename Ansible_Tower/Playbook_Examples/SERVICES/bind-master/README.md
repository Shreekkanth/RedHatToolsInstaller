bind
==================

`bind` configures a wildcard DNS entry for OpenShift.


Requirements
------------

`../roles/virt`

Role Variables
--------------

The following variables are not defined at `defaults/main.yml` by default.
They are referred from the inventory file.
* `public_domain`: ../../inventories/<inventory_file>
* `groups['infranode']`: ../../inventories/<inventory_file>
* `virt_networks['public']['cidr']`: ../../group_vars/ose

All the other necessary variables are defined at `defaults/main.yml`.

Dependencies
------------

No.

Example Playbook
----------------

```
---
# bind.yml
- hosts: host
  roles:
  - { role: bind }
```

License
-------

BSD

Author Information
------------------

Naoya Hashimoto <nhashimo@redhat.com>
