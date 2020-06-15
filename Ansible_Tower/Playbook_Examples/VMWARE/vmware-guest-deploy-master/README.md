role-vmware-guest
=========

Provision vmware vms

Role Variables
--------------

vmware_validate_certs: validate certs (default: true)

vmware_guest_name: guest name (required)

vcenter_username: vmware username (required)

vcenter_password: vmware password (required)

vmware_guest_hardware: vmware hardware (required)

vmware_guest_networks: vmware networks (requried)

vmware_guest_customization: vmware customiziation

vmware_guest_disk: vmware disks (required)

vmware_guest_publick_key: public key to insert into vm

Required if vmware_guest_public_key is defined:

vmware_guest_username: user to insert ssh key into

vmware_guest_password: password for previous useer

Example Playbook
----------------

    - role: role-vmware-guest
      vars:
        vmware_validate_certs: false
        vmware_guest_name: "{{host_name}}"
        vcenter_username: scsu\{{domain_username}}
        vcenter_password: "{{domain_password}}"
        vmware_guest_hardware:
          num_cpus: "{{blobs[vm_blob]['num_cpus']}}"
          memory_mb: "{{blobs[vm_blob]['memory_gb'] * 1024}}"
        vmware_guest_networks:
          - name: VLAN{{vlan_num}}
            ip: "{{infoblox_free_ip}}"
            netmask: "{{vlan[vlan_num]['netmask']}}"
            gateway: "{{vlan[vlan_num]['gateway']}}"
            type: static
            device_type: vmxnet3
        vmware_guest_customization:
          dns_servers: "{{dns_servers}}"
          dns_suffix: "{{dns_suffix}}"
        vmware_guest_disk: "{{blobs[vm_blob]['disks']}}"

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
