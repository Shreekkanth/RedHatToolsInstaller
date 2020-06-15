#!/usr/bin/env bash
if [ $PWD != $HOME ] ; then echo "USAGE: $0 Must be run from $HOME"; exit 1 ; fi

source ~/stackrc
cd ~

stack_name=edge-cloud

time openstack overcloud update converge --templates \
  --stack $stack_name \
  -n ~/templates/network_data.yaml \
  -r ~/templates/roles_data.yaml \
  -e /usr/share/openstack-tripleo-heat-templates/environments/network-isolation.yaml \
  -e /usr/share/openstack-tripleo-heat-templates/environments/network-environment.yaml \
  -e /usr/share/openstack-tripleo-heat-templates/environments/disable-telemetry.yaml \
  -e /usr/share/openstack-tripleo-heat-templates/environments/tls-endpoints-public-dns.yaml \
  -e /usr/share/openstack-tripleo-heat-templates/environments/inject-trust-anchor-hiera.yaml \
  -e /usr/share/openstack-tripleo-heat-templates/environments/host-config-and-reboot.yaml \
  -e /usr/share/openstack-tripleo-heat-templates/environments/ovs-hw-offload.yaml \
  -e ~/templates/environments/enable-tls.yaml \
  -e ~/templates/environments/overcloud-images.yaml \
  -e ~/templates/environments/keystone-domain-ad.yaml \
  -e ~/templates/environments/site-environment.yaml
