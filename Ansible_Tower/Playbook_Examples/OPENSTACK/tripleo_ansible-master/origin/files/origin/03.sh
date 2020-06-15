#!/bin/bash

baseimagedir=/var/lib/libvirt/images
#imagedir=/ssd/images
imagedir=${baseimagedir}
base=centos7-base
prefix=origin
bridge=br0

function build_xml {
	local name=$1; shift
	local imagedir=$1; shift
	local mem=$1; shift
	local vcpu=$1; shift

	virt-install --ram ${mem} --vcpus ${vcpu} --os-variant rhel7 \
	--disk path=${imagedir}/${name}.qcow2,device=disk,bus=virtio,format=qcow2 \
	--noautoconsole --vnc \
	--network model=virtio,bridge=${bridge} \
	--network model=virtio,network=mgmt \
	--network model=virtio,network=tenant \
	--network model=virtio,network=external \
	--name ${name} \
	--cpu SandyBridge,+vmx \
	--dry-run --print-xml \
	> ${name}.xml
}

build_xml ${prefix}-ns ${imagedir} 1024 2
virsh define ${prefix}-ns.xml

virsh attach-disk ${prefix}-ns ${imagedir}/${prefix}-ns-add1.qcow2 vdb --driver qemu --subdriver qcow2 --config
