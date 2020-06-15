role_ntpserver
=========

This role applies an NTP server function to a RHEL7 (or CentOS7) host.

Requirements
------------

A baseline kickstart or templated installation must have been performed on the host(s) being hardened
and accounts to provide sudo access must be accessible.

Role Variables
--------------

* `ntpservers`: List of upstream NTP servers to configure (list, optional)
      Default is:
        - 0.rhel.pool.ntp.org
        - 1.rhel.pool.ntp.org
        - 2.rhel.pool.ntp.org


Dependencies
------------

None.

Example Playbook
----------------

    ---
    - hosts: ntpservers
      tasks:
      - include_role:
          name: role_ntpserver


License
-------

GPL3

Author Information
------------------

Geoff Gatward, Red Hat
