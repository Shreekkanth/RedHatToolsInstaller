# sat6-create-hosts
An Ansible role to create new virtual and bare-metal hosts in Satellite 6.x. v2 of Satellite6 API is required.

## Role Variables

|Variable Name|Required|Description|Type|Default|
|---|:---:|---|:---:|:---:|
|sat6_fqdn|yes|Fully qualified domain name of the Satellite 6 host.|string|""|
|sat6_user|yes|Username of the Satellite 6 user that has access to create new hosts.|string|""|
|sat6_pass|yes|Password of the Satellite 6 user that has access to create new hosts. This should be vaulted to ensure security.|string|""|
|sat6_organization|yes|Satellite6 organization to create the hosts defined in `sat6_hosts`.|string|""|
|sat6_fail_on_existing|no|To fail the playbook if any of the hosts defined in `sat6_hosts` already exist in Satellite6.  Useful when using notifications in Ansible Tower, and you want to be notified on a failure. True means fail if a host exists, False means just output a summary instead and allows for a more idempotent style run. (i.e. you can run the playbook over and over again and it will only create hosts that don't exist)|boolean|False|
|sat6_hosts|yes|Satellite 6 hosts you would like to create|list of dictionaries|[]|

## `sat6_hosts` Dictionary Fields - Common
Fields you can utilize for either bare-metal or virtual host creation.

|Field Name|Required|Description|Type|
|---|:---:|---|:---:|
|name|yes|Hostname of the host to create|string|
|comment|no|A comment that will appear in the host's additional information.  A short description of what the host is for.|string|
|domain|no|Name of the Satellite6 domain to create the host with. Not required if you wish to inherit the host group's default domain, otherwise this overrides the host group default.|string|
|host_group|yes|Name of the Satellite6 Host Group to create the new host with.|string|
|ipv4|no|IPv4 address to assign to the host.  Not required if the host group is configured to suggest an IPv4 address via ipam or dhcp.|string|
|location|yes|Name of the Satellite6 location where you will be deploying the host.|string|
|partition_table|no|Name of the Satellite6 partition table to create the host with.  Not required if you wish to inherit the host group's default partition table.|string|
|subnet|no|Name of the Satellite6 subnet to create the host with.  Not required if you wish to inherit the host group's default subnet.|string|
|parameters|no|List of additional Satellite6 host specific parameters you would like to set on the host.  This is useful when doing post provisioning tasks and wish to use conditionals based off of these values, etc.|list of dictionaries|


## `sat6_hosts` Dictionary Fields - Virtual

|Field Name|Required|Description|Type|
|---|:---:|---|:---:|
|compute_profile|no|Name of the Satellite6 compute profile you want to deploy the host with.  If not provided the default from the host group will be utilized.|string|
|compute_resource|yes|Name of the Satellite6 compute resource you want to deploy the host on.|string|

## `sat6_hosts` Dictionary Fields - Physical

|Field Name|Required|Description|Type|
|---|:---:|---|:---:|
|mac|yes|MAC address of the physical host you want to deploy.|string|

## `sat6_hosts.parameters` Dictionary Fields
|---|:---:|---|:---:|
|name|yes|Name of the parameter to create.|string|
|value|yes|Value of the parameter to create|string|

## Debugging
To view full debugging output increase the verbosity to 1 (Verbose) in Ansible Tower, or a single `-v` in Ansible Core/Engine.  

## Example Playbook

```yaml
    ---
    - hosts: "localhost"
      vars_files:
        - "vars/myvaultedsecrets.yml"
      tasks:
        - name: Provision Satellite 6 Hosts
          include_role:
            - name: "sat6-create-hosts"
          vars:
            sat6_fqdn: "mysat6server.mydomain.com"
            sat6_user: ""
            #sat6_pass: "this is set in the vars/myvaultedsecrets.yml file"
            sat6_organization: "my organization"
            sat6_fail_on_existing: True
            #it's recommended to pass sat6_hosts as an extra_variable, but you could set
            #sat6_fail_on_existing: False to run the playbook in a more idempotent style if you wish to
            #keep track of all the sat6 hosts you create in source control
            sat6_hosts:
              #VM
              - name: "my-new-vm"
                host_group: "RHEL7-Virtual"
                location: "Raleigh"
                ipv4: "192.168.122.24"
                domain: "redhat.com"
                comment: "Web server to serve cool new website"
                compute_resource: "vsphere.vmware.com" #This is the name of your compute resource
                compute_profile: "3-Large"
              #Bare-metal
              - name: "my-new-bare-metal"
                host_group: "RHEL7-Physical"
                location: "Raleigh"
                ipv4: "192.168.122.25"
                domain: "redhat.com"
                comment: "Database server"
                mac: "12:34:56:78:91:23"                
```

## License
[MIT](LICENSE)

## Author Information
[Andrew J. Huffman](mailto:ahuffman@redhat.com)
