#!/bin/bash

nmcli con add type bridge ifname br0 con-name br0
nmcli con mod br0 bridge.stp no
nmcli con mod br0 ipv4.method auto 
nmcli con mod eno1 ipv4.method disabled ipv6.method disabled
nmcli con mod eno1 conn.master br0 conn.slave-type bridge
nmcli con down eno1
nmcli con up eno1
nmcli con up br0
