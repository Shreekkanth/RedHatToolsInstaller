#!/bin/bash

baseimagedir=/var/lib/libvirt/images
#imagedir=/ssd/images
imagedir=${baseimagedir}
base=centos7-base
prefix=origin

#qemu-img create -f qcow2 -b ${baseimagedir}/${base}.qcow2 ${imagedir}/${prefix}-ns.qcow2
#qemu-img create -f qcow2 -b ${baseimagedir}/${base}.qcow2 ${imagedir}/${prefix}-lb.qcow2
#qemu-img create -f qcow2 -b ${baseimagedir}/${base}.qcow2 ${imagedir}/${prefix}-master1.qcow2
#qemu-img create -f qcow2 -b ${baseimagedir}/${base}.qcow2 ${imagedir}/${prefix}-master2.qcow2
#qemu-img create -f qcow2 -b ${baseimagedir}/${base}.qcow2 ${imagedir}/${prefix}-master3.qcow2
#qemu-img create -f qcow2 -b ${baseimagedir}/${base}.qcow2 ${imagedir}/${prefix}-infra1.qcow2
#qemu-img create -f qcow2 -b ${baseimagedir}/${base}.qcow2 ${imagedir}/${prefix}-infra2.qcow2
#qemu-img create -f qcow2 -b ${baseimagedir}/${base}.qcow2 ${imagedir}/${prefix}-node1.qcow2
#qemu-img create -f qcow2 -b ${baseimagedir}/${base}.qcow2 ${imagedir}/${prefix}-node2.qcow2
#
#function build_xml {
#	local name=$1; shift
#	local imagedir=$1; shift
#	local mem=$1; shift
#	local vcpu=$1; shift
#
#	virt-install --ram ${mem} --vcpus ${vcpu} --os-variant rhel7 \
#	--disk path=${imagedir}/${name}.qcow2,device=disk,bus=virtio,format=qcow2 \
#	--noautoconsole --vnc \
#	--network model=virtio,bridge=br1 \
#	--network model=virtio,network=mgmt \
#	--network model=virtio,network=tenant \
#	--network model=virtio,network=external \
#	--name ${name} \
#	--cpu SandyBridge,+vmx \
#	--dry-run --print-xml \
#	> ${name}.xml
#}
#
#build_xml ${prefix}-ns ${imagedir} 1024 2
#build_xml ${prefix}-lb ${imagedir} 1024 2
#build_xml ${prefix}-master1 ${imagedir} 6144 2
#build_xml ${prefix}-master2 ${imagedir} 6144 2
#build_xml ${prefix}-master3 ${imagedir} 6144 2
#build_xml ${prefix}-infra1 ${imagedir} 4096 2
#build_xml ${prefix}-infra2 ${imagedir} 4096 2
#build_xml ${prefix}-node1 ${imagedir} 4096 2
#build_xml ${prefix}-node2 ${imagedir} 4096 2

virsh define ${prefix}-ns.xml


qemu-img create -f qcow2 -o preallocation=metadata ${imagedir}/${prefix}-ns-add1.qcow2 40G
virsh attach-disk ${prefix}-ns ${imagedir}/${prefix}-ns-add1.qcow2 vdb --driver qemu --subdriver qcow2 --config

