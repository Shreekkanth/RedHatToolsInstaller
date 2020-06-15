#remove network mac and interface information
sed -i '/HWADDR/d' /etc/sysconfig/network-scripts/ifcfg-eth0
sed -i "/^UUID/d" /etc/sysconfig/network-scripts/ifcfg-eth0
echo "DEVICE='eth0'" >> /etc/sysconfig/network-scripts/ifcfg-eth0

#remove any ssh keys or persistent routes, dhcp leases
subscription-manager unregister || true
subscription-manager clean
rm -f /etc/ssh/ssh_host_*
rm -f /etc/udev/rules.d/70-persistent-net.rules
rm -f /var/lib/dhclient/dhclient-eth0.leases
rm -rf /tmp/*
yum -y erase 'katello-ca-consumer-*'
yum -y clean all
rm -rf /var/cache/yum

#disable reverse dns lookups on sshd
echo "UseDNS no" >> /etc/ssh/sshd_config

#run fstrim
fstrim -va
