#!/bin/bash
#Create and mount filesystems required for the satellite 
#environment that would be controlled by pacemaker eventually
#TO BE RUN ON THE FIRST NODE ONLY
### Create Physical Volume ###
#
# BJ pvcreate /dev/sdc
#
### Create Volume group ###
#
# BJvgcreate sat_vg /dev/sdc
#
### Create Logical volumes ###
 lvcreate -L 500G -n lv_pulp sat_vg 
 lvcreate -L 10G -n lv_foreman sat_vg 
 lvcreate -L 10G -n lv_puppet sat_vg 
 lvcreate -L 10G -n lv_wwwpulp sat_vg 
 lvcreate -L 10G -n lv_elastic sat_vg 
 lvcreate -L 10G -n lv_candlepin sat_vg 
 lvcreate -L 100G -n lv_mongodb sat_vg 
 lvcreate -L 10G -n lv_psqldata sat_vg 
 lvcreate -L 10G -n lv_puppetenv sat_vg 
 lvcreate -L 10G -n lv_tftpboot sat_vg 
 lvcreate -L 10G -n lv_dhcp sat_vg 
 lvcreate -L 10G -n lv_named sat_vg 
#
### Create filesystems using these volumes ###
for i in $(lvs | grep sat_vg | awk '{print $1}'); do mkfs.xfs /dev/sat_vg/$i; done
#
### Create mount points ###
# 
#mkdir -p /var/lib/pulp 
#mkdir -p  /var/lib/candlepin 
#mkdir -p  /var/lib/foreman 
#mkdir -p  /var/lib/puppet 
#mkdir -p  /var/www/pulp 
#mkdir -p  /var/lib/elasticsearch 
#mkdir -p  /var/lib/mongodb 
#mkdir -p  /var/lib/pgsql 
#mkdir -p  /etc/puppet/environments 
#mkdir -p  /var/lib/tftpboot 
#mkdir -p  /var/lib/dhcpd
#systemctl stop named.service
#mv /var/named /var/named.orig
#mkdir -p  /var/named
#
### Mount the filesystems ###
#
mount  /dev/mapper/sat_vg-lv_pulp /var/lib/pulp
mount  /dev/mapper/sat_vg-lv_candlepin /var/lib/candlepin
mount  /dev/mapper/sat_vg-lv_foreman /var/lib/foreman
mount  /dev/mapper/sat_vg-lv_puppet /var/lib/puppet
mount  /dev/mapper/sat_vg-lv_wwwpulp /var/www/pulp
mount  /dev/mapper/sat_vg-lv_elastic /var/lib/elasticsearch
mount  /dev/mapper/sat_vg-lv_mongodb /var/lib/mongodb
mount  /dev/mapper/sat_vg-lv_psqldata /var/lib/pgsql
mount  /dev/mapper/sat_vg-lv_puppetenv /etc/puppet/environments
mount  /dev/mapper/sat_vg-lv_tftpboot /var/lib/tftpboot
mount  /dev/mapper/sat_vg-lv_named /var/named
# Copy over contents of /var/named.orig to /var/named
#cp -pr /var/named.orig/* /var/named
# Restore selinux booleans
#restorecon -Rv /var/named
