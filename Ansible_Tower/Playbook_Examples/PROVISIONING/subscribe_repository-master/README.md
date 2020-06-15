subscribe_repository
====================

`subscribe_repository` configures .repo files in the /etc/yum.repos.d/ directory.

Requirements
------------

No.

Role Variables
--------------

No.

Dependencies
------------

No.

Example Playbook
----------------

---
- hosts: servers
  vars:
  - subscribe_repository_host={{ repository_server_name }}
  - subscribe_repository_repo_file={{ .repo_file_name }}
  roles:
  - { role: subscribe_repository }
---

License
-------

BSD

Author Information
------------------

Naoya Hashimoto <nhashimo@redhat.com>
