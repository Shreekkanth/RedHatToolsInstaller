#!/bin/bash

service=osp10-undercloud
environment=lab

mkdir -p common/vars
touch common/vars/common.yml
mkdir -p common/roles/common

mkdir -p ${service}/hosts
touch ${service}/hosts/${environment}

mkdir -p ${service}/group_vars
touch ${service}/group_vars/all.yml

mkdir -p ${service}/group_vars/${environment}
mkdir -p ${service}/host_vars

mkdir -p ${service}/roles/common/tasks
mkdir -p ${service}/roles/common/handlers
mkdir -p ${service}/roles/common/templates
mkdir -p ${service}/roles/common/files
mkdir -p ${service}/roles/common/vars
mkdir -p ${service}/roles/common/defaults
mkdir -p ${service}/roles/common/meta

touch ${service}/site.yml
touch ${service}/${service}.yml
