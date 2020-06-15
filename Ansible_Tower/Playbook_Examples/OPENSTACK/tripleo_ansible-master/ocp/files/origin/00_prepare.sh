#!/bin/bash

baseimagedir=/var/lib/libvirt/images
#imagedir=/ssd/images
imagedir=${baseimagedir}
base=centos7-base
prefix=origin
bridge=br0

qemu-img create -f qcow2 -b ${baseimagedir}/${base}.qcow2 ${imagedir}/${prefix}-ns.qcow2
qemu-img create -f qcow2 -b ${baseimagedir}/${base}.qcow2 ${imagedir}/${prefix}-lb.qcow2
qemu-img create -f qcow2 -b ${baseimagedir}/${base}.qcow2 ${imagedir}/${prefix}-master1.qcow2
qemu-img create -f qcow2 -b ${baseimagedir}/${base}.qcow2 ${imagedir}/${prefix}-master2.qcow2
qemu-img create -f qcow2 -b ${baseimagedir}/${base}.qcow2 ${imagedir}/${prefix}-master3.qcow2
qemu-img create -f qcow2 -b ${baseimagedir}/${base}.qcow2 ${imagedir}/${prefix}-infra1.qcow2
qemu-img create -f qcow2 -b ${baseimagedir}/${base}.qcow2 ${imagedir}/${prefix}-infra2.qcow2
qemu-img create -f qcow2 -b ${baseimagedir}/${base}.qcow2 ${imagedir}/${prefix}-node1.qcow2
qemu-img create -f qcow2 -b ${baseimagedir}/${base}.qcow2 ${imagedir}/${prefix}-node2.qcow2

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
build_xml ${prefix}-lb ${imagedir} 1024 2
build_xml ${prefix}-master1 ${imagedir} 6144 2
build_xml ${prefix}-master2 ${imagedir} 6144 2
build_xml ${prefix}-master3 ${imagedir} 6144 2
build_xml ${prefix}-infra1 ${imagedir} 4096 2
build_xml ${prefix}-infra2 ${imagedir} 4096 2
build_xml ${prefix}-node1 ${imagedir} 4096 2
build_xml ${prefix}-node2 ${imagedir} 4096 2

virsh define ${prefix}-ns.xml
virsh define ${prefix}-lb.xml
virsh define ${prefix}-master1.xml
virsh define ${prefix}-master2.xml
virsh define ${prefix}-master3.xml
virsh define ${prefix}-infra1.xml
virsh define ${prefix}-infra2.xml
virsh define ${prefix}-node1.xml
virsh define ${prefix}-node2.xml

qemu-img create -f qcow2 -o preallocation=metadata ${imagedir}/${prefix}-master1-docker.qcow2 10G
qemu-img create -f qcow2 -o preallocation=metadata ${imagedir}/${prefix}-master2-docker.qcow2 10G
qemu-img create -f qcow2 -o preallocation=metadata ${imagedir}/${prefix}-master3-docker.qcow2 10G
qemu-img create -f qcow2 -o preallocation=metadata ${imagedir}/${prefix}-infra1-docker.qcow2 10G
qemu-img create -f qcow2 -o preallocation=metadata ${imagedir}/${prefix}-infra2-docker.qcow2 10G
qemu-img create -f qcow2 -o preallocation=metadata ${imagedir}/${prefix}-node1-docker.qcow2 10G
qemu-img create -f qcow2 -o preallocation=metadata ${imagedir}/${prefix}-node2-docker.qcow2 10G

virsh attach-disk ${prefix}-master1 ${imagedir}/origin-master1-docker.qcow2   vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk ${prefix}-master2 ${imagedir}/origin-master2-docker.qcow2   vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk ${prefix}-master3 ${imagedir}/origin-master3-docker.qcow2   vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk ${prefix}-infra1  ${imagedir}/${prefix}-infra1-docker.qcow2 vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk ${prefix}-infra2  ${imagedir}/${prefix}-infra2-docker.qcow2 vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk ${prefix}-node1  ${imagedir}/${prefix}-node1-docker.qcow2  vdb --driver qemu --subdriver qcow2 --config
virsh attach-disk ${prefix}-node2  ${imagedir}/${prefix}-node2-docker.qcow2  vdb --driver qemu --subdriver qcow2 --config

qemu-img create -f qcow2 -o preallocation=metadata ${imagedir}/${prefix}-ns-add1.qcow2 40G
virsh attach-disk ${prefix}-ns ${imagedir}/${prefix}-ns-add1.qcow2 vdb --driver qemu --subdriver qcow2 --config

qemu-img create -f qcow2 -o preallocation=metadata ${imagedir}/${prefix}-master1-add1.qcow2 40G
qemu-img create -f qcow2 -o preallocation=metadata ${imagedir}/${prefix}-master2-add1.qcow2 40G
qemu-img create -f qcow2 -o preallocation=metadata ${imagedir}/${prefix}-master3-add1.qcow2 40G
virsh attach-disk ${prefix}-master1 ${imagedir}/origin-master1-add1.qcow2 vdc --driver qemu --subdriver qcow2 --config
virsh attach-disk ${prefix}-master2 ${imagedir}/origin-master2-add1.qcow2 vdc --driver qemu --subdriver qcow2 --config
virsh attach-disk ${prefix}-master3 ${imagedir}/origin-master3-add1.qcow2 vdc --driver qemu --subdriver qcow2 --config
