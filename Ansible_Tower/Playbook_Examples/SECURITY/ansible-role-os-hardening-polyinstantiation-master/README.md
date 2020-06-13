# Polyinstantiation

Adds the ability to enforce polyinstantiation of directories.
Default supported directories for polyinstantiation are `/home`, `/tmp`, and `/var/tmp`.

To find more about the motivation behind polyinstantiation:

- [Polyinstantiating /tmp and /var/tmp directories](https://access.redhat.com/blogs/766093/posts/3169121)
- [Improve security with polyinstantiation](https://www.ibm.com/developerworks/library/l-polyinstantiation/)
- [Polyinstantiation of directories in an SELinux system](http://www.coker.com.au/selinux/talks/sage-2006/PolyInstantiatedDirectories.html)
- [Role-based access control in SELinux](https://www.ibm.com/developerworks/linux/library/l-rbac-selinux/)

## Requirements

None.

## Role Variables

- From `defaults/main.yml`

```yml
# SELinux booleans required to activate polyinstantiation
security_rhel7_poly_sebooleans:
  - name: polyinstantiation_enabled
    enabled: 'True'
# TODO: document
security_rhel7_poly_dirs:
  - polydir: '/var/tmp'
    enabled: 'True'
    instance_prefix: '/tmp/.inst/var-tmp-$USER-'
    method: 'tmpdir'
    create: 'True'
    iscript: 'var-tmp'
    noinit: 'False'
    shared: 'False'
    mntopts: 'nodev,nosuid,noexec,rw'
    list_of_uids: ['root']
  - polydir: '/tmp'
    enabled: 'True'
    instance_prefix: '/tmp/.inst/tmp-$USER-'
    method: 'tmpdir'
    create: 'True'
    iscript: 'tmp'
    noinit: 'False'
    shared: 'False'
    mntopts: 'nodev,nosuid,noexec,rw'
    list_of_uids: ['root']
  - polydir: '$HOME'
    enabled: 'True'
    instance_prefix: '/home/.inst/home-$USER-'
    method: 'tmpdir'
    create: 'True'
    iscript: 'home'
    noinit: 'False'
    shared: 'False'
    mntopts: 'nodev,nosuid,noexec,ro'
    list_of_uids: ['root']
```

- From `vars/main.yml`

```yml
# Custom polyinstantiated directories.
# If you want to add more polyinstantiated, or modify the defaults, you need to
# override the whole dict from `defaults/main.yml`.
# Additionally, if you require an iscript, write a template for it.
# security_rhel7_poly_dirs:
#   - polydir: '/tmp'
#     enabled: 'True'
#     instance_prefix: '/tmp/.inst/tmp-$USER'
#     method: 'context'
#     create: 'True'
#     iscript: 'tmp'
#     noinit: 'False'
#     shared: 'False'
#     mntopts: 'nodev,nosuid,noexec,rw'
#     list_of_uids: ['root']
#   - polydir: '/var/tmp'
#     enabled: 'True'
#     instance_prefix: '/tmp/.inst/var-tmp-$USER'
#     method: 'context'
#     create: 'True'
#     iscript: 'var-tmp'
#     noinit: 'False'
#     shared: 'False'
#     mntopts: 'nodev,nosuid,noexec,rw'
#     list_of_uids: ['root']
#   - polydir: '$HOME'
#     enabled: 'True'
#     instance_prefix: '/home/.inst/home-$USER'
#     method: 'context'
#     create: 'True'
#     iscript: 'home'
#     noinit: 'False'
#     shared: 'False'
#     mntopts: 'nodev,nosuid,noexec,ro'
#     list_of_uids: ['root']
# Check namespace.conf(5) for more information about the possible options.
```

## Dependencies

This role requires the [SELinux role](https://github.devops.worldpay.local/DOCET/ansible-os-hardening-selinux) to be used for polyinstantiation
activaction and the [OpenSSH module](https://github.devops.worldpay.local/DOCET/ansible-os-hardening-sshd) to enforce polyinstantiation when the
entrypoint is an SSH connection.
Graphical desktops can also be confined, but this role focuses on servers, and
there is no provision to manage GDM or other DMs.

## Example Playbook

Example of how to use this role:

```yml
    - hosts: servers
      roles:
         - { role: ansible-os-hardening-selinux }
         - { role: ansible-os-hardening-polyinstantiation }
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
