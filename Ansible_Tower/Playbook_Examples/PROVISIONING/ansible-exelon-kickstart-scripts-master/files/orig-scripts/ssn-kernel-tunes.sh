#!/bin/bash

grep vm.swapiness=0 /etc/sysctl.conf
if [ $? -eq 1 ]
then
echo vm.swapiness=0 >> /etc/sysctl.conf
fi
echo "kernel.sem= 250 32000 200 128" >> /etc/sysctl.conf
echo "fs.file-max=65536" >>/etc/sysctl.conf
echo "fs.aio-max-nr=1048576" >>/etc/sysctl.conf
echo "net.ipv4.ip_local_port_range="1024 65000"" >>/etc/sysctl.conf
echo "## TCP IP Window Sizes, recieve and send" >> /etc/sysctl.conf
echo "net.core.rmem_default=8388608" >> /etc/sysctl.conf
echo "net.core.rmem_max=8388608" >> /etc/sysctl.conf
echo "net.core.wmem_default=8388608" >> /etc/sysctl.conf
echo "net.core.wmem_max=8388608" >> /etc/sysctl.conf

echo "## Some more TCP tunes" >> /etc/sysctl.conf
echo "#How often to send keep alive packets when a connection is unused" >> /etc/sysctl.conf
echo "net.ipv4.tcp_keepalive_time=10" >> /etc/sysctl.conf
echo "#How long the kernel waits in between probes" >> /etc/sysctl.conf
echo "net.ipv4.tcp_keepalive_intvl=1" >> /etc/sysctl.conf
echo "#How many probes are sent before a connection is considered broken" >> /etc/sysctl.conf
echo "net.ipv4.tcp_keepalive_probes=200" >> /etc/sysctl.conf
echo "#How many times to retry before killing the connection" >> /etc/sysctl.connf
echo "net.ipv4.tcp_retries2=3" >> /etc/sysctl.conf
echo "#How many times to retry transmitting the syn packet" >> /etc/sysctl.conf
echo "net.ipv4.tcp_syn_retries=2" >> /etc/sysctl.conf
echo "kernel.randomize_va_space = 1" >> /etc/sysctl.conf
echo "net.ipv4.conf.all.send_redirects = 0" >> /etc/sysctl.conf
echo "net.ipv4.conf.default.send_redirects = 0" >> /etc/sysctl.conf
echo "net.ipv4.conf.default.accept_redirects = 0" >> /etc/sysctl.conf
echo "net.ipv4.conf.default.secure_redirects = 0" >> /etc/sysctl.conf
echo "net.ipv4.icmp_echo_ignore_broadcasts = 1" >> /etc/sysctl.conf
echo "net.ipv4.tcp_syncookies = 1" >> /etc/sysctl.conf
echo "net.ipv4.conf.all.rp_filter = 1" >> /etc/sysctl.conf
echo "net.ipv4.conf.default.rp_filter = 1" >> /etc/sysctl.conf
echo "net.ipv4.tcp_timestamps = 0" >> /etc/sysctl.conf
echo "net.ipv4.tcp_sack = 1" >> /etc/sysctl.conf
echo "net.ipv4.tcp_window_scaling = 1" >> /etc/sysctl.conf
echo "net.core.netdev_max_backlog = 10000" >> /etc/sysctl.conf
echo "vm.swappiness = 60" >> /etc/sysctl.conf
echo "vm.dirty_background_ratio=3" >> /etc/sysctl.conf
echo "vm.dirty_ratio=15" >> /etc/sysctl.conf
echo "vm.dirty_expire_centisecs=500" >> /etc/sysctl.conf
echo "vm.dirty_writeback_centisecs=100" >> /etc/sysctl.conf
mem=$(free|grep Mem|awk '{print$2}')
totmem=$(echo "$mem*1024"|bc)
huge=$(grep Hugepagesize /proc/meminfo|awk '{print $2}')
max=$(echo "$totmem*75/100"|bc)
all=$(echo "$max/$huge"|bc)
echo "kernel.shmmax = $max" >> /etc/sysctl.conf
echo "kernel.shmall = $all" >> /etc/sysctl.conf
echo "kernel.sysrq = 1" >> /etc/sysctl.conf

