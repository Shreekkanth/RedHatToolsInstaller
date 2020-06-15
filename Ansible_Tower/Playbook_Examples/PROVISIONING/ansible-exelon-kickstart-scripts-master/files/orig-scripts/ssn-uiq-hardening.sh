#!/bin/ksh


#  Script to harden Redhat (RH) UIQ host BEFORE it goes into the DMZ.
#  Copy this script into {host}:/var/tmp/ and run on the host itself

#  G Sarnaik 030413

###########################################################################

# disables from /etc/services
disable_services()
{
  services_turn_offs="imap|\
pop|\
amanda|\
amandaidx|\
amidxtape|\
^appserv|\
^auth|\
chargen|\
cvspserver|\
daytime|\
discard|\
^echo|\
eklogin|\
klogin|\
kshell|\
ktalk|\
^ftp|\
xfs|\
^imq*|\
^ipp|\
^slp|\
^sql|\
^kerberos|\
mobileip-agent|\
mobile-ip|\
nfs|\
nfsd|\
talk|\
finger|\
tcpmux|\
telnet|\
tftp|\
^time|\
uucp|\
sendmail|\
DHCP|\
dhcp"

  egrep -v "${services_turn_offs}" ${HARD_DIR}/services.before_hardening > /etc/services
}

RH_disable_chkconfig()
{
  chkconfig_turn_offs="gssftp \
    netfs \
    nfs \
    nfslock \
    NetworkManager \
    tcpmux-server \
    ekrb5-telnet \
    krb5-telnet \
    daytime-dgram \
    daytime-stream \
    iptables \
    time-dgram \
    time-stream"

  for i in ${chkconfig_turn_offs}
  do
    chkconfig --level 123456 ${i} off
  done
}

RH_disable_GUI()
{
  turn_offs=`awk '/5:on/ {print $1}' ${HARD_DIR}/chkconfig.before_hardening`
  for proc in ${turn_offs}
  do
    chkconfig --level 5 ${proc} off
  done

  # remove "x:5:respawn:/etc/X11/prefdm -nodaemon" from /etc/inittab
  grep -v X11 ${HARD_DIR}/inittab.before_hardening > /etc/inittab

  # remove X11 server
  #rpm -e `rpm -qa|grep ^xorg-x11-server`
  yum -y groupremove "X Window System"

}

RH_remove_samba()
{
   yum -y erase samba
}


RH_auditing()
{
  # get kernel line with either a tab or multiple spaces
  sed -i '/^    kernel/s|$| audit=1|' /boot/grub/grub.conf
  sed -i '/^ *kernel/s|$| audit=1|' /boot/grub/grub.conf

  # Add the following lines to the /etc/audit/audit.rules file:
  echo >> /etc/audit/audit.rules
  echo "# system logs" >> /etc/audit/audit.rules
  echo "-w /var/log/faillog -p wa -k logins" >> /etc/audit/audit.rules
  echo "-w /var/log/lastlog -p wa -k logins" >> /etc/audit/audit.rules
  echo "-w /var/log/tallylog -p wa -k logins" >> /etc/audit/audit.rules
  echo "-w /var/log/btmp -p wa -k session" >> /etc/audit/audit.rules
}

RH_privileged_commands()
{
  echo >> /etc/audit/audit.rules
  echo "# privileged commands" >> /etc/audit/audit.rules
  for P in `grep ext3 /etc/fstab | awk '{print $2}'`
  do
    find $P -xdev \( -perm -4000 -o -perm -2000 \) -type f | awk '{print "-a always,exit -F path=" $1 " -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged" }' >> /etc/audit/audit.rules
  done
}

RH_log_rotate()
{
  # change log rotation to 180 days and compress
  sed -e 's/rotate 4/rotate 25/' -e 's/#compress/compress/' ${HARD_DIR}/logrotate.conf.before_hardening > /etc/logrotate.conf
}

RH_lock_system_accounts()
{
  for acct in `cut -d: -f1 /etc/passwd`
  do
    acct_uid=`id -u $acct`
    if [ $acct_uid -lt 500 -a $acct != "root" ]
    then
      state=`passwd -S $acct | awk '{print $2}'`
      [ "$state" != "LK" ] && passwd -l $acct
    fi
  done
}

RH_sshd_config()
{
  # configure /etc/ssh/sshd_config to disable rhosts and deny root logins other than console
  sed -e 's/#IgnoreRhosts/IgnoreRhosts/' \
      -e 's/#PermitRootLogin yes/PermitRootLogin no/' \
      -e 's/#RSAAuthentication yes/RSAAuthentication yes/' \
      -e 's/#ClientAliveInterval 600/ClientAliveInterval 0/' \
      -e 's/#ClientAliveCountMax 3/ClientAliveCountMax 0/' \
      ${HARD_DIR}/sshd_config.before_hardening > /etc/ssh/sshd_config
          echo "Ciphers aes256-ctr,aes192-ctr,aes128-ctr,arcfour256,aes128-cbc" >> /etc/ssh/sshd_config
          service sshd restart
}

RH_sshd_banner()
{
        sed -i 's,^#Banner /some/path,Banner /etc/ssh/sshd-banner,' /etc/ssh/sshd_config
}

RH_at_cron_deny()
{
  rm -f /etc/at.deny /etc/cron.deny
}

RH_daemon_umask()
{
  echo "# Set daemon umask" >> /etc/sysconfig/init
  echo "umask 027" >> /etc/sysconfig/init
}


RH_fstab()
{
  sed -e '/tmpfs/ s/defaults/defaults,nodev/' \
      -e '/tmp/ s/defaults/defaults,nosuid/' ${HARD_DIR}/fstab.before_hardening > /etc/fstab
}

RH_files_remove()
{
  rm -rf /etc/auto.* \
   /etc/init.d/httpd \
   /etc/build.cfg
}

RH_sudoers_audit()
{
  # Add the following lines to the /etc/audit/audit.rules file:
  echo >> /etc/audit/audit.rules
  echo "# sudoers" >> /etc/audit/audit.rules
  echo "-w /etc/sudoers -p wa -k scope" >> /etc/audit/audit.rules
  echo "-w /var/log/sudo.log -p wa -k actions" >> /etc/audit/audit.rules
  touch /var/log/sudo.log
}

RH_kernel_modules()
{
  # Add the following lines to the /etc/audit/audit.rules file:
  echo  >> /etc/audit/audit.rules
  echo "# kernel load/unload" >> /etc/audit/audit.rules
  echo "-w /sbin/insmod -p x -k modules" >> /etc/audit/audit.rules
  echo "-w /sbin/rmmod -p x -k modules" >> /etc/audit/audit.rules
  echo "-w /sbin/modprobe -p x -k modules" >> /etc/audit/audit.rules
  echo "-a always,exit -F arch=b32 -S init_module -S delete_module -k modules" >> /etc/audit/audit.rules
  echo "-a always,exit -F arch=b64 -S init_module -S delete_module -k modules" >> /etc/audit/audit.rules
}

RH_syslog_conf()
{
  echo "syslog.*   /var/log/syslog" >> /etc/syslog.conf
  touch /var/log/syslog
  sed 's,{,/var/log/syslog {,' ${HARD_DIR}/logrotate.d_syslog.before_hardening > /etc/logrotate.d/syslog
}



RH_local_accounts()
{
#  mkdir -m 755 /opt/users

  # NOC
  echo "noc:x:908:100:Network Operation Center User:/opt/users/noc:/usr/bin/ksh" >> /etc/passwd
  echo "noc:l5xwEFQiTFGqw:13760::::::" >> /etc/shadow
  /usr/sbin/pwconv
  /usr/bin/chage -M 99999 noc
  mkdir -m 750 /opt/users/noc
  chown 908:100 /opt/users/noc
#  echo "Allowusers noc" >> /etc/ssh/sshd_config


  # restrict local account login
  echo "Allowusers unixsa noc ssn sgs-scan bacmon netmgr ssnsupport uc4user uiqrsync oracle" >> /etc/ssh/sshd_config
}

# adjust Netbackup bp.conf for DMZ
netbackup()
{
cat > ${HARD_DIR}/bp.conf.after_hardening <<EOF
SERVER = nbumtami-msw-01.ceg.corp.net
SERVER = nbumtami-msw-01.ceg.corp.net
CLIENT_NAME = HOSTNAME.uiq.bgesg.net
CONNECT_OPTIONS = localhost 1 0 2
EOF

  sed "s/HOSTNAME/`hostname`/" ${HARD_DIR}/bp.conf.after_hardening > /opt/openv/netbackup/bp.conf
}

sudoers()
{
sed -i "s/localhost/`hostname`/" /etc/sudoers
}

setup_GMT()
{
sed 's,America/New_York,GMT,g' /etc/sysconfig/clock > /etc/sysconfig/clock_new
cat /etc/sysconfig/clock_new > /etc/sysconfig/clock
rm -f /etc/sysconfig/clock_new
rm -f /etc/localtime
ln -sf /usr/share/zoneinfo/GMT  /etc/localtime
}

setup_eth0()
{
LOG=/var/tmp/setup_eth0.log
rm -rf /var/tmp/setup_eth0.log
/opt/sfw/bin/inq | grep VMware >> $LOG 2>&1
if [ $? = 0 ]
then
        cat /etc/sysconfig/network-scripts/ifcfg-bond0 > /etc/sysconfig/network-scripts/ifcfg-eth0
        sed -i 's/DEVICE=bond0/DEVICE=eth0/' /etc/sysconfig/network-scripts/ifcfg-eth0
        sed -i 's/BONDING_OPTS="mode=1 primary=eth0 miimon=500"/ /' /etc/sysconfig/network-scripts/ifcfg-eth0
        rm -f /etc/sysconfig/network-scripts/ifcfg-bond0
        rm -f /etc/sysconfig/network-scripts/ifcfg-eth1
        service network restart
fi
}

###########################################################################

HARD_DIR=/var/tmp/hardening
mkdir -p 600 ${HARD_DIR} > /dev/null 2>&1


OS=`uname -s`

###########################################################################

case "${OS}" in
Linux)
  chkconfig --list > ${HARD_DIR}/chkconfig.before_hardening
  service --status-all > ${HARD_DIR}/service.before_hardening
  cp -p /etc/inittab ${HARD_DIR}/inittab.before_hardening
  cp -p /etc/passwd ${HARD_DIR}/passwd.before_hardening
  cp -p /etc/group ${HARD_DIR}/group.before_hardening
  cp -p /etc/shadow ${HARD_DIR}/shadow.before_hardening
  cp -p /etc/services ${HARD_DIR}/services.before_hardening
  cp -p /boot/grub/grub.conf ${HARD_DIR}/grub.conf.before_hardening
  cp -p /etc/audit/audit.rules ${HARD_DIR}/audit.rules.before_hardening
  cp -p /etc/logrotate.conf ${HARD_DIR}/logrotate.conf.before_hardening
  cp -p /etc/ssh/sshd_config ${HARD_DIR}/sshd_config.before_hardening
  cp -p /etc/motd ${HARD_DIR}/motd.before_hardening
  cp -p /etc/fstab ${HARD_DIR}/fstab.before_hardening
  cp -p /etc/syslog.conf ${HARD_DIR}/logrotate.d_syslog.before_hardening
  cp -p /opt/openv/netbackup/bp.conf ${HARD_DIR}/bp.conf.before_hardening
  cp -p /etc/sysconfig/network-scripts/ifcfg-bond0 ${HARD_DIR}/ifcfg-bond0.before_hardening
  cp -p /etc/sysconfig/network-scripts/ifcfg-eth0 ${HARD_DIR}/ifcfg-eth0.before_hardening

  disable_services
  RH_disable_chkconfig
  RH_remove_samba
  RH_auditing
  RH_log_rotate
  RH_lock_system_accounts
  RH_sshd_config
  RH_sshd_banner
  RH_at_cron_deny
  RH_daemon_umask
  RH_fstab
  RH_kernel_modules
  RH_privileged_commands
  RH_sudoers_audit
  RH_syslog_conf
  RH_local_accounts
  netbackup
  RH_files_remove
  sudoers
  setup_GMT
  setup_eth0
  ;;
esac

