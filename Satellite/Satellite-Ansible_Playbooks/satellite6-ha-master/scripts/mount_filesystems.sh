#!/bin/bash
#Activate the volume group
vgchange -a y sat_vg
#

#Mount the filesystems
mount -o _netdev /dev/mapper/sat_vg-lv_named /var/named
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
