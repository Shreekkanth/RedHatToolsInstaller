# RPM related STIG checks

Performs all packaging related STIG checks, such as:

- Verify all installed RPM packages
- Ensure RPM verification task has finished
- Get files with invalid checksums
- The cryptographic hash of system files and commands must match vendor values
- Require digital signatures for all packages
- Clean requirements/dependencies when removing packages
- Get packages with incorrect file permissions or ownership
- Reset file permissions/ownership to vendor values

## Requirements

None. The required packages are managed by the role.

## Role Variables

- From `defaults/main.yml`

```yml
security_enable_gpgcheck_repo: yes                            # V-71981
```

- From `vars/main.yml`

```yml
pkg_mgr_config: "{{ (ansible_pkg_mgr == 'yum') | ternary('/etc/yum.conf', '/etc/dnf/dnf.conf') }}"
rpm_gpgchecks:
  - regexp: "^gpgcheck.*"
    line: "gpgcheck={{ security_enable_gpgcheck_packages | bool | ternary('1', 0) }}"
  - regexp: "^localpkg_gpgcheck.*"
    line: "localpkg_gpgcheck={{ security_enable_gpgcheck_packages_local | bool | ternary('1', 0) }}"
  - regexp: "^repo_gpgcheck.*"
    line: "repo_gpgcheck={{ security_enable_gpgcheck_repo | bool | ternary('1', 0) }}"
```

## Dependencies

None.

## Example Playbook

Example of how to use this role:

```yml
    - hosts: servers
      roles:
         - { role: ansible-os-hardening-rpm }
```

## Contributing

This repository uses [git-flow](http://nvie.com/posts/a-successful-git-branching-model/).
To contribute to the role, create a new feature branch (`feature/foo_bar_baz`),
write [Molecule](http://molecule.readthedocs.io/en/master/index.html) tests for the new functionality
and submit a pull request targeting the `develop` branch.

Happy hacking!

## License

Apache 2.0, as this work is derived from [OpenStack's ansible-hardening role](https://github.com/openstack/ansible-hardening).

## Author Information

[David Sastre](david.sastre@redhat.com)
