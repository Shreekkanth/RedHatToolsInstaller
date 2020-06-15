#!/bin/bash
# This script mounts the shared filesystems to the secondary node
#Activate the volume group
vgchange -a y sat_vg
#
#Create mount points
#
mkdir -p /var/lib/pulp
mkdir -p  /var/lib/candlepin
mkdir -p  /var/lib/foreman
mkdir -p  /var/lib/puppet
mkdir -p  /var/www/pulp
mkdir -p  /var/lib/elasticsearch
mkdir -p  /var/lib/mongodb
mkdir -p  /var/lib/pgsql
mkdir -p  /etc/puppet/environments
mkdir -p  /var/lib/tftpboot
mkdir -p  /var/lib/dhcpd
systemctl stop named.service
mv /var/named /var/named.orig
mkdir -p  /var/named
#
#Mount the filesystems
mount -o _netdev /dev/mapper/sat_vg-lv_pulp /var/lib/pulp
mount -o _netdev /dev/mapper/sat_vg-lv_candlepin /var/lib/candlepin
mount -o _netdev /dev/mapper/sat_vg-lv_foreman /var/lib/foreman
mount -o _netdev /dev/mapper/sat_vg-lv_puppet /var/lib/puppet
mount -o _netdev /dev/mapper/sat_vg-lv_wwwpulp /var/www/pulp
mount -o _netdev /dev/mapper/sat_vg-lv_elastic /var/lib/elasticsearch
mount -o _netdev /dev/mapper/sat_vg-lv_mongodb /var/lib/mongodb
mount -o _netdev /dev/mapper/sat_vg-lv_psqldata /var/lib/pgsql
mount -o _netdev /dev/mapper/sat_vg-lv_puppetenv /etc/puppet/environments
mount -o _netdev /dev/mapper/sat_vg-lv_tftpboot /var/lib/tftpboot
mount -o _netdev /dev/mapper/sat_vg-lv_dhcp /var/lib/dhcpd
mount -o _netdev /dev/mapper/sat_vg-lv_named /var/named
