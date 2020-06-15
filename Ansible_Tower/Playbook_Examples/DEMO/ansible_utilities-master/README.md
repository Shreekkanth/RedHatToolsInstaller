# DOMino Utility Playbooks

## idm_register

### Usage

### Requirements

### Variables

## register_sat6

### Usage

### Requirements

### Variables

## push_ssh_keys

This playbook will add the public key found in `files/{{ key_name }}` to the remote systems specified in the inventory. This is done so that Ansible can authenticate to these systems in the future using keys instead of passwords.

### Usage

This playbook is meant to be run from Ansible Tower, because it requires a machine credential that will have a machine password so that Ansible can authenticate to the systems before the SSH key is added.

### Requirements

- An SSH key has been generated using a command such as `ssh-keygen -t rsa` and placed in files/. It should be created using a password so that the private key can be kept in source control. Keeping the private key in source control ensures that it can be add to authenticate to future systems.

### Variables

- `key_name`: the name of the public key to be pushed out to the remote systems
- `user`: the name of the user that the key should be added to
