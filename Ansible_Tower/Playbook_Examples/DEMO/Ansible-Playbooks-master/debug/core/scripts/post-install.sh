#!/bin/bash

set -x

source ~/core-cloudrc

# Create Dell Unity Cinder type
cinder type-create unity
cinder type-key unity set volume_backend_name=tripleo_dellemc_unity
cinder create --volume-type unity 1

# Flavors
openstack flavor create \
  --ram 512 \
  --disk 1 \
  --vcpus 1 \
  m1.tiny

# Images
openstack image create \
  --public \
  --file ~/images/cirros-0.4.0-x86_64-disk.img \
  --disk-format qcow2 \
  --container bare \
  cirros

# Networks
openstack network create test-network
openstack subnet create \
  --allocation-pool start=192.168.0.50,end=192.168.0.100 \
  --ip-version 4 \
  --subnet-range 192.168.0.0/24 \
  --no-dhcp \
  --gateway 192.168.0.1\
  --network test-network \
  test-subnet

# Keypairs
openstack keypair create \
  --public-key ~/.ssh/id_rsa.pub \
  undercloud-key

# Servers
openstack server create \
  --flavor m1.tiny \
  --image cirros \
  --key-name undercloud-key \
  --network test-network cirros-1
