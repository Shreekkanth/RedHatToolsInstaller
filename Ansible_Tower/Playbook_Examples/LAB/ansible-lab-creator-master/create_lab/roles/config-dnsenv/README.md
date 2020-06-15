Role Name
=========

This role configures IdM DNS records

## Requirements
The IdM config role requires that IDM DNS be fully functional

## Dependencies

None

## Optional Vars


### Example Inventory

```
[all:vars]
idm_record_state=present
idm_server=idmserver.address.orhostname
idm_password=password
domain_name=example.com


[idm]
idm1.test.lab
```
### Example Playbook
```
- hosts: idm
  become: yes

  roles:
    - idm

```

License
-------

Apache License 2.0


Author Information
------------------

Red Hat Community of Practice & staff of the Red Hat Open Innovation Labs.
