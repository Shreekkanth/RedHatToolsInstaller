#!/bin/bash

#qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/ns-var.qcow2 40G
#qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/ocp36-master1-var.qcow2 40G
#qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/ocp36-master2-var.qcow2 40G
#qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/ocp36-master3-var.qcow2 40G
#qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/ocp36-infra1-var.qcow2 40G
#qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/ocp36-infra2-var.qcow2 40G
#qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/ocp36-node1-var.qcow2 40G
#qemu-img create -f qcow2 -o preallocation=metadata /ssd/images/ocp36-node2-var.qcow2 40G
#
#virsh attach-disk ns /ssd/images/ns-var.qcow2 vdc --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp36-master1 /ssd/images/ocp36-master1-var.qcow2 vdc --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp36-master2 /ssd/images/ocp36-master2-var.qcow2 vdc --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp36-master3 /ssd/images/ocp36-master3-var.qcow2 vdc --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp36-infra1 /ssd/images/ocp36-infra1-var.qcow2 vdc --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp36-infra2 /ssd/images/ocp36-infra2-var.qcow2 vdc --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp36-node1 /ssd/images/ocp36-node1-var.qcow2 vdc --driver qemu --subdriver qcow2 --config
virsh attach-disk ocp36-node2 /ssd/images/ocp36-node2-var.qcow2 vdc --driver qemu --subdriver qcow2 --config
