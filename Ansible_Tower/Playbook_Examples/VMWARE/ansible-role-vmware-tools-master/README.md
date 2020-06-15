# ahuffman.vmware-tools
An Ansible role to mount, unmount, or upgrade VMWare tools.

## Variables
| Variable Name | Required | Description | Default Value | Type |
| --- | :---: | --- | :---: | :---: |
| vctr_user | yes | Username of the vCenter user with privileges to mount/unmount/upgrade VMware tools.| "" | string |
| vctr_pass | yes | Password of the vCenter user | "" | string |
| vctr_hostname | yes | hostname of the vCenter | "" | string |
| vctr_datacenter | yes | name of the vCenter datacenter | "" | string |
| vctr_validate_certs | yes | Validate the vCenter's certificate | True | boolean |
| vctr_vm_name | yes | Name of the virtual machine to mount/unmount/upgrade VMWare tools on. | "" | string |
| vctr_vm_folder | yes | Name of the virtual machine folder that the virtual machine resides in | "" | string |

## Playbook Examples
### Mount VMWare Tools Example
```yaml
---
- name: "Mount VMWare Tools"
  hosts: "localhost"
  vars_files:
    - "vars/mysecrets.yml"
  tasks:
    - name: "Mount VMWare Tools"
      include_role:
        name: "vmware-tools"
        tasks_from: "mount"
      vars:
        vctr_user: "admin"
        vctr_pass: "{{ from_vault }}"
        vctr_hostname: "my.vcenter.server.com"
        vctr_validate_certs: False
        vctr_datacenter: "My Datacenter"
        vctr_vm_folder: "Linux"
        vctr_vm_name: "my-new-vm-server"
```
### Unmount VMWare Tools Example
```yaml
---
- name: "Unmount VMWare Tools"
  hosts: "localhost"
  vars_files:
    - "vars/mysecrets.yml"
  tasks:
    - name: "Unmount VMWare Tools"
      include_role:
        name: "vmware-tools"
        tasks_from: "unmount"
      vars:
        vctr_user: "admin"
        vctr_pass: "{{ from_vault }}"
        vctr_hostname: "my.vcenter.server.com"
        vctr_validate_certs: False
        vctr_datacenter: "My Datacenter"
        vctr_vm_folder: "Linux"
        vctr_vm_name: "my-new-vm-server"
```
### Upgrade VMWare Tools Example
```yaml
---
- name: "Upgrade VMWare Tools"
  hosts: "localhost"
  vars_files:
    - "vars/mysecrets.yml"
  tasks:
    - name: "Upgrade VMWare Tools"
      include_role:
        name: "vmware-tools"
        tasks_from: "upgrade"
      vars:
        vctr_user: "admin"
        vctr_pass: "{{ from_vault }}"
        vctr_hostname: "my.vcenter.server.com"
        vctr_validate_certs: False
        vctr_datacenter: "My Datacenter"
        vctr_vm_folder: "Linux"
        vctr_vm_name: "my-new-vm-server"
```
