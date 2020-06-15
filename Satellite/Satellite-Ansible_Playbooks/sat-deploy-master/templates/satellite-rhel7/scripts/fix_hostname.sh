#!/bin/bash

echo "Configuring HOSTNAME: $HOSTNAME"
sed -i -r -e "s/^(HOSTNAME=)localhost\.localdomain/\1$HOSTNAME/" /etc/sysconfig/network
hostname $HOSTNAME
echo $HOSTNAME > /etc/hostname
echo 127.0.0.1 `hostname` `hostname -s` >> /etc/hosts
echo "HOSTNAME configured"
