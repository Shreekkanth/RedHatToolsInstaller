prefix=origin
dns=172.16.99.11
basename=lb
last_octet=20
hostnamectl set-hostname ${prefix}-${basename}.osetest.local
interface=eth1
addr=10.0.1.${last_octet}
nmcli con del 'Wired connection 1'
nmcli con add type ethernet ifname ${interface} con-name ${interface}
nmcli con mod ${interface} ipv4.method manual ipv4.address ${addr}/24 connection.autoconnect yes
nmcli con down ${interface}
nmcli con up ${interface}

interface=eth2
addr=10.0.2.${last_octet}
nmcli con del 'Wired connection 2'
nmcli con add type ethernet ifname ${interface} con-name ${interface}
nmcli con mod ${interface} ipv4.method manual ipv4.address ${addr}/24 connection.autoconnect yes
nmcli con down ${interface}
nmcli con up ${interface}

interface=eth3
addr=172.16.99.${last_octet}
nmcli con del 'Wired connection 3'
nmcli con add type ethernet ifname ${interface} con-name ${interface}
nmcli con mod ${interface} ipv4.method manual ipv4.address ${addr}/24 ipv4.gateway 172.16.99.254 ipv4.dns ${dns} connection.autoconnect yes
nmcli con down ${interface}
nmcli con up ${interface}

nmcli con mod eth0 connection.autoconnect no
nmcli con down eth0
sed -i -e '/^UUID=.*/d' /etc/sysconfig/network-scripts/ifcfg-eth0
