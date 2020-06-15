dns=172.16.99.11
hostnamectl set-hostname ocp36-node2.osetest.local
last_octet=42
interface=eth1
addr=10.0.1.${last_octet}
#nmcli con del ${interface}
#nmcli con add type ethernet ifname ${interface} con-name ${interface}
nmcli con mod ${interface} ipv4.method manual ipv4.address ${addr}/24 connection.autoconnect yes
nmcli con down ${interface}
nmcli con up ${interface}

interface=eth2
addr=10.0.2.${last_octet}
#nmcli con del ${interface}
#nmcli con add type ethernet ifname ${interface} con-name ${interface}
nmcli con mod ${interface} ipv4.method manual ipv4.address ${addr}/24 connection.autoconnect yes
nmcli con down ${interface}
nmcli con up ${interface}

interface=eth3
addr=172.16.99.${last_octet}
#nmcli con del ${interface}
#nmcli con add type ethernet ifname ${interface} con-name ${interface}
nmcli con mod ${interface} ipv4.method manual ipv4.address ${addr}/24 ipv4.gateway 172.16.99.254 ipv4.dns ${dns} connection.autoconnect yes
nmcli con down ${interface}
nmcli con up ${interface}



