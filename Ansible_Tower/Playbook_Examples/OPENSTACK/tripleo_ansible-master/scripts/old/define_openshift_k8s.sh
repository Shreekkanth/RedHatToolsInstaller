#!/bin/bash

qemu-img create -f qcow2 -b /var/lib/libvirt/images/centos7-base.qcow2 /ssd/images/k8s2-master1.qcow2
#qemu-img create -f qcow2 -b /var/lib/libvirt/images/centos7-base.qcow2 /ssd/images/k8s2-master2.qcow2
#qemu-img create -f qcow2 -b /var/lib/libvirt/images/centos7-base.qcow2 /ssd/images/k8s2-master3.qcow2
qemu-img create -f qcow2 -b /var/lib/libvirt/images/centos7-base.qcow2 /ssd/images/k8s2-node1.qcow2
qemu-img create -f qcow2 -b /var/lib/libvirt/images/centos7-base.qcow2 /ssd/images/k8s2-node2.qcow2

function build_xml {
	local name=$1; shift
	local imagedir=$1; shift
	local mem=$1; shift
	local vcpu=$1; shift

	virt-install --ram ${mem} --vcpus ${vcpu} --os-variant rhel7 \
	--disk path=${imagedir}/${name}.qcow2,device=disk,bus=virtio,format=qcow2 \
	--noautoconsole --vnc \
	--network model=virtio,bridge=br1 \
	--network model=virtio,network=mgmt \
	--network model=virtio,network=tenant \
	--network model=virtio,network=external \
	--name ${name} \
	--cpu SandyBridge,+vmx \
	--dry-run --print-xml \
	> ${name}.xml
}

build_xml k8s2-master1 /ssd/images 4096 2
#build_xml k8s2-master2 /ssd/images 4096 2
#build_xml k8s2-master3 /ssd/images 4096 2
build_xml k8s2-node1 /ssd/images 4096 2
build_xml k8s2-node2 /ssd/images 4096 2

virsh define k8s2-master1.xml
#virsh define k8s2-master2.xml
#virsh define k8s2-master3.xml
virsh define k8s2-node1.xml
virsh define k8s2-node2.xml

qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/k8s2-master1-add1.qcow2 10G
#qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/k8s2-master2-add1.qcow2 10G
#qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/k8s2-master3-add1.qcow2 10G
qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/k8s2-node1-docker.qcow2 10G
qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/k8s2-node2-docker.qcow2 10G

virsh attach-disk k8s2-master1 /ssd/images/k8s2-master1-add1.qcow2 vdb --driver qemu --subdriver qcow2 --config
#virsh attach-disk k8s2-master2 /ssd/images/k8s2-master2-add1.qcow2 vdb --driver qemu --subdriver qcow2 --config
#virsh attach-disk k8s2-master3 /ssd/images/k8s2-master3-add1.qcow2 vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk k8s2-node1 /ssd/images/k8s2-node1-docker.qcow2 vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk k8s2-node2 /ssd/images/k8s2-node2-docker.qcow2 vdb --driver qemu --subdriver qcow2 --config
