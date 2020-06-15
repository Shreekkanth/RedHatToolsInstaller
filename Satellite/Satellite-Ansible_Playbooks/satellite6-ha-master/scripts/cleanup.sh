#!/bin/bash
#
#This script stops Satellite services on the node, unmounts the 
#filesystems and deactivates the shared volume group
#
#Stop services
katello-service stop
systemctl stop postgresql.service
systemctl stop puppet.service
systemctl stop dhcpd.service
systemctl stop named.service
#
#unmount the filesysytems
#
umount /dev/mapper/sat_vg-lv_pulp /var/lib/pulp
umount /dev/mapper/sat_vg-lv_candlepin /var/lib/candlepin
umount /dev/mapper/sat_vg-lv_foreman /var/lib/foreman
umount /dev/mapper/sat_vg-lv_puppet /var/lib/puppet
umount /dev/mapper/sat_vg-lv_wwwpulp /var/www/pulp
umount /dev/mapper/sat_vg-lv_elastic /var/lib/elasticsearch
umount /dev/mapper/sat_vg-lv_mongodb /var/lib/mongodb
umount /dev/mapper/sat_vg-lv_psqldata /var/lib/pgsql
umount /dev/mapper/sat_vg-lv_puppetenv /etc/puppet/environments
umount /dev/mapper/sat_vg-lv_tftpboot /var/lib/tftpboot
umount /dev/mapper/sat_vg-lv_dhcp /var/lib/dhcpd
umount /dev/mapper/sat_vg-lv_named /var/named
#
#Deactivate volume group
#
vgchange -a n sat_vg


