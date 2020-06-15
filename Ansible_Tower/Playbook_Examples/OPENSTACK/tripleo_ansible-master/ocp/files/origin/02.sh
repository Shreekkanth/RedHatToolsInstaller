#!/bin/bash

baseimagedir=/var/lib/libvirt/images
#imagedir=/ssd/images
imagedir=${baseimagedir}
base=centos7-base
prefix=origin

virsh attach-disk ${prefix}-infra1  ${imagedir}/${prefix}-infra1-docker.qcow2 vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk ${prefix}-infra2  ${imagedir}/${prefix}-infra2-docker.qcow2 vdb --driver qemu --subdriver qcow2 --config
