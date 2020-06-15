#!/usr/bin/env bash
if [ $PWD != $HOME ] ; then echo "USAGE: $0 Must be run from $HOME"; exit 1 ; fi

source ~/stackrc
cd ~

stack_name={{ stack_name }}

time openstack overcloud update converge --templates \
  --stack $stack_name \
  -n ~/templates/network_data.yaml \
  {{ overcloud_deploy_templates | join (' \\\n') | indent(width = 2) }}
