nmcli con mod eth3 ipv4.gateway ''
nmcli con mod eth1 ipv4.gateway 10.0.1.254
systemctl restart network
ip r
traceroute -n www.google.com
