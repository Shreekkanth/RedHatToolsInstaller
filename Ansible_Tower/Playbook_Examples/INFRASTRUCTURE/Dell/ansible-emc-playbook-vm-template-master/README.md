# EMC VM Template
## Description
This repository contains playbooks to achieve the following:
  * Build a `bios` based RHEL7 virtual machine by utilizing a custom kickstart boot ISO
  * Build a `efi` based bios-rom RHEL7 virtual machine by utilizing a custom kickstart boot ISO
  * Destroy (delete) a virtual machine/template
  * Remove (delete) a vCenter virtual machine folder  

VM template provisioning is completed via another internal EMC process.

## Playbooks
| Playbook Name | File Name | Description | Documentation |
| --- | :---: | --- | :---: |
| Build EMC VM Template | [build-emc-vm-template.yml](build-emc-vm-template.yml) | An Ansible playbook to build EMC's bios or efi based VM Template. | [Doc](docs/build-emc-vm-template.md) |
| Destroy EMC VM Template | [destroy-emc-vm-template.yml](destroy-emc-vm-template.yml) | An Ansible playbook to power off and delete a VM from disk in vCenter. | [Doc](docs/destroy-emc-vm-template.md) |
| Remove VM Folder | [remove-vm-folder.yml](remove-vm-folder.yml) | An Ansible playbook to delete/remove a VM folder in vSphere. | [Doc](docs/remove-vm-folder.md) |
