# satellite Register Role

## About

The role has to be executed with root permission, using the root user or via sudo because it will install packages and configure system

DNS resolution is verified during the execution, FQDN of all servers has to be resolved using DNS.

## Ansible Requirements

Minimun ansible version: **2.1** (Required by the **headers** parameter of the **uri** module)

Role has to be executed in a playbook with the gather_facts activated, because several facts will be obtained from the host

## Configuration parameters

### Required variables in the environment file

## Example playbook

```yml
---
- name: satelliteRegister
  hosts: <<host list>>
  remote_user: <<user>>
  gather_facts: true
  become: yes
  become_user: root
  become_method: sudo
  vars:
  roles:
    - satelliteRegister
```
