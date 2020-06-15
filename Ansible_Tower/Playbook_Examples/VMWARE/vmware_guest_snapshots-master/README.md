[![pipeline status](https://gitlab.consulting.redhat.com/iag/ansible/roles/vmware_guest_snapshots/badges/master/pipeline.svg)](https://gitlab.consulting.redhat.com/iag/ansible/roles/vmware_guest_snapshots/commits/master)

vmware_guest_snapshots
=========

Creates, deletes, updates VM snapshots on VMware systems.

This role uses Molecule for testing.

Molecule has been configured with custom cleanup and prepare steps to ensure that a test vmware snapshot is removed before and after the the molecule testing.



Requirements
------------

Requires python module 'pyvmomi' to be installed in the ansible python environment of the Ansible control node, for Ansible Tower this module should be installed into the Ansible virtual environment `/var/lib/awx/venv/ansible/`.

Role Variables
--------------

- `vm_name` is the hostname of the virtual machine. This name is expected to be provided as a FQDN. It should be a string.
- `vm_snapshot_state` is the desired state of the snapshot. Default value is `present`.
  - If set to `present` and a snapshot with the same name exists, it will be updated. 
  - If set to `present` and does not exist, it will be created. 
  - If set to `absent` the snapshot with the name will be deleted.
- `vm_datacenter` is the vCenter datacenter which the guest exists in.
- `vm_datacenter2` is the 2nd vCenter datacenter which the guest exists in.
- `vm_snapshot_name`: is the name of the snapshot which should be `present` or `absent` on the vm. Default value is `Ansible_Snapshot`
- `vm_snapshot_description` is the description field on the snapshot. Default value is `Created by Ansible Tower`
- `vm_hostname` is the fqdn/ip of the vCenter/ESX server for the vm.
- `vm_hostname2` is the fqdn/ip of a 2nd vCenter/ESX server for the vm.
- `vm_hostname_password` is the password to connect to the `vm_hostname`. This should be encrypted with ansible-vault or collected using 'Surveys' in Ansible Tower or a suitable feature.
- `vm_hostname_username` is the username to connect to the `vm_hostname`.
- `vm_hostname_validate_certs` defines whether to validate the - `vm_hostname` certificate or not. Default is 'no'.
- `vm_hostname_port` is the port to connect to on `vm_hostname`. Default is 443.


Dependencies
------------

Nil.

Example Playbook
----------------

```yaml
    - hosts: servers
      vars:
        vm_name: myvm.domain.local
        vm_snapshot_state: present
        vm_datacenter: prod
        vm_hostname: esx01.prod.local
        vm_hostname_password: secureme
        vm_hostname_username: johndoe
        vm_hostname_validate_certs: yes
      roles:
         - { role: vmware_guest_snapshots }
```
License
-------

BSD

Author Information
------------------

Blake Douglas, Red Hat, blake@redhat.com
