Role Name
=========
Install and configure a Red Hat baremetal server.

- Install SSH keys (rcipsshkeys)
- Configure network (ifcfg-* files)
- Register and subscribe to RHN (with your RHN credentials)
- Enable RHEL* repositories
- Install EPEL repository (true or false)
- Install list of packages (choose what you want)
- Update the system (true or false)
- Create stack user and sudo entry
- Install and configure OpenVPN (Red Hat VPN, true or false)
- Install undercloud prerequisites (true or false)


Requirements
------------
None.

Role Variables
--------------
```
provisioning_rhn_unregister: true
provisioning_configure_network: true
provisioning_update_system: true
provisioning_disable_repos: true
provisioning_enable_epel: true
provisioning_packages:
  - vim
  - yum-plugin-priorities
  - strace
  - ethtool
  - net-tools
  - screen
  - sysstat
  - git
provisioning_openvpn: true
provisioning_redhat_network: false
provisioning_undercloud: false
provisioning_director_version: '7-director'
```

Dependencies
------------
None.

Example Playbook
----------------
```
$ mkdir ~/ansible ; cd ~/ansible
$ mkdir -p playbooks/name-your-playbook/files/etc
$ cd playbooks/name-your-playbook/files/etc
$ mkdir -p openvpn sysconfig/network-scripts
$ cp -rfp ~/somewhere/{client.*,redhat.conf,RedHatISCA.pem} openvpn
$ cp -rfp ~/somewhere/ifcfg-* sysconfig/network-scripts
$ cd .. ; mkdir -p inventory/name-your-inventory
$ cat <<EOF > inventory/name-your-inventory/hosts 
[lab]
gtrellu-lab ansible_ssh_host=46.21.13.41
EOF
$ cd ~/ansible
$ ansible-playbook -i inventory/name-your-inventory/hosts playbooks/name-your-playbook/main.yml --ask-pass
```

```
---
# playbooks/name-your-playbook/main.yml
- hosts: all
  remote_user: root

  vars:
    rhn_username: gtrellu@redhat.com
    rhn_password: XXXXXXXXXXX
    rhn_pool_id: 8a85f98144844aff014488d058bf15be
    rhn_repos:
      - rhel-7-server-rpms
      - rhel-7-server-optional-rpms
      - rhel-7-server-extras-rpms
      - rhel-7-server-openstack-7.0-rpms
      - rhel-7-server-openstack-7.0-director-rpms
    ifcfg_to_remove: ifcfg-ens3f3.1121

  roles:
    - provisioning
```

License
-------
GPL, CC-BY

Author Information
------------------
Gaetan Trellu - gtrellu@redhat.com
