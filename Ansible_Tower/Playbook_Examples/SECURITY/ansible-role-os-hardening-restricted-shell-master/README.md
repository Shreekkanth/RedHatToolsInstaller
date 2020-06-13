# Restricted shell

Adds the ability to enforce the use of a restricted shell for local accounts.

To find more about the motivation behind restricted shells and potential
pitfalls:

- [Escape from Shellcatraz](https://speakerdeck.com/knaps/escape-from-shellcatraz-breaking-out-of-restricted-unix-shells)
- [Escaping Restricted Linux Shells](https://pen-testing.sans.org/blog/pen-testing/2012/06/06/escaping-restricted-linux-shells)
- [Breaking out of rbash using scp](http://pentestmonkey.net/blog/rbash-scp)

## Requirements

None. The required packages are managed by the role.

## Role Variables

- From `defaults/main.yml`

```yml
# Restricted shell
# Activate/deactivate restricted shell.
security_rhel7_rbash_enabled: 'True'
# SELinux booleans required to prevent user_t and staff_t types from executing
# content in their homes, for the purposes of protecting the restricted shell.
security_rhel7_rbash_sebooleans:
  - name: user_exec_content
    enabled: 'True'
  - name: staff_exec_content
    enabled: 'True'
# TODO: document
# FIXME: enforce only 'present' links
security_rhel7_rbash_binaries:
  - name: clear
    state: 'present'
  - name: sudo
    state: 'present'
  - name: sudoedit
    state: 'present'
  - name: rvim
    state: 'absent'
  - name: rview
    state: 'present'
  - name: less
    state: 'present'
  - name: passwd
    state: 'present'
  - name: awk
    state: 'absent'
  - name: elinks
    state: 'absent'
  - name: scp
    state: 'absent'
  - name: ftp
    state: 'absent'
  - name: python
    state: 'absent'
  - name: perl
    state: 'absent'
#TODO: add more commands with evident shell escapes
# ftp, gdb, more, less (but see LESSSECURE), man, rvim, scp, find
# any scripting language: ruby, perl, python, lua, awk, ...
# Provide the restricted shell with all the coreutils
security_rhel7_rbash_coreutils: 'False'
# Minimum UID numeric value to apply security constraints to. By default,
# all non system accounts.
security_rhel7_min_uid: 1000
```

- From `vars/main.yml`

```yml
---
# TODO: document security implications
rbash_custom_binaries: {}
```

## Dependencies

This role depends on `ansible-os-hardening-selinux` for a more effective confinement
of unprivileged users.
Read [why](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/SELinux_Users_and_Administrators_Guide/sect-Security-Enhanced_Linux-Confining_Users-Booleans_for_Users_Executing_Applications.html).

## Example Playbook

Example of how to use this role:

```yml
    - hosts: servers
      roles:
         - { role: ansible-os-hardening-selinux }
         - { role: ansible-os-hardening-restricted-shell }
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
