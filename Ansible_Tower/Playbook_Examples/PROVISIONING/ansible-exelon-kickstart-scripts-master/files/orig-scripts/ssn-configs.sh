#!/bin/bash
if `rpm -qa|grep VRTS`
then
/bin/sed -i 's/PATH\=\$PATH/PATH\=\$PATH:\/usr\/bin:\/opt\/quest\/bin:\/opt\/VRTS\/bin:\/etc\/vx\/bin/' /root/.bash_profile
/bin/echo "MANPATH=\$MANPATH:/opt/VRTS/man" >> /root/.bash_profile
/bin/echo "export MANPATH" >> /root/.bash_profile
else
/bin/sed -i 's/PATH\=\$PATH/PATH\=\$PATH:\/usr\/bin:\/opt\/quest\/bin/' /root/.bash_profile
fi
#####Fix utmp##
/bin/chmod 664 /var/run/utmp
/bin/chmod 664 /var/log/messages*
#####Fix /etc/man.config
/bin/sed -i 's/\/usr\/bin\/less -is/\/usr\/bin\/less \-Xis/' /etc/man.config

###Create Link
ln .s /usr/lib/libcrypto.so.1.0.1e /usr/lib/libcrypto.so.4

############# Custom script work
# change sendmail relay to point to exrelay

/bin/sed -i 's/DSsmtpux.ceg.corp.net/DSexrelay.ceg.corp.net/' /etc/mail/sendmail.cf
/bin/sed -i 's/DSsmtpux.ceg.corp.net/DSexrelay.ceg.corp.net/' /etc/mail/submit.cf
/bin/sed -i 's/D{MTAHost}smtpux.ceg.corp.net/D{MTAHost}exrelay.ceg.corp.net/' /etc/mail/submit.cf
/bin/sed -i 's/DAEMON=yes/DAEMON=no/' /etc/sysconfig/sendmail

/usr/sbin/groupadd -g 60002 sgs-scan
/usr/sbin/useradd -u 60002 -g 60002 -c "sgs-scan Security Auditor" -d /opt/users/sgs-scan -s /bin/bash sgs-scan
/usr/sbin/usermod -p '$1$nY0vHsFq$rX4jgdwCFr6x00dRrlXhp0' sgs-scan
/bin/mkdir -m 755 /opt/users/sgs-scan ; chown -R sgs-scan:sgs-scan /opt/users/sgs-scan

/bin/sed -i 's/\*.info;mail.none;authpriv.none;cron.none/\*.err;\*.info;mail.none;authpriv.none;cron.none;auth.none/' /etc/syslog.conf
/bin/sed -i '/local7/a\
auth.info                               @syslog-cndlr-01.ceg.corp.net\
auth.info                               @syslog-drf-01.ceg.corp.net' /etc/syslog.conf

/sbin/service syslog restart

/usr/sbin/groupadd -g 60000 ssn
/usr/sbin/useradd -u 60000 -g 60000 -c "SSN Control Account" -d /opt/users/ssn -s /bin/bash ssn
/usr/sbin/usermod -p '$1$rLgQWaq/$AKTQnDsYBodpXzvdtli0E/' ssn
/usr/sbin/gpasswd --members ssn,uiqrsync ssn
/bin/mkdir -m 755 /opt/users/ssn ; chown -R ssn:ssn /opt/users/ssn
/bin/mkdir -m 0755 /apps

/usr/sbin/groupadd -g 60003 uiqrsync
/usr/sbin/useradd -u 60003 -g 60003 -c "rsync user id" -d /opt/users/uiqrsync -s /bin/bash uiqrsync
/usr/sbin/usermod -p '$1$a7Ry4J9J$Zgl5FESwlELOvAH0vtiTY1' uiqrsync
/bin/mkdir -m 755 /opt/users/uiqrsync ; chown -R uiqrsync:uiqrsync /opt/users/uiqrsync

/usr/sbin/groupadd -g 500 ssnsupport
/usr/sbin/useradd -u 500 -g 500  -d /opt/users/ssnsupport -s /bin/bash ssnsupport
/usr/sbin/usermod -p '$1$W3w2qaI1$framRyLru9FB6.HndqEMT.:' ssnsupport
/bin/mkdir -m 755 /opt/users/ssnsupport ; chown -R ssnsupport:ssnsupport /opt/users/ssnsupport

/usr/sbin/groupadd -g 60005 netmgr
/usr/sbin/useradd -u 60005 -g 60005 -c "netmgr account" -d /opt/users/netmgr -s /bin/bash netmgr
/usr/sbin/usermod -p 'pHAIW2/eUNTLezhDiI44.' netmgr
/usr/sbin/gpasswd --members e16970,e33877,e13352,uiqrsync,e39239,e46467 netmgr
/bin/mkdir -m 755 /opt/users/netmgr ; chown -R netmgr:netmgr /opt/users/netmgr

/usr/sbin/groupadd -g 501 bacmon
/usr/sbin/useradd -u 501 -g 501 -d /opt/users/bacmon -s /bin/bash bacmon
/usr/sbin/usermod -p '$1$.y6dCyJO$xpuQPIK8wks63uo12M3GV0' bacmon
/bin/mkdir -m 755 /opt/users/bacmon ; chown -R bacmon:bacmon /opt/users/bacmon

/usr/sbin/groupadd -g 60004 uc4user
/usr/sbin/useradd -u 60004 -g 60004 -d /opt/users/uc4user -s /bin/bash uc4user
/usr/sbin/usermod -p '$1$B8FyWnh6$mu9O5J3OFSmsCNsLmLCNq/' uc4user
/bin/mkdir -m 755 /opt/users/uc4user ; chown -R uc4user:uc4user /opt/users/uc4user

/usr/sbin/groupadd -g 602 dba
/bin/mkdir -m 755 /opt/users
/usr/sbin/useradd -u 1003 -g 602 -c "Oracle software user" -d /opt/users/oracle -s /bin/ksh oracle
/usr/sbin/usermod -p '\$1\$5zRCmv4e\$KmPVEQpqnnuavZEUuoqvB1' oracle
/bin/mkdir -m 755 /opt/users/oracle ; chown -R oracle:dba /opt/users/oracle
/bin/ln -s /opt/users/oracle /oracle


/usr/sbin/groupadd -g 666 unixsa
/usr/sbin/useradd -u 999 -g 666 -d /opt/users/unixsa -s /bin/bash unixsa
/usr/sbin/usermod -p '$1$VNz/zowH$PH2VDCihLFNNAxwE1OaBn.' unixsa
/bin/mkdir -m 700 /opt/users/unixsa ; chown -R unixsa:users /opt/users/unixsa

/usr/sbin/groupadd -g 602 dba
/bin/mkdir -m 755 /opt/users
/usr/sbin/useradd -u 1003 -g 602 -c "Oracle software user" -d /opt/users/oracle -s /bin/ksh oracle
/usr/sbin/usermod -p '\$1\$5zRCmv4e\$KmPVEQpqnnuavZEUuoqvB1' oracle
/bin/mkdir -m 755 /opt/users/oracle ; chown -R oracle:dba /opt/users/oracle

#e33877
echo "e33877:x:33877:100:James Garrett:/opt/users/e33877:/bin/bash" >> /etc/passwd
echo "e33877:$1$eFeMo.i4$uYR6tZTvVnryEtJGGIUoT.:15749::99999::::" >> /etc/shadow
/usr/sbin/pwconv
/usr/bin/chage -M 99999 e33877
mkdir -m 750 /opt/users/e33877
chown 33877:100 /opt/users/e33877

#e16970
echo "e16970:x:16970:100:Nicholas Schwienteck:/opt/users/e16970:/bin/bash" >> /etc/passwd
echo "e16970:$1$FoEc0BDt$JVn4aILTtbttflon5Up5A1:15731::99999::::" >> /etc/shadow
/usr/sbin/pwconv
/usr/bin/chage -M 99999 e16970
mkdir -m 750 /opt/users/e16970
chown 16970:100 /opt/users/e16970

#e13352
echo "e13352:x:13352:100:Kevin Collins:/opt/users/e13352:/bin/bash" >> /etc/passwd
echo "e13352:$1$z5Bb6MOY$ZVCHg9Ppd7ZoCd7BhOxIM.:15731::99999::::" >> /etc/shadow
/usr/sbin/pwconv
/usr/bin/chage -M 99999 e13352
mkdir -m 750 /opt/users/e13352
chown 13352:100 /opt/users/e13352

#e39239
echo "e39239:x:39239:100:Michael Morlock:/opt/users/e39239:/bin/bash" >> /etc/passwd
echo "e39239:$1$HX0VQW9l$W0SxRy.SKAJEr3WCnVNjY.:15747:0:99999:7:::" >> /etc/shadow
/usr/sbin/pwconv
/usr/bin/chage -M 99999 e39239
mkdir -m 750 /opt/users/e39239
chown 39239:100 /opt/users/e39239

#e46467
echo "e46467:x:46467:100:Ashraf Girguis:/opt/users/e46467:/bin/bash" >> /etc/passwd
echo "e46467:$1$YfgNOtow$r1ptYhu2.S5Y3Ry.pZVgK.:15783:0:99999:7:::" >> /etc/shadow
/usr/sbin/pwconv
/usr/bin/chage -M 99999 e46467
mkdir -m 750 /opt/users/e46467
chown 46467:100 /opt/users/e46467

#e048895
echo "e048895:x:48895:100:Harris, Christopher J_(BGE):/opt/users/e048895:/bin/bash" >> /etc/passwd
echo "e048895:$1$tJHmpibt$EdAhmR/Eyu.soCDSZzfPA1:16323:0:99999:7:::" >> /etc/shadow
/usr/sbin/pwconv
/usr/bin/chage -M 99999 e048895
mkdir -m 750 /opt/users/e048895
chown 48895:100 /opt/users/e048895

/usr/sbin/usermod -a -G netmgr e33877
/usr/sbin/usermod -a -G netmgr e39239
/usr/sbin/usermod -a -G netmgr e46467
/usr/sbin/usermod -a -G netmgr e048895


echo "Allowusers e33877 e16970 e13352 e39239 e46467 e048895" >> /etc/ssh/sshd_config
service sshd restart


yum localinstall -y http://satadmin.exelonds.com/pub/software/syslog-ng-premium-edition-client-5.0.10b-1.rhel6.i386.rpm

