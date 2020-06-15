# First Boot Role

## About

The role has to be executed with root permission, using the root user or via sudo because it will install packages and configure system

DNS resolution is verified during the execution, FQDN of all servers has to be resolved using DNS.

## Ansible Requirements

Minimun ansible version: **2.1** (Required by the **headers** parameter of the **uri** module)

Role has to be executed in a playbook with the gather_facts activated, because several facts will be obtained from the host

### DNS Lookup plugin

The role uses the **dns lookup plugin** to verify that hostname can be resolved on dns before start the installation of the server.

It requires that the **python-dns** package to be installed in the server running this ansible role

## Configuration parameters

### Required variables in the environment file

## Example playbook

```yml
---
- name: First boot role
  hosts: <<host list>>
  remote_user: <<user>>
  gather_facts: true
  become: yes
  become_user: root
  become_method: sudo
  vars:
  roles:
    - firstBoot
```
