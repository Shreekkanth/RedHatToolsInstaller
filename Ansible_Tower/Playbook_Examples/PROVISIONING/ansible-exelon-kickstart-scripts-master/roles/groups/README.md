# groups

A role to create operating system user groups.

## Role Variables
|Variable Name|Required|Default Value|Type|
|:---:|:---:|:---:|:---:|
|groups|yes|undefined|list of dictionaries|

### `groups` dictionary fields
|field|description|type|
|:---:|:---:|:---:|
|name|Name of the group to create|string|
|gid|Group ID to create the group with|string|
|system|Whether or not the group is a system group type|Boolean|

## Example Playbook
```yaml
- hosts: servers
  roles:
    - role: groups
      groups:
        - name: "group1"
          gid: "10000"
          system: False
        - name: "group2"
          gid: "10001"
          system: False        
```             

## License
[MIT](LICENSE)

## Author
[Andrew J. Huffman](mailto:ahuffman@redhat.com)
