#!/bin/bash

if [ x"$#" != x"3" ]; then
	echo "$0 op prefix version"
	exit 1
fi
op=$1; shift
prefix=$1; shift
version=$1; shift
imagedir=/var/lib/libvirt/images
net_provisioning=foreman
net_external=external
mac_vendor="52:54:00"

kvm_host=whaleshark.nrt.redhat.com
bmc_user=admin
bmc_password=password
bmc_port_start=6230
declare -A vbmc

num_ctrl=3
mem_ctrl=12288
vcpu_ctrl=4

num_comp=2
mem_comp=8192
vcpu_comp=2

num_ceph=3
mem_ceph=8192
vcpu_ceph=2

num_networker=0
mem_networker=4096
vcpu_networker=2

if [ x"${op}" = x"instackenv.json" ]; then
	rm -f /tmp/instackenv.json
	cat >> /tmp/instackenv.json <<END
{
  "nodes": [
END
fi

bmc_port=${bmc_port_start}
for type in ctrl comp ceph networker; do
	#echo "=> type: ${type}"
	mac_tmp=$(printf "%x" ${version})
	case ${type} in
	ctrl)
		num_nodes=${num_ctrl}
		mem=${mem_ctrl}
		vcpu=${vcpu_ctrl}
		mac_prefix="${mac_vendor}:${mac_tmp}1"
		;;
	comp)
		num_nodes=${num_comp}
		mem=${mem_comp}
		vcpu=${vcpu_comp}
		mac_prefix="${mac_vendor}:${mac_tmp}2"
		;;
	ceph)
		num_nodes=${num_ceph}
		mem=${mem_ceph}
		vcpu=${vcpu_ceph}
		mac_prefix="${mac_vendor}:${mac_tmp}3"
		;;
	networker)
		num_nodes=${num_networker}
		mem=${mem_networker}
		vcpu=${vcpu_networker}
		mac_prefix="${mac_vendor}:${mac_tmp}4"
		;;
	esac

	if [ x"${num_nodes}" = x"0" ]; then
		continue
	fi

	for i in $(seq 1 ${num_nodes}); do
		j=$(printf "%02d" ${i})
		node=${type}${j}
		dom=${prefix}-${node}
		#echo "==> node: ${node}, domain=${dom}, mac=${mac}"

		case ${op} in
		create)
			virsh list --all | grep ${dom} > /dev/null 2>&1
			if [ x"$?" = x"0" ]; then
				echo "domain ${dom} exists, skip..."
				continue
			fi

			if [ ! -f ${imagedir}/${dom}.qcow2 ]; then
				echo "===> creating qcow2 image"
				qemu-img create -f qcow2 -o preallocation=metadata ${imagedir}/${dom}.qcow2 60G;
			fi

			opt_disk=""
			if [ x"${type}" = x"ceph" ]; then
				if [ ! -f ${imagedir}/${dom}-storage.qcow2 ]; then
					echo "===> creating qcow2 image"
					qemu-img create -f qcow2 -o preallocation=metadata ${imagedir}/${dom}-storage.qcow2 60G;
				fi
				opt_disk="--disk path=${imagedir}/${dom}-storage.qcow2,device=disk,bus=virtio,format=qcow2"
			fi

			cmd="virt-install --ram ${mem} --vcpus ${vcpu} --os-variant rhel7 \
			--disk path=${imagedir}/${dom}.qcow2,device=disk,bus=virtio,format=qcow2 \
			${opt_disk} \
			--noautoconsole --vnc
			--network model=virtio,mac=${mac_prefix}:aa:${j},network=${net_provisioning} \
			--network model=virtio,mac=${mac_prefix}:bb:${j},network=${net_external} \
			--network model=virtio,mac=${mac_prefix}:cc:${j},network=${net_external} \
			--name ${dom} \
			--cpu SandyBridge,+vmx \
			--dry-run --print-xml"

			#echo ${cmd}
			${cmd} > /tmp/${dom}.xml
			virsh define --file /tmp/${dom}.xml
			;;
		delete)
			virsh destroy ${dom}
			virsh undefine ${dom} --remove-all-storage
			;;
		vbmc)
			#echo "vbmc add ${dom} --port ${bmc_port} --username ${bmc_user} --password ${bmc_password}"
			#echo "vbmc start ${dom}"
			vbmc["${dom}"]="${bmc_port}"
			;;
		instackenv.json)
			cat >> /tmp/instackenv.json <<END
    {
      "name": "${dom}",
      "mac": [ "${mac_prefix}:aa:${j}" ],
      "pm_type": "ipmi",
      "pm_addr": "${kvm_host}",
      "pm_user": "${bmc_user}",
      "pm_password": "${bmc_password}",
      "pm_port": "${bmc_port}"
    },
END
			;;
		*)
			echo "unknown op: ${op}"
			;;
		esac
		(( bmc_port = bmc_port + 1 ))
	done
done

(( bmc_port_end = bmc_port - 1 ))

if [ x"${op}" = x"vbmc" ]; then
	cat <<END
#!/bin/bash

if [ x"\$#" != x"1" ]; then
	echo "\${0} op"
	exit 1
fi
op=\$1; shift

case \${op} in
add)
END
	for dom in ${!vbmc[*]}; do
		echo "	sudo vbmc add ${dom} --port ${vbmc[${dom}]} --username ${bmc_user} --password ${bmc_password}"
	done
	cat <<END
	;;
delete)
	for i in \$(vbmc list -c 'Domain name' -f value); do vbmc delete \$i; done
	ps ax | grep vbmc | grep -v grep | awk '{print $1}' | xargs kill -9
	;;
start)
END
	for dom in ${!vbmc[*]}; do
		echo "	sudo vbmc start ${dom}"
	done
	cat <<END
	;;
stop)
END
	for dom in ${!vbmc[*]}; do
		echo "	sudo vbmc stop ${dom}"
	done
	cat <<END
	;;
firewall-cmd)
END
	for dom in ${!vbmc[*]}; do
		echo "#	sudo firewall-cmd --add-port ${vbmc[${dom}]}/udp"
		echo "#	sudo firewall-cmd --add-port ${vbmc[${dom}]}/udp --permanent"
	done
	echo "	sudo firewall-cmd --add-port ${bmc_port_start}-${bmc_port_end}/udp"
	echo "	sudo firewall-cmd --add-port ${bmc_port_start}-${bmc_port_end}/udp --permanent"
	cat <<END
	;;
iptables)
END
	for dom in ${!vbmc[*]}; do
		echo "#	sudo iptables -I INPUT 1 -p udp -m udp --dport ${vbmc[${dom}]} -m conntrack --ctstate NEW,UNTRACKED -j ACCEPT"
	done
	echo "	sudo iptables -I INPUT 1 -p udp -m udp --dport ${bmc_port_start}:${bmc_port_end} -m conntrack --ctstate NEW,UNTRACKED -j ACCEPT"
	cat <<END
	;;
ipmitool)
END
	for dom in ${!vbmc[*]}; do
		echo "	echo \"=> ${dom}	${vbmc[${dom}]}\"; ipmitool -I lanplus -H whaleshark.nrt.redhat.com -p ${vbmc[${dom}]} -U ${bmc_user} -P ${bmc_password} chassis power status"
	done
	cat <<END
	;;
*)
	echo "unknown op: \${op}"
	exit 1
	;;
esac
END
fi

if [ x"${op}" = x"instackenv.json" ]; then
	cat >> /tmp/instackenv.json <<END
  ]
}
END
	cat /tmp/instackenv.json | perl -e 'for (<>) {chomp; if ($_ eq "  ]") { $prev =~ s/,$//; } print "$prev\n"; $prev = $_;}; print "$prev\n";'
fi
