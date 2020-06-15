for vm in origin-ns origin-lb origin-master1 origin-master2 origin-master3 origin-infra1 origin-infra2 origin-node1 origin-node2; do virsh start ${vm}; done
