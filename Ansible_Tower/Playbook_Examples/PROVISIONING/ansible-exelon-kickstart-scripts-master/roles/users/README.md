# Users
A role to create operating system user accounts and set appropriate permissions on their home directories.

## Role Variables
|Variable Name|Required|Default Value|Type|
|:---:|:---:|:---:|:---:|
|users|yes|undefined|list of dictionaries|

### `users` dictionary fields
|field|description|type|
|:---:|:---:|:---:|
|name|Username for the user account to create|string|
|groups|List of additional groups the user account should be a member of|list|
|uid|User ID to create the user account as|string|
|primary_group|Primary group the user is a member of|string|
|comment|Description of the user account being created|string|
|password|Encrypted string of the user account's password|string|
|home|Path to create for the user account's home directory|string|
|home_mode|Permission mode for the user account's home directory|string|
|home_owner|Username that should own the user account's home directory|string|
|home_group|Group that owns the user account's home directory|string|
|shell|Path to the binary shell for the user account|string|

## Example Playbook
```yaml
- hosts: servers
  roles:
    - role: users
      users:
        - name: "user1"
          groups:
            - "group1"
            - "group2"
          uid: "1000"
          primary_group: "users"
          comment: "User Account 1"
          password: "$lkjadsf;lkj;asdflkj./"
          home: "/home/user1"
          home_mode: "0700"
          home_owner: "user1"
          home_group: "users"
          shell: "/bin/bash"
        - name: "user2"
          groups: [] #[] is yaml syntax for an empty list
          uid: "1001"
          primary_group: "users"
          comment: "User Account 2"
          password: "3adsflj;$asdf/."
          home: "/home/user2"
          home_mode: "0700"
          home_owner: "user2"
          home_group: "users"
          shell: "/bin/sh"
```
## License
[MIT](LICENSE)

## Author
[Andrew J. Huffman](mailto:ahuffman@redhat.com)
