# Remove VM Folder
## Description
An Ansible playbook to delete/remove a VM folder in vSphere.  ***WARNING: This will remove all VMs contained within the folder you are removing***

* The variables that affect this playbook are found in [vars](vars), and are in the naming convention of emc-vm-template-**[datacenter name]**, where the `datacenter name` must match the name passed from the playbook prompt for vSphere data-center.  

## Playbook Filename
[remove-vm-folder.yml](remove-vm-folder.yml)
## Tags Available
N/A
## Process Details
The playbook begins the process by prompting the end-user for a data-center, their vSphere username and password, and VM folder to remove.  The playbook connects to the configured vCenter data-center and deletes the VM folder specified.
## Author Information
[Andrew J. Huffman](mailto:ahuffman@redhat.com)
