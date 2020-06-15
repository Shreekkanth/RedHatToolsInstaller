# IPA Installation Role

## About

The role has to be executed with root permission, using the root user or via sudo because it will install packages and configure system

This role will install IdM on the server, as **master** or as **replica**, depending of a variable assigned to each host, for example:

```yml
[ipa-servers]
	10.0.0.10	masterserver=True
	10.0.0.11	masterserver=False
	10.0.0.12	masterserver=False
```

Replica set has to be configured after installing the replica server.

Master server has to be installed before installing the replicas.

Different replicas can be installed at the same time, if any server in the inventory is already installed, role will not modify it.

DNS resolution is verified before install. FQDN of all servers has to be resolved using DNS.

New user is created to register new servers. New idm role is created with Host Enrollement privileges adding privilege to "System: Add Hosts"

New group and password policy without expiration is created. **Admin** and enroller users are assigned to that group.

## Ansible Requirements

rhel-7-server-rpms repo has to available and enabled to install ipa packages

Role has to be executed in a playbook with the gather_facts activated, because hostname will be obtained from the {{ansible_fqdn}} fact

### DNS Lookup plugin

The role uses the **dns lookup plugin** to verify that hostname can be resolved on dns before start the installation of the server.

It requires that the **python-dns** package to be installed in the server running ansible.

## Configuration parameters

### Required variables in the environment file

Country variables has to be created in the environment file. The role will use them, and they don't have any default value:

- `ipa_server`: IPA Server used on replica installation to sync to.
- `ipa_domain`: Domain name to create.
- `dspassword`: Directory Manager admin password
- `adminpassword`: IdM admin password
- `register_username`: ID of the user created to register new servers
- `register_password`: Register user password
- `passwordpolicy_name`: Name of the group and the non expiring password policy

## Example playbook

```yml
---
- name: IdM Installation
  hosts: <<host list>>
  remote_user: <<user>>
  gather_facts: true
  become: yes
  become_user: root
  become_method: sudo
  vars:
    dspassword: "{{ lookup('vault', '{{ dspassword_key }}', 'value', 'None', '{{ vault_server }}', 'token', 'None', 'None', '{{ vault_read_token }}') }}"
    adminpassword: "{{ lookup('vault', '{{ adminpassword_key }}', 'value', 'None', '{{ vault_server }}', 'token', 'None', 'None', '{{ vault_read_token }}') }}"
    register_password: "{{ lookup('vault', '{{ register_password_key }}', 'value', 'None', '{{ vault_server }}', 'token', 'None', 'None', '{{ vault_read_token }}') }}"
    ipa_server: 'ipa-server.example.com'
    ipa_domain: 'example.com'
    register_username: 'enroller'
    passwordpolicy_name: 'serviceaccounts'
  roles:
    - ansible-ipaInstaller
```
