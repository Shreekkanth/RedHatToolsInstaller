# Destroy EMC VM Template Playbook
## Description
An Ansible playbook to power off and delete a VM from disk in vCenter.

* The variables that affect this playbook are found in [vars](vars), and are in the naming convention of emc-vm-template-**[datacenter name]**, where the `datacenter name` must match the name passed from the playbook prompt for vSphere data-center.  

## Playbook Filename
[destroy-emc-vm-template.yml](destroy-emc-vm-template.yml)
## Tags Available
N/A
## Process Details
The playbook begins the process by prompting the end-user for a data-center, their vSphere username and password, and the name of the VM to remove.  The playbook connects to the configured vCenter data-center, powers off the VM, and then deletes it from disk.

## Author Information
[Andrew J. Huffman](mailto:ahuffman@redhat.com)
