# ansible-role-icingaweb2
install and configure icingaweb2

[![Build Status](https://travis-ci.org/chrnie/ansible-role-icingaweb2.svg?branch=master)](https://travis-ci.org/chrnie/ansible-role-icingaweb2)

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    icingaweb2_install_source: "git"

`git` for a git clone of https://github.com/icinga/icingaweb2, `package` installs icingaweb from the icinga2 repo.


## Dependencies

Icingaweb2 needs icinga2 and a working IDO


## Example Playbook
You can find an example playbook for testing purposes on https://github.com/chrnie/icinga2-vagrant-ansible

- hosts: icinga2_master
  roles:
    - chrnie.icingaweb2


## License

Apache License 2.0


## Author Information

Created in 2017 by Christoph Niemann, https://github.com/chrnie
Forked from https://github.com/mkayontour/icinga2-ansible/roles/common
