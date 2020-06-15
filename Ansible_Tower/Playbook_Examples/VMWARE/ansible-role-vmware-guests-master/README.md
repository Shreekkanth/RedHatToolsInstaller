VMWare Management Role
=========

Ansible Role to create and destroy virtual machines on a vSphere Infrastructure

Requirements
------------
The role has to be executed with root permission, using the root user or via sudo because it requires some packages from pip to be installed in the server where role is executed

Minimum ansible version required to run this role is 2.2

This Role is compatible with RHEL and SUSE.

- RHEL 7: **open-vm-tools** and **perl** rpm packages have to be installed and **vmtoolsd** daemon has to be started and enabled.

- RHEL 6: **VMWare Tools** has to be installed and started

Role Variables
--------------
`state`: Determine if `vm_name` has to be created or deleted (valid values are **present** or **absent**)

`use_ipam` (boolean): Use IPAM role to determine the networking configuration. If true, bluecat vars have to be defined.

`vc_hostname`: FQDN of the vCenter

`vc_username`: Username to connect vCenter

`vc_pwd`: Password to connect vCenter

`vc_datacenter`: Datacenter where is located the virtual machine

`vc_cluster`: Cluster where is located the virtual machine

`vc_folder`: Folder where is located the virtual machine

`vm_name`: Name of the virtual machine in the vCenter

`vm_datastore`: Datastore where is located the virtual machine

`vm_network`: Network where is located the virtual machine

`vm_templname`: Name of the template used to deploy the virtual machine

`vm_ip`: IP address assigned to the virtual machine

`vm_netmask`: Netmask assigned to the virtual machine

`vm_gateway`: Gateway of the network assigned to the virtual machine

Dependencies
------------

Example Playbook
----------------

    - hosts: all
      roles:
         - { role: ansible-role-vmware-guests }

Testing
--------
[Molecule](http://molecule.readthedocs.io/en/latest/) is the framework selected to implement automated tests.
- Components:
  - **molecule/default:** Name of the default scenario, which will execute the complete set of tests
  - **molecule/default/molecule.yml:** Configuration file. It includes the number of servers to deploy and the provider where to deploy them.
  - **molecule/default/tests/:** Tests to be executed on servers after the role execution.


- Examples:
  - **molecule test:** Executes the complete set of tests defined in the scenario.
  - **molecule syntax:** Only executes syntax checks on the role
  - **molecule verify:** Only executes tests on servers


- Default scenario:

When using default scenario, following tests will be executed:

    ├── lint          Yaml validator on role
    ├── destroy       Destroy testing servers
    ├── dependency    requirements.yml execution
    ├── syntax        Syntax checks
    ├── create        Create testing servers
    ├── prepare       Execute preparing playbooks (molecule/default/prepare.yml)
    ├── converge      Execute role on servers
    ├── idempotence   Check role idempotency on servers
    ├── side_effect   Check side effects on role
    ├── verify        Execute tests (molecule/default/tests/*) on servers
    └── destroy       Delete testing servers

License
-------

Copyright (c) 2018 F. Hoffmann-La Roche Ltd. All rights reserved.

Author Information
------------------

Developed by Roche Team @ F. Hoffmann-La Roche Ltd.
