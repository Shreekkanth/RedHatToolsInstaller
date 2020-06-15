#!/bin/bash -x

if [ x"$#" != x"4" ]; then
	echo "$0 name cpu memMB storageGB"
	exit 1
fi
#NAME=rhel7-minimum
NAME=$1; shift

HNAM=$(echo $NAME|tr -s [:upper:] [:lower:]|sed -e 's/\./\-/g')
VARIANT=rhel7 # could refer this value on virt-install(1)
#ISO=/home/ori/rhel-server-7.0-x86_64-dvd.iso
#ISO=/srv/binaries/isos/RHEL/7/5/x86_64/default/rhel-server-7.2-x86_64-dvd.iso
#REPOSERVER=10.64.193.148
LOCATION=http://binaries.nrt.redhat.com/contents/RHEL/7/5/x86_64/default/


#CPU=2
#MEM=2048 #MB
#HDD=16   #GB
CPU=$1; shift
MEM=$1; shift
HDD=$1; shift

cat > ${NAME}-ks.cfg << EOF
#cdrom
firstboot --disable
ignoredisk --only-use=vda
# Keyboard layouts
keyboard --vckeymap=us --xlayouts='us'
# System language
lang en_US.UTF-8

# Network information
network --device=eth0 --onboot=yes --ipv6=auto --bootproto=dhcp
network  --hostname=${NAME}.osptest.local
# Root password
rootpw redhat
user --name=ori --groups=wheel --password=orimanabu --plaintext
# System timezone
timezone Asia/Tokyo
# System bootloader configuration
bootloader --location=mbr --boot-drive=vda
autopart --type=lvm
# Partition clearing information
clearpart --all --initlabel --drives=vda

%packages
@core
%end

%pre
%end


%post --nochroot

%end

%post
set -x -v
exec 1>/root/ks-post.log 2>&1
test -f /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release && \
    rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release || :

%end

reboot



EOF


virsh dominfo ${NAME} && \
{ virsh destroy ${NAME}; virsh detach-disk ${NAME} --target vda --persistent && virsh undefine ${NAME}; }

virt-install \
    --connect=qemu:///system \
    --accelerate \
    --noreboot \
    --hvm \
    --vcpus=${CPU} \
    --cpu=host \
    --name=${NAME} \
    --os-type=linux \
    --os-variant=${VARIANT} \
    --ram=${MEM} \
    --disk path=//var/lib/libvirt/images/${NAME}.qcow2,format=qcow2,size=${HDD},sparse=true \
    --force \
    --network=bridge:br0,model=virtio \
    --location=${LOCATION} \
    --nographics \
    --console pty,target_type=serial \
    --extra-args="text console=tty0 console=ttyS0,115200 serial rd_NO_PLYMOUTH ks=file:/${NAME}-ks.cfg" \
    --initrd-inject=$(pwd)/${NAME}-ks.cfg

#resize
