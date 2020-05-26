Azure Storage Account Create
============================

Creates an Azure storage account.

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
- `storage_account_type`: the type of storage account. [learn more](https://azure.microsoft.com/documentation/articles/storage-redundancy/)
- `storage_account_name`: the name of the storage account

Example Playbook
----------------

```yaml
- hosts: azure
  roles:
  - { 
        'role': 'azure_storageaccount_create',
        'resource_group': 'abb1a6f7-ec37-4507-a780-2f9e69f5a1b0',
        'storage_account_type': 'Standard_LRS',
        'storage_account_name': 'sa1'
    }
```