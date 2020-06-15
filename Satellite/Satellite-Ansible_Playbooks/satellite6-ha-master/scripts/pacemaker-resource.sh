#!/bin/bash
#This script creates all the required resources for the SAT6-HA pacemaker cluster
#and sets colocation constraints and order constraints to ensure that all the 
#services are colocated on the same node and start in the correct order.
#VIP resource
#
pcs resource create VirtualIP IPaddr2 ip=10.19.2.30 cidr_netmask=24 
# LVM and filesystem creation
pcs resource create sat_vg LVM volgrpname=sat_vg exclusive=true 
pcs resource create fs_pulp Filesystem device="/dev/sat_vg/lv_pulp" directory="/var/lib/pulp" fstype="xfs" 
pcs resource create fs_candlepin Filesystem device="/dev/sat_vg/lv_candlepin" directory="/var/lib/candlepin" fstype="xfs"   
pcs resource create fs_foreman Filesystem device="/dev/sat_vg/lv_foreman" directory="/var/lib/foreman" fstype="xfs"  
pcs resource create fs_puppet Filesystem device="/dev/sat_vg/lv_puppet" directory="/var/lib/puppet" fstype="xfs"  
pcs resource create fs_wwwpulp Filesystem device="/dev/sat_vg/lv_wwwpulp" directory="/var/www/pulp" fstype="xfs"  
pcs resource create fs_elastic Filesystem device="/dev/sat_vg/lv_elastic" directory="/var/lib/elasticsearch" fstype="xfs"  
pcs resource create fs_mongodb Filesystem device="/dev/sat_vg/lv_mongodb" directory="/var/lib/mongodb" fstype="xfs"  
pcs resource create fs_pgsql Filesystem device="/dev/sat_vg/lv_psqldata" directory="/var/lib/pgsql" fstype="xfs"  
pcs resource create fs_puppetenv Filesystem device="/dev/sat_vg/lv_puppetenv" directory="/etc/puppet/environments" fstype="xfs" 
pcs resource create fs_tftpboot Filesystem device="/dev/sat_vg/lv_tftpboot" directory="/var/lib/tftpboot" fstype="xfs" 
pcs resource create fs_dhcp Filesystem device="/dev/sat_vg/lv_dhcp" directory="/var/lib/dhcpd" fstype="xfs" 
pcs resource create fs_named Filesystem device="/dev/sat_vg/lv_named" directory="/var/named" fstype="xfs" 
#
# Service resource creation
#
pcs resource create rs_dhcp systemd:dhcpd op monitor interval=10s op start interval=0s timeout=100s op stop interval=0s timeout=100s
pcs resource create rs_named systemd:named op monitor interval=10s op start interval=0s timeout=100s op stop interval=0s timeout=100s
pcs resource create rs_puppet systemd:puppet op monitor interval=10s op start interval=0s timeout=100s op stop interval=0s timeout=100s
pcs resource create rs_pgsql systemd:postgresql op monitor interval=10s op start interval=0s timeout=100s op stop interval=0s timeout=100s
pcs resource create rs_mongodb systemd:mongod op monitor interval=10s op start interval=0s timeout=100s op stop interval=0s timeout=100s
pcs resource create rs_qpidd systemd:qpidd op monitor interval=10s op start interval=0s timeout=100s op stop interval=0s timeout=100s
pcs resource create rs_qdrouterd systemd:qdrouterd op monitor interval=10s op start interval=0s timeout=100s op stop interval=0s timeout=100s
pcs resource create rs_tomcat systemd:tomcat op monitor interval=10s op start interval=0s timeout=100s op stop interval=0s timeout=100s
pcs resource create rs_elasticsearch lsb:elasticsearch op monitor interval=10s 
pcs resource create rs_pulp_workers systemd:pulp_workers op monitor interval=10s op start interval=0s timeout=100s op stop interval=0s timeout=100s
pcs resource create rs_foreman-proxy systemd:foreman-proxy op monitor interval=10s op start interval=0s timeout=100s op stop interval=0s timeout=100s
pcs resource create rs_pulp_resource_manager systemd:pulp_resource_manager op monitor interval=10s op start interval=0s timeout=100s op stop interval=0s timeout=100s
pcs resource create rs_pulp_celerybeat systemd:pulp_celerybeat op monitor interval=10s op start interval=0s timeout=100s op stop interval=0s timeout=100s
pcs resource create rs_httpd systemd:httpd op monitor interval=10s op start interval=0s timeout=100s op stop interval=0s timeout=100s
pcs resource create rs_foreman-tasks systemd:foreman-tasks op monitor interval=10s timeout=30s op start interval=0s timeout=100s op stop interval=0s timeout=100s
##############################
###  Creating Constraints  ###
##############################
#
# Colocation Constraints
#
pcs constraint colocation add sat_vg with VirtualIP
pcs constraint colocation set fs_dhcp fs_named fs_puppet fs_puppetenv fs_pgsql fs_mongodb fs_pulp fs_wwwpulp fs_foreman fs_elastic fs_candlepin fs_tftpboot sequential=false set sat_vg 
pcs constraint colocation add rs_dhcp with fs_dhcp
pcs constraint colocation add rs_named with fs_named
pcs constraint colocation add rs_pgsql with fs_pgsql
pcs constraint colocation add rs_mongodb with fs_mongodb
pcs constraint colocation add rs_foreman-proxy with fs_foreman
pcs constraint colocation add rs_elasticsearch with fs_elastic
pcs constraint colocation set fs_puppet fs_puppetenv rs_puppet
pcs constraint colocation set fs_pulp fs_wwwpulp rs_pulp_workers
pcs constraint colocation set VirtualIP rs_qpidd rs_qdrouterd
pcs constraint colocation add rs_tomcat with VirtualIP
pcs constraint colocation add rs_httpd with VirtualIP
pcs constraint colocation set fs_pulp fs_wwwpulp rs_pulp_resource_manager
pcs constraint colocation set fs_pulp fs_wwwpulp rs_pulp_celerybeat
pcs constraint colocation add rs_foreman-tasks with fs_foreman
#
#Order constraints to start service after the filesystems
#
pcs constraint order set sat_vg set fs_dhcp fs_named fs_puppet fs_puppetenv fs_pgsql fs_mongodb fs_pulp fs_wwwpulp fs_foreman fs_elastic fs_candlepin fs_tftpboot sequential=false
pcs constraint order VirtualIP then sat_vg
pcs constraint order set sat_vg fs_dhcp rs_dhcp
pcs constraint order set sat_vg fs_named rs_named
pcs constraint order set sat_vg fs_puppet fs_puppetenv rs_puppet
pcs constraint order set sat_vg fs_pgsql rs_pgsql
pcs constraint order set sat_vg fs_mongodb rs_mongodb
pcs constraint order set sat_vg fs_pulp fs_wwwpulp rs_pulp_workers rs_pulp_celerybeat
pcs constraint order set sat_vg fs_foreman rs_foreman-proxy
pcs constraint order set sat_vg fs_elastic rs_elasticsearch
pcs constraint order start fs_wwwpulp then rs_httpd
#
#Order constraints to start  services after parent service
#
pcs constraint order set VirtualIP rs_qpidd rs_qdrouterd
pcs constraint order VirtualIP then rs_dhcp
pcs constraint order VirtualIP then rs_named

pcs constraint order set rs_puppet rs_dhcp rs_named rs_pgsql sequential=false set rs_mongodb set rs_qpidd rs_qdrouterd sequential=false set rs_tomcat rs_elasticsearch rs_pulp_workers rs_pulp_celerybeat rs_pulp_resource_manager rs_foreman-proxy sequential=false set rs_httpd rs_foreman-tasks sequential=false
# 
# Set default resource stickiness to avoid failback when the original node is restored 
# 
pcs property set default-resource-stickiness=INFINITY 
