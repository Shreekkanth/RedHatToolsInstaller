#!/usr/bin/env bash

source ~/stackrc;
cd ~;

openstack overcloud container image prepare \
  --namespace satellite-01.rich.sea.com:5000 \
  --prefix sea-osp13_containers- \
  --tag-from-label {version}-{release} \
  -e /usr/share/openstack-tripleo-heat-templates/environments/network-isolation.yaml \
  -e /usr/share/openstack-tripleo-heat-templates/environments/network-environment.yaml \
  -e /usr/share/openstack-tripleo-heat-templates/environments/neutron-sriov.yaml \
  -e /usr/share/openstack-tripleo-heat-templates/environments/host-config-and-reboot.yaml \
  -e /usr/share/openstack-tripleo-heat-templates/environments/ssl/tls-endpoints-public-ip.yaml \
  -e /home/stack/templates/environments/misc-host-settings.yaml \
  -e /home/stack/templates/environments/storage-environment.yaml \
  -e /home/stack/templates/environments/site-environment.yaml \
  -e ~/templates/environments/neutron-sriov.yaml \
  -e ~/templates/environments/enable-tls.yaml \
  -e ~/templates/environments/inject-trust-anchor.yaml \
  --roles-file ~/templates/roles_data.yaml \
  --output-env-file /home/stack/templates/environments/overcloud-images.yaml
