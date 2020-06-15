#!/bin/bash

declare -a servers=(
"10.0.1.121"
"10.0.1.122"
"10.0.1.123"
)

my_addr=$(ip -4 -o addr show dev eth1 | awk '{print $4}' | sed -e 's,/.*,,')
cluster=""
#for fqdn in ${servers[@]}; do
#	short=$(echo ${fqdn} | sed -e 's/\..*$//')
#	name=etcd-${short}
#	cluster="${cluster},${name}=http://${fqdn}:2380"
#done

my_index=0
for addr in ${servers[@]}; do
	if [ x"${addr}" = x"${my_addr}" ]; then
		break
	fi
	((my_index = my_index + 1))
done

index=0
for addr in ${servers[@]}; do
	name=etcd${index}
	cluster="${cluster},${name}=http://${addr}:2380"
	((index = index + 1))
done
cluster=$(echo ${cluster} | sed -e 's/^,//')

cmd=$(echo "
docker run -d \
--restart always \
-v /etc/ssl/certs:/etc/ssl/certs \
-v /var/lib/etcd-cluster:/var/lib/etcd \
-p 4001:4001 \
-p 2380:2380 \
-p 2379:2379 \
--name etcd \
gcr.io/google_containers/etcd-amd64:3.0.17 \
etcd --name=etcd${my_index} \
--advertise-client-urls=http://${my_addr}:2379,http://${my_addr}:4001 \
--listen-client-urls=http://0.0.0.0:2379,http://0.0.0.0:4001 \
--initial-advertise-peer-urls=http://${my_addr}:2380 \
--listen-peer-urls=http://0.0.0.0:2380 \
--initial-cluster-token=9477af68bbee1b9ae037d6fd9e7efefd \
--initial-cluster=${cluster} \
--initial-cluster-state=new \
--auto-tls \
--peer-auto-tls \
--data-dir=/var/lib/etcd
")
echo ${cmd}
eval ${cmd}
