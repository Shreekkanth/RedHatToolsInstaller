# ansible-role-localpackages
Ansible Role for Local Package Installation

Role Name
=========

A simple local package installer for a lab environment

Requirements
------------

Utilises 'synchronize' package, thus requires rsync on the remote host. The role takes care of it, if it is not there.
Hastens the play if it just does a check for the files are alreay on the remote host.

All the .rpm files are located in the 

    <role>/files/rpm/<package name>/*.rpm


Role Variables
--------------

The only variables that are required are the following

```
---
packages:
  <packagename_1>:
      - <remote location of the file 1>
      - <remote location of the file 2>
      - <remote location of the file 3>
  <packagename_2>:
      - <remote location of the file A>
      - <remote location of the file B>

...
```

Example Vars File - `<role>/vars/v_redhat.yml`
----------------
```
packages:
  rsync:
    - /var/run/rpm/rsync/rsync-3.1.2-6.el7_6.1.x86_64.rpm
  nextpackage:
    - /var/run/rpm/nextpackage/nextpackage-1.1.1-6.el7_6.1.x86_64.rpm
  otherpackage:
    - /var/run/rpm/otherpackage/otherpackage-2.2.2-6.el7_6.1.x86_64.rpm
```
Example Playbook
----------------
```
- name: "Setup Remote Host from Base Build Image"
  hosts: "{{ variable_host | default('all') }}"
  become: yes

  roles:
    - { role: localpackages }
```
License
-------

MIT

Author Information
------------------

@PhatScripts
