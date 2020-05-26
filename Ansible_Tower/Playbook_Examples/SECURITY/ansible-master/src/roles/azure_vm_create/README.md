Azure Virtual Machine Create
============================

Creates an Azure virtual machine.

This role provisions the operating system based on group membership. Supported groups are:

- `windows`
- `rhel`
- `ubuntu`

#### Windows

Windows hosts are provisioned with WinRM access. The WinRM listener uses a [PKCS#12](https://en.wikipedia.org/wiki/PKCS_12) certificate from the host's [Key Vault](https://docs.microsoft.com/en-us/azure/key-vault/key-vault-whatis) during deployment for the https fingerprint. The WinRM service is configured to delayed start mode. See [here](https://docs.microsoft.com/en-us/azure/marketplace/cloud-partner-portal/virtual-machine/cpp-create-key-vault-cert) for more information about creating the WinRM certificate.

Ansible WinRM connectivity is established on the standard 5986 https port using NTLM authentication. NTLM authenticates against the `admin_username` using the `admin_password` provided to the role.

Requirements
------------

- ansible==2.8.1
- msrest==0.6.8
- packaging==19.0
- ansible[azure]

Role Variables
--------------

#### Inventory Variables

- `resource_group`: the resource group for the storage account 
- `network_name`: the name of the virtual network
- `subnet_name`: the name of subnet in the virtual network

#### Group Variables

- `image_publisher`: the os image creator
- `image_offer`: the type of os image
- `image_sku`: the exact sku of the image
- `size`: the virtual machine size

#### Host Variables

- `admin_username`: the vm adminstrator username
- `admin_password`: the vm adminstrator password
- `os_disk_type`: the type of the primary disk
- `os_disk_size`: the size of the primary disk in GB

Example Playbook
----------------

```yaml
- hosts: azure
  roles:
  - {  
        'role': 'ansible_vm_create',
        'resource_group': 'rg1',
        'network_name': 'network1',
        'subnet_name' : 'subnet1',
        'image_publisher': 'MicrosoftWindowsServer',
        'image_offer': 'WindowsServer',
        'image_sku': '2016-Datacenter',
        'size': 'Standard_D2s_v3',
        'admin_username': 'admin',
        'admin_password': 'password1!',
        'os_disk_type': 'Standard_LRS',
        'os_disk_size': '128'
    }
```