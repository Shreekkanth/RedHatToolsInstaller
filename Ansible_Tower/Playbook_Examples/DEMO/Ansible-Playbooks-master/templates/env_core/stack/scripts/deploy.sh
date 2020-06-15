#!/usr/bin/env bash
if [ $PWD != $HOME ] ; then echo "USAGE: $0 Must be run from $HOME"; exit 1 ; fi

cd ~
source ~/stackrc

stack_name={{ stack_name }}

time openstack overcloud deploy --templates \
  --stack $stack_name \
  -n ~/templates/network_data.yaml \
  -r ~/templates/roles_data.yaml \
  -e /usr/share/openstack-tripleo-heat-templates/environments/network-isolation.yaml \
  -e /usr/share/openstack-tripleo-heat-templates/environments/network-environment.yaml \
  -e /usr/share/openstack-tripleo-heat-templates/environments/neutron-sriov.yaml \
  -e /usr/share/openstack-tripleo-heat-templates/environments/host-config-and-reboot.yaml \
  -e /usr/share/openstack-tripleo-heat-templates/environments/ssl/tls-endpoints-public-ip.yaml \
  -e ~/templates/environments/overcloud-images.yaml \
  -e ~/templates/environments/misc-host-settings.yaml \
  -e ~/templates/environments/storage-environment.yaml \
  -e ~/templates/environments/site-environment.yaml \
  -e ~/templates/environments/neutron-sriov.yaml \
  -e ~/templates/environments/enable-tls.yaml \
  -e ~/templates/environments/inject-trust-anchor.yaml
