#!/bin/bash

qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhel7-base.qcow2 /ssd/images/ns.qcow2
qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhel7-base.qcow2 /ssd/images/ocp36-lb.qcow2
qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhel7-base.qcow2 /ssd/images/ocp36-master1.qcow2
qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhel7-base.qcow2 /ssd/images/ocp36-master2.qcow2
qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhel7-base.qcow2 /ssd/images/ocp36-master3.qcow2
qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhel7-base.qcow2 /ssd/images/ocp36-infra1.qcow2
qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhel7-base.qcow2 /ssd/images/ocp36-infra2.qcow2
qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhel7-base.qcow2 /ssd/images/ocp36-node1.qcow2
qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhel7-base.qcow2 /ssd/images/ocp36-node2.qcow2

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

build_xml ns /ssd/images 1024 2
build_xml ocp36-lb /ssd/images 1024 2
build_xml ocp36-master1 /ssd/images 4096 2
build_xml ocp36-master2 /ssd/images 4096 2
build_xml ocp36-master3 /ssd/images 4096 2
build_xml ocp36-infra1 /ssd/images 2048 2
build_xml ocp36-infra2 /ssd/images 2048 2
build_xml ocp36-node1 /ssd/images 2048 2
build_xml ocp36-node2 /ssd/images 2048 2

virsh define ns.xml
virsh define ocp36-lb.xml
virsh define ocp36-master1.xml
virsh define ocp36-master2.xml
virsh define ocp36-master3.xml
virsh define ocp36-infra1.xml
virsh define ocp36-infra2.xml
virsh define ocp36-node1.xml
virsh define ocp36-node2.xml

qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/ocp36-master1-docker.qcow2 10G
qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/ocp36-master2-docker.qcow2 10G
qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/ocp36-master3-docker.qcow2 10G
qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/ocp36-infra1-docker.qcow2 10G
qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/ocp36-infra2-docker.qcow2 10G
qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/ocp36-node1-docker.qcow2 10G
qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/ocp36-node2-docker.qcow2 10G

virsh attach-disk ocp36-master1 /ssd/images/ocp36-master1-docker.qcow2 vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp36-master2 /ssd/images/ocp36-master2-docker.qcow2 vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp36-master3 /ssd/images/ocp36-master3-docker.qcow2 vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp36-infra1 /ssd/images/ocp36-infra1-docker.qcow2 vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp36-infra2 /ssd/images/ocp36-infra2-docker.qcow2 vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp36-node1 /ssd/images/ocp36-node1-docker.qcow2 vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp36-node2 /ssd/images/ocp36-node2-docker.qcow2 vdb --driver qemu --subdriver qcow2 --config
