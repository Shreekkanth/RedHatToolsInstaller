# ClamAV antivirus

Adds a ClamAV antivirus service to your project.

[Note that](https://access.redhat.com/solutions/22007), at the time of this writing,
ClamAV is not supported or offered in Red Hat repositories.
However, many anti-virus solutions, including ClamAV, are available
from other vendors or via Extra Packages for Enterprise Linux (EPEL).

## Requirements

None. The required packages are managed by the role.

## Role Variables

- From `defaults/main.yml`

```yml

---
# Set the package install state for distribution packages
# Options are 'present' and 'latest'
security_package_state: present
# SELinux booleans required to allow ClamAV scan the system and use the JIT
security_rhel7_selinux_booleans_clamav:
  - name: antivirus_can_scan_system
    enabled: 'True'
  - name: antivirus_use_jit
    enabled: 'True'
# Enable virus scanning with clamav
security_enable_virus_scanner: 'yes'                            # V-72213
# Run the virus scanner update during the deployment (if scanner is deployed)
security_run_virus_scanner_update: 'yes'
```

- From `vars/main.yml`

```yml
clamav_proxy: ""
clamav_proxy_port: ""
clamav_proxy_user: ""
clamav_proxy_password: ""
clamav_service: 'clamd@scan'

# RHEL 7 STIG: Packages to add/remove
stig_packages_rhel7:
  - packages:
      - clamav
      - clamav-data
      - clamav-devel
      - clamav-filesystem
      - clamav-lib
      - clamav-scanner-systemd
      - clamav-server-systemd
      - clamav-server
      - clamav-update
    state: "{{ security_package_state }}"
    enabled: "{{ security_enable_virus_scanner }}"
```

## Dependencies

This role depends on `ansible-os-hardening-selinux` and `ansible-os-epel`.

## Example Playbook

Example of how to use this role:

```yml
    - hosts: servers
      roles:
         - { role: ansible-os-hardening-clamav }
```

## Contributing

This repository uses
[git-flow](http://nvie.com/posts/a-successful-git-branching-model/).
To contribute to the role, create a new feature branch (`feature/foo_bar_baz`),
write [Molecule](http://molecule.readthedocs.io/en/master/index.html) tests for
the new functionality
and submit a pull request targeting the `develop` branch.

Happy hacking!

## License

Apache 2.0

## Author Information

[David Sastre](david.sastre@redhat.com)
