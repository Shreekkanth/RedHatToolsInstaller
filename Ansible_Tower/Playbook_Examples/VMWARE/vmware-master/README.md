Set of ansible playbooks to automate content host creation on vcenter.
This requires a template to already be created in the vmware environment.  

Prerequisite: 
On control node: python2-pyvmomi

```
# sudo dnf list fedora-release python2-pyvmomi
Installed Packages
fedora-release.noarch                   28-6                        @updates
python2-pyvmomi.noarch                  6.5-4.fc27                  @fedora 
```



Usage: # ansible-playbook  vmware_create_content_host.yml  --extra-vars "vm_name=gtaylor-ans-1"  --ask-vault-pass

or put vault password in file:  
--vault-password-file=VAULT_PASSWORD_FILES  
and specify --user key file:  
--private-key=PRIVATE_KEY_FILE  
The list goes on.... with options for improvement.  



Item by item explanation:
```
ansible-playbook                        # ansible command to run playbooks
vmware_create_content_host.yml          # specific playbook to create a new guest(content host for Satellite in this use case)
--extra-vars "vm_name=gtaylor-ans-1"    # use ansible --extra-vars option to pass the virtual guest name to the playbook
--ask-vault-pass                        # vault password where password and corp specific resource names are stored
```

These are the values in the vcenter-vault.yml that will need to be adjusted for
your environment.  The only value that is super-secret is the vcenter password.
The rest of the variables are in the vault as a safety measure in case the
playbooks are leaked outside of the corporate network. 
```
vcenter_ip: vcenter.toledo.x.x.x.x.x.com
vcenter_username: xxxx
vcenter_password: xxxx
datacenter: xxxx
template: xxxx
folder: xxxx
```
You'll need to delete the existing vcenter-vault.yml and create a new file for your use.  Variable names are above, supply your values or see gt for values used.  


The repo also contains: 

```
This README.md file
inventory
vmware_delete_vm.yml	# allows easy deletion of vm guest.  uses same values as vmware_create_content_host.yml
vmware_rename_vm_yml	# rename external vm guest name.  uses same values as vmware_create_content_host.yml.  lightly tested.
vcenter-vault.yml       # vault file to hold password and other corp resource values
```

Feedback and suggestions for improvement welcomed!


Test Line
