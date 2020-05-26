# AIDE IDS installation and configuration

Adds an AIDE IDS service to your project.

## Requirements

None. The required packages are managed by the role.

## Role Variables

- From `defaults/main.yml`

```yml
security_aide_exclude_dirs:
  - /opt
  - /run
  - /var
# Set the package install state for distribution packages
# Options are 'present' and 'latest'
security_package_state: present
# Initialize the AIDE database immediately (may take time).
security_rhel7_initialize_aide: 'no'                         # V-71973
```

- From `vars/main.yml`

```yml
aide_cron_job_path: /etc/cron.d/aide
aide_database_file: /var/lib/aide/aide.db.gz

# RHEL 7 STIG: Packages to add/remove
stig_packages_rhel7:
  - packages:
      - aide
    state: "{{ security_package_state }}"
    enabled: 'True'
```

## Dependencies

This role depends on `ansible-os-hardening-selinux`.

## Example Playbook

Example of how to use this role:

```yml
    - hosts: servers
      roles:
         - { role: ansible-os-hardening-aide, security_rhel7_initialize_aide: 'yes' }
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
