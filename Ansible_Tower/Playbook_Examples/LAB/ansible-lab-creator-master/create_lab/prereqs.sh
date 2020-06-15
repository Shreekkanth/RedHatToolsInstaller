#!/bin/bash

# Run this script before the ansible. All this does is setup the subscriptions you require

ORG_ID=$1
AK_NAME=$2

subscription-manager register --org=$ORG_ID --activationkey=$AK_NAME
subscription-manager attach --auto
subscription-manager repos --disable=*
subscription-manager repos --enable=rhel-7-server-rpms --enable=rhel-7-server-extras-rpms --enable=rhel-7-server-ansible-2.7-rpms

yum install -y ansible wget screen


#mkdir -p /var/lib/libvirt/
#mkdir -p /home/libvirt/images
#ln -s /home/libvirt/images /var/lib/libvirt/images
#ls -al /var/lib/libvirt/
#restorecon -Rvv /var/lib/libvirt


#eof
