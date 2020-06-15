Role Name
=========

This role applies a generic baseline to a base kickstart RHEL7 (or CentOS7) host.

Requirements
------------



Role Variables
--------------

* `ntp_client`: NTP client to install (chrony/ntpd). Default is chrony
* `ntpservers`: List of upstream NTP servers to configure.
* `system`: Name of the system the host belongs to for use in MOTD. Default is Unknown
* `sys_env`: Environment the host is in (e.g. Prod/QA/Test) for use in MOTD. Default is Unknown
* `role`: Role of this host for use in MOTD. Default is Unknown

Dependencies
------------

None.

Example Playbook
----------------

    ---
    - hosts: servers
      tasks:
      - include_role:
          name: role_generic_os
        vars:
          system: FANCYPANTS

License
-------

GPL3

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
