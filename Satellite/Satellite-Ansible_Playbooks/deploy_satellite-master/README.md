Deploy satellite
=================

This role installs and configures satellite.

Note: This file needs a lot of updating.  Please go through the code before use.

Requirements
------------

1) Ansible server/jump box (version 2.1+ recommended). This is the server from which all playbooks will be run.

Dependencies
------------
A "common" role that will add repository sources to the target server, i.e. my "common" role.

Role Variables
--------------

All variables used by this role are listed under defaults/main.yml. It is recommended that users do not change defaults/main.yml directly and instead control variables fia the files under group_vars/all/satellite.yml.

Vairalbe List
-------------



Dependencies
------------

None

Example Playbook
----------------

```
- name: Run satellite Configuration Playbook
  hosts: tag_app_satellite
  become: yes
  become_flags: -i
  roles:
    - { role: deploy_satellite, when: deploy_satellite }
```

License
--------
MIT

Author Information
------------------
Matthew Bach (mbach@redhat.com)   
Lester Claudio (claudiol@redhat.com)  
Glenn Snead (glennsnead@gmail.com)  
Josh Springer (jspringe@redhat.com)  
Carolyn Thiel (cthiel@redhat.com) 
