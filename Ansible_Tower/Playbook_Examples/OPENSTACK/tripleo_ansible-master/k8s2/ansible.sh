ansible -i hosts/lab all_nodes -u root -m shell -a 'nmcli c down eth3; nmcli c mod eth3 ipv4.dns 172.16.99.254; nmcli c up eth3'
ansible -i hosts/lab all_nodes -u root -m shell -a 'nmcli con mod eth3 ipv4.gateway ""; nmcli con mod eth1 ipv4.gateway 10.0.1.254; systemctl restart network; ip r'
ansible -i hosts/lab all_nodes -u root -m shell -a 'traceroute -n www.google.com'
