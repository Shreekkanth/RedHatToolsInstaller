VMWare Provisioning
=========

This role will read values defined in the configuration registry repository, and build a VM using those specifications.

Requirements
------------

* Server Definition in config_registry
* Extra Variable passed at runtime with a comma-separated list of VMs
* pyvmomi module installed

Role Variables
--------------

extra_vars:
|Variable name | Function|
|--------------|------------|
|new_vms|list of hostnames, passed at runtime. These must refer to hosts in the config registry.|


Most variables for this role are defined in config_registry. It's mandatory to run the pull-config role first, with the `config_registry_servers` parameter enabled.

Dependencies
------------

pull-config role

Example Playbook
----------------
```yaml
    - hosts: localhost
      roles:
        - role: pull-config
          config_registry_servers: True
          config_registry_apps: False
    - hosts: app-servers
      roles:
        - role: app-infra
```



Author Information
------------------

Mat Wilson <mawilson@redhat.com>
