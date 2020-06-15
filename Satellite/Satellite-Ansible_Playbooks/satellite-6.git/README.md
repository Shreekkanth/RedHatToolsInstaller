Role Name
=========

This is a satellite 6 installation that includes a DHCP server with dynamic dns updating set. The DHCP server also sets up pxe

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

## satellite-6 ##
rndc-key-file: rndc.key
rndc-key-name: rndc-satellite-hss
rndc-key-secret: ""
subs-mgr-username: ""
subs-mgr-password: ""

##dhcp##


Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

MIT

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).

TODO
====
- create redhat.repo for RHEL 7.1
- use RH subscription mgr
- setup repo or use common/repos or rhn satelite for epel access
- test comment
