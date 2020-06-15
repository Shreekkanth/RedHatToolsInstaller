#!/bin/bash

qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhel7-base.qcow2 /var/lib/libvirt/images/ocp311-ns.qcow2
qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhel7-base.qcow2 /var/lib/libvirt/images/ocp311-lb.qcow2
qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhel7-base.qcow2 /var/lib/libvirt/images/ocp311-master1.qcow2
qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhel7-base.qcow2 /var/lib/libvirt/images/ocp311-master2.qcow2
qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhel7-base.qcow2 /var/lib/libvirt/images/ocp311-master3.qcow2
qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhel7-base.qcow2 /var/lib/libvirt/images/ocp311-infra1.qcow2
qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhel7-base.qcow2 /var/lib/libvirt/images/ocp311-infra2.qcow2
qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhel7-base.qcow2 /var/lib/libvirt/images/ocp311-node1.qcow2
qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhel7-base.qcow2 /var/lib/libvirt/images/ocp311-node2.qcow2

function build_xml {
	local name=$1; shift
	local imagedir=$1; shift
	local mem=$1; shift
	local vcpu=$1; shift

	virt-install --ram ${mem} --vcpus ${vcpu} --os-variant rhel7 \
	--disk path=${imagedir}/${name}.qcow2,device=disk,bus=virtio,format=qcow2 \
	--noautoconsole --vnc \
	--network model=virtio,bridge=br0 \
	--network model=virtio,network=mgmt \
	--network model=virtio,network=tenant \
	--network model=virtio,network=external \
	--name ${name} \
	--cpu SandyBridge,+vmx \
	--dry-run --print-xml \
	> ${name}.xml
}

build_xml ocp311-ns /var/lib/libvirt/images 1024 1
build_xml ocp311-lb /var/lib/libvirt/images 1024 1
build_xml ocp311-master1 /var/lib/libvirt/images 4096 2
build_xml ocp311-master2 /var/lib/libvirt/images 4096 2
build_xml ocp311-master3 /var/lib/libvirt/images 4096 2
build_xml ocp311-infra1 /var/lib/libvirt/images 16384 2
build_xml ocp311-infra2 /var/lib/libvirt/images 16384 2
build_xml ocp311-node1 /var/lib/libvirt/images 8192 2
build_xml ocp311-node2 /var/lib/libvirt/images 8192 2

virsh define ocp311-ns.xml
virsh define ocp311-lb.xml
virsh define ocp311-master1.xml
virsh define ocp311-master2.xml
virsh define ocp311-master3.xml
virsh define ocp311-infra1.xml
virsh define ocp311-infra2.xml
virsh define ocp311-node1.xml
virsh define ocp311-node2.xml

qemu-img create -f qcow2 -o preallocation=metadata /var/lib/libvirt/images/ocp311-master1-var.qcow2 40G
qemu-img create -f qcow2 -o preallocation=metadata /var/lib/libvirt/images/ocp311-master2-var.qcow2 40G
qemu-img create -f qcow2 -o preallocation=metadata /var/lib/libvirt/images/ocp311-master3-var.qcow2 40G
qemu-img create -f qcow2 -o preallocation=metadata /var/lib/libvirt/images/ocp311-infra1-var.qcow2 40G
qemu-img create -f qcow2 -o preallocation=metadata /var/lib/libvirt/images/ocp311-infra2-var.qcow2 40G
qemu-img create -f qcow2 -o preallocation=metadata /var/lib/libvirt/images/ocp311-node1-var.qcow2 40G
qemu-img create -f qcow2 -o preallocation=metadata /var/lib/libvirt/images/ocp311-node2-var.qcow2 40G

virsh attach-disk ocp311-master1 /var/lib/libvirt/images/ocp311-master1-var.qcow2 vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp311-master2 /var/lib/libvirt/images/ocp311-master2-var.qcow2 vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp311-master3 /var/lib/libvirt/images/ocp311-master3-var.qcow2 vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp311-infra1 /var/lib/libvirt/images/ocp311-infra1-var.qcow2 vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp311-infra2 /var/lib/libvirt/images/ocp311-infra2-var.qcow2 vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp311-node1 /var/lib/libvirt/images/ocp311-node1-var.qcow2 vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp311-node2 /var/lib/libvirt/images/ocp311-node2-var.qcow2 vdb --driver qemu --subdriver qcow2 --config

qemu-img create -f qcow2 -o preallocation=metadata /var/lib/libvirt/images/ocp311-master1-docker.qcow2 20G
qemu-img create -f qcow2 -o preallocation=metadata /var/lib/libvirt/images/ocp311-master2-docker.qcow2 20G
qemu-img create -f qcow2 -o preallocation=metadata /var/lib/libvirt/images/ocp311-master3-docker.qcow2 20G
qemu-img create -f qcow2 -o preallocation=metadata /var/lib/libvirt/images/ocp311-infra1-docker.qcow2 20G
qemu-img create -f qcow2 -o preallocation=metadata /var/lib/libvirt/images/ocp311-infra2-docker.qcow2 20G
qemu-img create -f qcow2 -o preallocation=metadata /var/lib/libvirt/images/ocp311-node1-docker.qcow2 20G
qemu-img create -f qcow2 -o preallocation=metadata /var/lib/libvirt/images/ocp311-node2-docker.qcow2 20G

virsh attach-disk ocp311-master1 /var/lib/libvirt/images/ocp311-master1-docker.qcow2 vdc --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp311-master2 /var/lib/libvirt/images/ocp311-master2-docker.qcow2 vdc --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp311-master3 /var/lib/libvirt/images/ocp311-master3-docker.qcow2 vdc --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp311-infra1 /var/lib/libvirt/images/ocp311-infra1-docker.qcow2 vdc --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp311-infra2 /var/lib/libvirt/images/ocp311-infra2-docker.qcow2 vdc --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp311-node1 /var/lib/libvirt/images/ocp311-node1-docker.qcow2 vdc --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp311-node2 /var/lib/libvirt/images/ocp311-node2-docker.qcow2 vdc --driver qemu --subdriver qcow2 --config
