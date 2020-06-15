last_octet=121

interface=eth1
addr=10.0.1.${last_octet}
nmcli con del ${interface}
nmcli con add type ethernet ifname ${interface} con-name ${interface}
nmcli con mod ${interface} ipv4.method manual ipv4.address ${addr}/24
nmcli con down ${interface}
nmcli con up ${interface}

interface=eth2
addr=10.0.2.${last_octet}
nmcli con del ${interface}
nmcli con add type ethernet ifname ${interface} con-name ${interface}
nmcli con mod ${interface} ipv4.method manual ipv4.address ${addr}/24
nmcli con down ${interface}
nmcli con up ${interface}

interface=eth3
addr=172.16.99.${last_octet}
nmcli con del ${interface}
nmcli con add type ethernet ifname ${interface} con-name ${interface}
nmcli con mod ${interface} ipv4.method manual ipv4.address ${addr}/24 ipv4.gateway 172.16.99.254 ipv4.dns 172.16.99.254
nmcli con down ${interface}
nmcli con up ${interface}

nmcli con down eth0
nmcli con mod eth0 connection.autoconnect no

