Server Names
============

Get server names for virtual machines.

This role calls the Deloitte Server Naming API (SNAPI) to register hostnames for new virtual machines.

### Server Name Generation

The SNAPI uses the api POST ***system*** json key to create a unique server name. Using the same system value on repeat requests results in the same server name being returned, thus the API is idempotent on the ***system key*** value.

An algorithm is used to generate ***system keys*** for each cloud provider to make server names unique for all hosts. Each cloud provider uses a concatenated string of inventory local variables and a unique SNAPI UUID used as a random seed. The SNAPI has a 100 character limit on the ***system key*** so the concatenated string is hashed using sha256 to generate a 64 character ***system key***.

**Azure Key Algorithm**:  
sha256(Azure subscription ID + Azure Resource Group + Ansible Inventory Hostname + SNAPI UUID)

Requirements
------------

- ansible==2.8.1
- msrest==0.6.8
- packaging==19.0
- ansible[azure]

Role Variables
--------------

- `snapi_auth_url`: the server naming api oauth2 url
- `snapi_resource`: the server naming api resource id
- `snapi_client_id`: the server naming api client id 
- `snapi_client_secret`: the server naming api client secret
- `snapi_name_url`: the server naming api server name url
- `snapi_environment`: the environment prefix for new hostnames (eg. USAZUADVDE)
- `snapi_uuid`: the snapi system key seed
- `subscription_id`: the Azure subscription id
- `resource_group`: the Azure resource group

Example Playbook
----------------

```yaml
- hosts: azure
  roles:
  - {  
        "snapi_auth_url": "https://login.microsoftonline.com/36da45f1-dd2c-4d1f-af13-5abe46b99921/oauth2/token",
        "snapi_resource": "7c851ad3-88a4-48ca-99af-3688434f1264",
        "snapi_client_id": "4e0db9ac-aa09-4a21-8989-5dbfdf6ca505",
        "snapi_client_secret": "c2VjcmV0MTIzCg==",
        "snapi_name_url": "https://onecloudapi.deloitte.com/servernaming/20190215/ServerNaming",
        "snapi_environment": "USAZUADVDE",
        "snapi_uuid": "8b53c9a8-ed07-462c-827f-4c0440c91f81",
        "subscription_id": "d20a6d5e-576d-4fe4-86fa-70306e8b237d",
        "resource_group": "rg1"
    }
```