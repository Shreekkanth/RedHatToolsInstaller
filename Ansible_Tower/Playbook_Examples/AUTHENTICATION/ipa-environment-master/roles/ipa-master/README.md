ipa-master
==========

ipa-master is designed for a view to provide a generic interface to ipa servers
rather then splitting the workflow between server and replica roles.

This role requires that any ipa server or replica is already instantiated
before this role can function correctly.

Supported Functions
-------------------
* cn=Config database maintenance


Example Playbook
----------------
As this role makes changes to the cn=Config database it is recommended that the
role be ran with `serial` to ensure directory services continuity during
restarts.

```yaml
- hosts: ipa-masters
  serial: 1
  roles:
    - role: ipa-master
      ipa_master_ds_secret: "{{ ipa_master_ds_secret }}"
```

License
-------

LGPL

Author Information
------------------

Devil Horn project

maintainer: tbd@tbd.com

JIRA: https://redhat-anzservices.atlassian.net/secure/RapidBoard.jspa?rapidView=7
