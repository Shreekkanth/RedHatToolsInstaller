Playbook Name    : create_osp_lab                                                 
Playbook Author  : Ken Hitchcock                                                   
Playbook Purpose : Automate Openstack 13 Build on Libvirt                          

Playbook has one master playbook file called create_osp_lab.yaml with multiple roles.

One var file called vms.yaml with a dictionary called guests. Add all the vms you wish 
to create below it the guests dictionary. 

Fields below the guests are self explainatory.

Requirements

 - Libvirt environment already installed and configured.
 - Update var/vms.yaml with your environment layout.
 - Ansible engine installed.
 - /etc/ansible/hosts file updated with the following groups.
   - [kvm]
   - [ansible_host]
 - /etc/ansible/hosts configured with HostKeyChecking set to no. (Still to be automated)



