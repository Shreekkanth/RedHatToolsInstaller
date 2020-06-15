# Build EMC VM Template Playbook
## Description
An Ansible playbook to build EMC's bios or efi based VM Template.
## Playbook Filename
[build-emc-vm-template.yml](build-emc-vm-template.yml)
## Tags Available
| Tag | Description | Includes Tags |
| --- | --- | :---: |
| vm_exist_check | Runs tasks associated with testing if a device already exists on the VM Template kickstart IP address | N/A |
| vm_create | Runs tasks associated with creating the VM in vSphere and installing the Operating System. | vm_exist_check, vm_folder, seed_snapshot |
| postconfig | Runs tasks associated with configuring and customizing the virtual machine template. | finalize_vm_config |
| vmware_tools | Runs tasks associated with installing VMWare Tools. | vmware_tools_mount, vmware_tools_copy, vmware_tools_unmount, vmware_tools_install |
| cleanup | Runs tasks associated with cleaning up the VM prior to converting to a template. | N/A |
| wrap_up | Runs tasks associated with converting the VM into a VM template.| vm_shutdown, final_snapshot, vm_convert_to_template, vm_export_to_ovf |
| seed_snapshot | Creates a VM snapshot with title `Seed Snapshot`. | N/A |
| finalize_vm_config | Runs tasks associated with ensuring the boot ISO is detached and setting VM bios boot settings. | N/A |
| vmware_tools_mount | Runs tasks associated with attaching the VMWare Tools installation ISO to a VM | N/A |
| vmware_tools_copy | Runs tasks associated with extracting the VMWare Tools installation files to /tmp prior to installation | N/A |
| vmware_tools_unmount | Runs tasks associated with ensuring VMWare Tools installation ISO is detached from a VM | N/A |
| vmware_tools_install | Runs tasks associated with installing VMWare Tools on the VM | N/A |
| vm_shutdown | Shuts down the VM via VMWare Tools in preparation for a final snapshot and conversion to a VM template. | N/A |
| final_snapshot | Creates a VM snapshot with title `Post-configuration Snapshot` | N/A |
| vm_convert_to_template | Converts the VM to a template. | N/A |
| vm_export_to_ovf | Exports the built VM Template as OVF, converts the OVF to OVA, and moves it to the `vm_template_export_win_share` | N/A |

## Variables
| Variable Name | Default Value | Description | Type | Variable File |
| --- | :---: | --- | :---: | --- |
| vctr_iso_source_path | "/apps/data/built_iso/rhel7.6_emc_ks_{{ vm_build_type }}.iso" | This is the ISO to upload to vCenter when the prompt is answered as "yes".  The path is templated with "bios" or "efi" based on the prompt answer for the type of template to build. | string | [vars/common.yml](vars/common.yml) |
| vm_template_export_path | "/tmp" | Where to initially (and temporarily) export the OVF VM template to. The temporary OVF is cleaned up as part of the conversion process to OVA.| string | [vars/common.yml](vars/common.yml) |
| vm_template_export_win_share | "//rosetta.corp.emc.com/ansible" | Where to export the OVA VM template to. | string | [vars/common.yml](vars/common.yml) |
| vm_template_ova_force_sha1_hash_algo | True | Newer ESX servers export their OVF files with SHA256 checksums.  This setting forces the conversion of the checksums to SHA1 for compatibility with older ESX environments. | boolean | [vars/common.yml](vars/common.yml) |
## Process Details
The following sections describe the major sections of the template build process.

### Initialization
The playbook begins the process by prompting the end-user for a data-center, their vSphere username and password, the IP address that was set in their kickstart configuration file (used to connect to the VM when initially built), name to create the VM as, and whether or not to update the source kickstart ISO in the vSphere data-center.

* The playbook file that executes these actions is [build-emc-vm-template.yml](build-emc-vm-template.yml).  
    * The variables that affect this section are found in [vars](vars), and are in the naming convention of emc-vm-template-**[datacenter name]**, where the `datacenter name` must match the name passed from the playbook prompt for vSphere data-center.
    * There are also some variables that are common, and do not apply to a specific datacenter.  These variables are found in [vars/common.yml](vars/common.yml).

### Virtual Machine Creation
The playbook attaches to vSphere and makes sure the configured folder to build the VM in exists, and creates it if not.  Next the virtual machine is created with the configured VM settings, the custom kickstart boot ISO (uploaded in the initialization section) is attached to the VM, and the VM is powered on.  Once the VM's operating system has been installed and we are able to connect to it via SSH port 22, the seed VM snapshot is created.

* The playbook file that executes the VM folder and VM creation actions is [build-emc-vm-template.yml](build-emc-vm-template.yml).  
    * The variables that affect this section are found in [vars](vars), and are in the naming convention of emc-vm-template-**[datacenter name]**, where the `datacenter name` must match the name passed from the playbook prompt for vSphere data-center.
* The playbook file that checks for connectivity to the new VM is [playbooks/wait_for_connection.yml](playbooks/wait_for_connection.yml).  
    * *There are no variables associated with this playbook.*
* The playbook file that executes the seed snapshot creation is [playbooks/vm_seed_snapshot.yml](playbooks/vm_seed_snapshot.yml).  
    * The variables that affect this section are found in [vars](vars), and are in the naming convention of emc-vm-template-**[datacenter name]**, where the `datacenter name` must match the name passed from the playbook prompt for vSphere data-center.

### Post Configuration
The playbook connects to the VM after the seed snapshot has been created and begins the post provisioning configuration and customization work.  

This playbook runs a series of tasks that were implemented in accordance to the `rhel7u5u1_template_build_notes.docx` documentation provided by EMC, which entails the manual steps taken to build EMC's VM template prior to automation.

Once the post provisioning steps have completed, the VM's settings are finalized.  This involves reconfiguring the VM to ensure that the CD-ROM is fully detached, and that the bios boot order has been properly configured.

* The playbook file that executes the post-provisioning configuration actions is [playbooks/post_provisioning.yml](playbooks/post_provisioning.yml), which includes the task list found in [playbooks/tasks/post-provision-tasks.yml](playbooks/tasks/post-provision-tasks.yml).
    * All post-provisioning variables are located in [playbooks/vars/emc-vm-template-postprovision.yml](playbooks/vars/emc-vm-template-postprovision.yml).
* The playbook file that executes the VM setting finalization actions is [playbooks/vm_finalize_configuration](playbooks/vm_finalize_configuration).  
    * The variables that affect this section are found in [vars](vars), and are in the naming convention of emc-vm-template-**[datacenter name]**, where the `datacenter name` must match the name passed from the playbook prompt for vSphere data-center.

### VMWare Tools
Once the post provisioning configuration is completed VMWare Tools are installed.  This process involves attaching the VMWare Tools installation ISO to the VM, locating the installation tarball, extracting the tarball to /tmp, ejecting the VMWare Tools installation ISO from the VM, validating that VMWare Tools ISO is detached from the VM in vCenter, and finally installing VMWare Tools.

* The playbook file that attaches the VMWare Tools ISO to the VM is [playbooks/vmware_tools_mount.yml](playbooks/vmware_tools_mount.yml).
* The playbook file that executes the extraction of the VMWare Tools installation files is [playbooks/vmware_tools_copy.yml](playbooks/vmware_tools_copy.yml)
* The playbook file that detaches the VMWare Tools ISO is [playbooks/vmware_tools_unmount.yml](playbooks/vmware_tools_unmount.yml).
* The playbook file that installs VMWare Tools is [playbooks/vmware_tools_install.yml](playbooks/vmware_tools_install.yml).


*All of the above playbook file variables are found in [vars](vars), and are in the naming convention of emc-vm-template-**[datacenter name]**, where the `datacenter name` must match the name passed from the playbook prompt for vSphere data-center.*

### Cleanup
After VMWare Tools are installed on the VM the configuration process is nearly complete.  Prior to converting the VM to a VMWare template we need to cleanup the system.

This playbook runs a series of tasks that were implemented in accordance to the `rhel7u5u1_template_build_notes.docx` documentation provided by EMC, which entails the manual steps taken to build EMC's VM template prior to automation.

* The playbook file that executes the clean up actions is [playbooks/vm_cleanup.yml](playbooks/vm_cleanup.yml).  All clean up variables are located in [playbooks/vars/emc-vm-template-postprovision.yml](playbooks/vars/emc-vm-template-postprovision.yml).

### Wrap-Up and Finalization
After the VM is cleaned up, the VM is powered off, a final snapshot is taken, the VM is then converted to a VMWare template, the VMWare template is exported in OVF format, the OVF export is converted to OVA and deposited on a Windows network share for pickup by vRA.

* The playbook file that powers off the VM is [playbooks/vm_shutdown.yml](playbooks/vm_shutdown.yml)
* The playbook file that creates a final snapshot of the clean VM is [playbooks/vm_final_snapshot.yml](playbooks/vm_final_snapshot.yml)
* The playbook file that converts the VM to a VMWare template is [playbooks/vm_convert_to_template.yml](playbooks/vm_convert_to_template.yml)
* The playbook file that exports, converts, and deposits the OVA VMware template is [playbooks/vm_export_to_ovf.yml](playbooks/vm_export_to_ovf.yml)


*All of the above playbook file variables are found in [vars](vars), and are in the naming convention of emc-vm-template-**[datacenter name]**, where the `datacenter name` must match the name passed from the playbook prompt for vSphere data-center.*

## Author Information
[Andrew J. Huffman](mailto:ahuffman@redhat.com)
