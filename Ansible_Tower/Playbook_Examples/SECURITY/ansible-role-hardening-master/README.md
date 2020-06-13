ansible-role-hardening
=========

This role applies a basic ISM compliant hardening baseline to a RHEL7 (or CentOS7) host.

Requirements
------------

A baseline kickstart or templated installation must have been performed on the host(s) being hardened
and accounts to provide sudo access must be accessible.

Role Variables
--------------

* `ssh_listen_address`: Address to listen on. Default is 0.0.0.0  (string, optional)
* `ssh_AddressFamily`: IP address family to use. Default is inet  (string, optional)
* `ssh_port`: Port that SSH listens on. Default is 22  (String, optional)
* `ssh_PermitRootLogin`: Permit root login (yes/no). Default is no  (boolean, optional)
* `ssh_MaxAuthTries`: Max number of login attempts. Default is 3  (integer, optional)
* `ssh_ClientAlive_Interval`: SSH Inactivity timeout. (integer, optional)
* `ssh_ClientAliveCountMax`: SSH Inactivity counter. Default is 0  (integer, optional)
* `ssh_Banner`: Location of login warning test. Default is /etc/issue  (string, optional)
* `ssh_HostKeyAlgorithms`: List of HostKeyAlgorithms to accept (client)  (string, optional)
* `ssh_KexAlgorithms`: List of SSH KexAlgorithms to allow  (string, optional)
* `ssh_Ciphers`: List of SSH Ciphers to allow  (string, optional)
* `ssh_MACs`: List of SSH MACs to allow  (string, optional)
* `ssh_LoginGraceTime`: SSH login grace time. Default is 60  (integer, optional)
* `ssh_AllowTcpForwarding`: Enable SSH TCP forwarding. Default is yes  (string, optional)
* `ssh_X11Forwarding`: Enable SSH X11 forwarding. Default is no  (string, optional)

* `kernel_exec_shield`: Default is 1  (integer, optional)
* `kernel_randomize_va_space`: Default is 2  (integer, optional)
* `fs_suid_dumpable`: Default is 0  (integer, optional)
* `net_ipv4_conf_all_forwarding`: Default is 0  (integer, optional)
* `net_ipv4_ip_forward`: Default is 0  (integer, optional)
* `net_ipv4_conf_default_send_redirects`: Default is 0  (integer, optional)
* `net_ipv4_conf_all_send_redirects`: Default is 0  (integer, optional)
* `net_ipv4_all_accept_source_route`: Default is 0  (integer, optional)
* `net_ipv4_all_accept_redirects`: Default is 0  (integer, optional)
* `net_ipv4_all_secure_redirects`: Default is 0  (integer, optional)
* `net_ipv4_all_log_martians`: Default is 0  (integer, optional)
* `net_ipv4_default_accept_source_route`: Default is 0  (integer, optional)
* `net_ipv4_default_accept_redirects`: Default is 0  (integer, optional)
* `net_ipv4_default_secure_redirects`: Default is 0  (integer, optional)
* `net_ipv4_icmp_echo_ignore_broadcasts`: Default is 1  (integer, optional)
* `net_ipv4_icmp_ignore_bogus_error_responses`: Default is 1  (integer, optional)
* `net_ipv4_tcp_syncookies`: Default is 1  (integer, optional)
* `net_ipv4_conf_all_rp_filter`: Default is 1  (integer, optional)
* `net_ipv4_conf_default_rp_filter`: Default is 1  (integer, optional)

* `auth_source`: Used in rendering of /etc/issue. Default is local, options LDAP/AD  (string, optional)

* `disable_ipv6`: Disable IPv6 from the system, per ISM requirements. Default is true  (boolean, optional)

Dependencies
------------

None

Example Playbook
----------------

  ---
  # site.yml
  # Role inclusion workflow

    - hosts: all
      tasks:
      - include_role:
          name: ansible-role-hardening
        vars:
          ssh_port: 2022
          ssh_permitRootLogin: no
          net_ipv4_conf_all_log_martians: 0


License
-------

GPL3

Author Information
------------------

Geoff Gatward
