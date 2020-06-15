# Linux Disk Management

1. Create volume group on new server
2. Extends volume group to utilize all free space
3. Creates a filesystem on the new volume group
4. Verifies the filesystem exists
5. Mounts the new filesystem

### Requirements
------------
Linux OS supported LVM

### Role Variables
--------------

##### Variable Table

| Variable | Defined by |
|----------|------------|
| linux_disk_management_vg_name | defaults |
| linux_disk_management_disk_name | defaults |
| linux_disk_management_volume_name | defaults |
| linux_disk_management_mount_point | defaults |
| linux_disk_management_filesystem_type | defaults |

### Dependencies
------------

### Example Playbook
----------------

```
---
- name: Run disk expansion role
  include_role:
    name: ansible-role_linux_disk_management
  vars:
    linux_disk_management_vg_name: vg02
    linux_disk_management_disk_name: /dev/sdb
    linux_disk_management_volume_name: lv_opt_usr
    linux_disk_management_mount_point: /opt/usr
    linux_disk_management_filesystem_type: xfs
```
### License
-------

All rights reserved. BlueCross BlueShield of Tennessee, Inc.

### Author Information
------------------

William Collins

John Kennedy
