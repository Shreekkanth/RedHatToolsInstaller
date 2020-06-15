# SELinux management

Enforces and configures SELinux.

## Requirements

None. Required packages are managed by the role.

## Role Variables

- From `defaults/main.yml`

```yml
## Linux Security Module (lsm)
# Set the package install state for distribution packages
# Options are 'present' and 'latest'
security_package_state: present
# SELinux policy
security_rhel7_selinux_policy: 'targeted'
# Enable SELinux on Red Hat/CentOS
security_rhel7_enable_linux_security_module: 'yes'             # V-71989 / V-71991
# Ensure SEtroubleshoot is absent
security_rhel7_remove_setroubleshoot: 'yes'
# SELinux booleans.
security_rhel7_selinux_booleans:
# Allow system cron jobs to relabel filesystem for restoring file contexts.
  - name: cron_can_relabel
    enabled: 'False'
# Allow system cronjob to be executed on on NFS, CIFS or FUSE filesystem.
  - name: cron_system_cronjob_use_shares
    enabled: 'False'
# Determine whether crond can execute jobs in the user domain as opposed to the
# generic cronjob domain.
  - name: cron_userdomain_transition
    enabled: 'False'
# SELinux booleans required to prevent different seusers from executing
# content in their homes, for the purposes of protecting the restricted shell.
  - name: guest_exec_content
    enabled: 'False'
  - name: staff_exec_content
    enabled: 'True'
  - name: user_exec_content
    enabled: 'False'
# SELinux booleans required to prevent daemons from leaking information through
# coredumps
  - name: daemons_dump_core
    enabled: 'False'
# If you want to deny user domains applications to map a memory region as both
# executable and writable (this is dangerous and the executable should be
# reported) you must turn this boolean on.
  - name: deny_execmem
    enabled: 'True'
# SELinux booleans required to prevent users and processes from leaking
# information using tracing capabilities. Cripples 'strace', 'top' and other
# tools.
  - name: deny_ptrace
    enabled: 'True'
# SELinux booleans required to activate FIPS mode
# https://en.wikipedia.org/wiki/Federal_Information_Processing_Standards
  - name: fips_mode
    enabled: 'True'
# SELinux booleans required to allow logins directly on consoles
  - name: login_console_enabled
    enabled: 'True'
# To control the ability to mmap a low area of the address space, as configured by
# /proc/sys/vm/mmap_min_addr, you must turn on the mmap_low_allowed boolean.
# Disabled by default.
  - name: mmap_low_allowed
    enabled: 'False'
# SELinux booleans required to lock down the system in such a way that
# you can not change the SELinux settings on the box.
# Disallow programs, such as newrole, from transitioning to administrative user
# domains.
#  - name: secure_mode
#    enabled: 'True'
# Disable kernel module loading.
#  - name: secure_mode_insmod
#    enabled: 'True'
# Boolean to determine whether the system permits loading policy, setting enforcing
# mode, and changing boolean values. Set this to true and you have to reboot to
# set it back.
#  - name: secure_mode_policyload
#    enabled: 'True'
# If you want to allow unconfined executables to make their heap memory
# executable.  Doing this is a **really bad idea**. Probably indicates a badly
# coded executable, but could indicate an attack. This executable should be
# reported. Disabled by default.
  - name: selinuxuser_execheap
    enabled: 'False'
# Allow all unconfined executables to use libraries requiring text relocation that
# are not labeled textrel_shlib_t
  - name: selinuxuser_execmod
    enabled: 'False'
# If you want to allow unconfined executables to make their stack executable.
# **This should never, ever be necessary**. Probably indicates a badly coded
# executable, but could indicate an attack. This executable should be reported.
# Enabled by default.
  - name: selinuxuser_execstack
    enabled: 'False'
# Allow user to r/w files on filesystems that do not have extended attributes
# (FAT, CDROM, FLOPPY)
  - name: selinuxuser_rw_noexattrfile
    enabled: 'False'
# Allow users to run TCP servers (bind to ports and accept connection from the
# same domain and outside users)  disabling this forces FTP passive mode and may
# change other protocols.
  - name: selinuxuser_tcp_server
    enabled: 'False'
# Allow users to run UDP servers (bind to ports and accept connection from the
# same domain and outside users)  disabling this may break avahi discovering
# services on the network and other udp related services.
  - name: selinuxuser_udp_server
    enabled: 'False'
# Allow user  to use ssh chroot environment.
  - name: selinuxuser_use_ssh_chroot
    enabled: 'True'
# Manage SELinux related services
security_rhel7_selinux_services:
  - name: setroubleshoot
    enabled: 'False'
  - name: mcstrans
    enabled: 'False'
  - name: restorecond
    enabled: 'True'
```

- From `vars/main.yml`

```yml
# RHEL 7 STIG: Packages to add/remove
stig_packages_rhel7:
  - packages:
      - libselinux-python
      - policycoreutils-python
      - policycoreutils-restorecond
      - selinux-policy
      - selinux-policy-targeted
    state: "{{ security_package_state }}"
    enabled: "{{ security_rhel7_enable_linux_security_module }}"
  - packages:
      - setroubleshoot
      - setroubleshoot-server
      - setroubleshoot-plugins
    state: absent
    enabled: "{{ security_rhel7_remove_setroubleshoot }}"
# Custom SELinux booleans.
# Dictionary with the following structure:
#
# custom_selinux_booleans:
#   - name: auditadm_exec_content
#     enabled: 'True'
#   - name: dbadm_exec_content
#     enabled: 'True'
#   - name: logadm_exec_content
#     enabled: 'True'
#   - name: secadm_exec_content
#     enabled: 'True'
#   - name: sysadm_exec_content
#     enabled: 'True'
#   - name: xguest_exec_content
#     enabled: 'False'
custom_selinux_booleans: {}
#
# Custom SELinux services.
# Dictionary with the following structure:
#
# custom_selinux_services:
#   - name: foo
#     enabled: 'True'
custom_selinux_services: {}
```

## Dependencies

None.

## Example Playbook

Example of how to use this role:

```yml
    - hosts: servers
      roles:
         - { role: ansible-os-hardening-selinux }
```

## Contributing

This repository uses [git-flow](http://nvie.com/posts/a-successful-git-branching-model/).
To contribute to the role, create a new feature branch (`feature/foo_bar_baz`),
write [Molecule](http://molecule.readthedocs.io/en/master/index.html) tests for the new functionality
and submit a pull request targeting the `develop` branch.

Happy hacking!

## License

GPLv3

## Author Information

[David Sastre](david.sastre@redhat.com)
