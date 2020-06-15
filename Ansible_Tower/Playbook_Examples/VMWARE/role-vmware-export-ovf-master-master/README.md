# ahuffman.vmware_export_ovf

An Ansible Role to export VMs as OVFs.

## Requirements
pyvmomi Python module must be installed on the Ansible Control Node.  `pip install pyvmomi`

## Role Variables

| Variable Name | Required | Description | Default Value | Type |
| --- | :---: | --- | :---: | :---: |
| vctr_user | yes | Username of the vCenter user.| "" | string |
| vctr_pass | yes | Password of the vCenter user | "" | string |
| vctr_hostname | yes | Hostname of the vCenter | "" | string |
| vctr_datacenter | yes | Name of the vCenter datacenter | "" | string |
| vctr_validate_certs | yes | Validate the vCenter's certificate | False | boolean |
| vctr_vm_template_name | yes | Name of the virtual machine to export to OVF | "" | string |
| vctr_vm_template_folder | yes | Name of the virtual machine folder that the target virtual machine resides in | "" | string |
| vm_export_ovf_with_images | yes | Whether or not to export the OVF with attached ISOs | False | boolean |
| vm_export_ovf_export_folder | yes | Where to export the OVF to on the Ansible Control Node | "" | string |

## Example Playbook
```yaml
---
- name: "Export VM to OVF"
  hosts: "localhost"
  tasks:
    - name: "Export VM to OVF"
      include_role:
        name: "vwmare_export_ovf"
      vars:
        vm_export_ovf_export_folder: "/tmp"
```

## License
[MIT](LICENSE)

## Author Information
[Andrew J. Huffman](mailto:ahuffman@redhat.com)
