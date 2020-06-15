#!/bin/bash

target=/data/images
target=/iso
name=data
name=iso

mkdir -p ${target}
chcon -t virt_image_t ${target}

virsh pool-list --all
virsh pool-define-as ${name} dir null null null null ${target}
virsh pool-start ${name}
virsh pool-autostart ${name}
virsh pool-list --all
