#!/bin/bash
# Benjamin Chardi bchardim@redhat.com, v1.0 - 03/2014
# Satellite 6.1.3
# Disclaimer | This script is NOT SUPPORTED by Red Hat Global Support Service.
# Global Variables
umask 0027
export RETENTION=15
export VER=`date +%Y-%m-%d-%H%M%S`
export BDIR=/var/tmp/rhs6backup
export LOGFILE=/var/log/satellite6-backup.log
export DIRECTORIES='/etc/sudoers /etc/sudoers.d /etc/foreman-proxy /etc/foreman /etc/hammer /etc/tomcat /etc/httpd /etc/katello-installer /etc/pki /etc/puppet /srv /var/lib/candlepin /var/lib/foreman-proxy /var/lib/foreman /var/lib/puppet /var/www/pulp /etc/default /etc/katello /etc/elasticsearch /etc/candlepin /etc/pulp /etc/pki/katello /etc/pki/pulp /etc/sysconfig/katello /etc/sysconfig/elasticsearch /root/ssl-build /var/www/html/pub /var/lib/elasticsearch /usr/share/foreman-proxy /usr/share/katello /usr/share/java/elasticsearch /var/lib/tftpboot /var/named /var/lib/dhcpd /etc/dhcp/'
# Function to launch commands
execom () {
command=$1
if [ `/bin/echo $command | grep -P .+ | wc -l` -ne 0 ]
then
datecom=`/bin/date +%Y%m%d%H%M%S`
/bin/echo "$datecom Executting command : '$command >> $LOGFILE 2>&1'" >> $LOGFILE 2>&1
/bin/sh -c "$command >> $LOGFILE 2>&1"
RET=$?
/bin/echo "$datecom Return from command '$command >> $LOGFILE 2>&1' is '$RET'" >> $LOGFILE 2>&1
if [ ! "$RET" == "0" ]
then
/bin/echo "$datecom Return from command '$command >> $LOGFILE 2>&1' '$RET' != '0' . Aborting script : 'exit 1'" >> $LOGFILE 2>&1
/bin/echo "$datecom Return from command '$command >> $LOGFILE 2>&1' '$RET' != '0' . Aborting script : 'exit 1'"
/usr/bin/katello-service start >> $LOGFILE 2>&1
exit 1
fi
fi
}
# Script begin
/bin/echo "Starting execution of $0 $1 at $VER" >> $LOGFILE 2>&1
# Generate skel dir with permissions
execom "/bin/mkdir -p ${BDIR}"
execom "/bin/chmod 755 ${BDIR}"
execom "/bin/mkdir -p ${BDIR}/${VER}"
execom "/bin/chgrp postgres ${BDIR}/${VER}"
execom "/bin/chmod 770 ${BDIR}/${VER}"
# Clean up old backups, they have been captured by NetBackup
for i in $(/usr/bin/find ${BDIR}/ -type d -mtime +${RETENTION})
do
execom "/bin/rm -rf $i"
done
# Backup the configuration and data files
execom "/bin/tar --selinux -czvf ${BDIR}/${VER}/config_files.tar.gz $DIRECTORIES"
execom "/bin/tar --selinux -tzvf ${BDIR}/${VER}/config_files.tar.gz"
# Online Repositories Backup
/bin/echo "Trying to make online backup /var/lib/pulp and /var/www/pub via rsync" >> $LOGFILE 2>&1
/usr/bin/rsync --partial --progress --delete -alv /var/lib/pulp ${BDIR}/${VER}/ >> $LOGFILE 2>&1
CHKREPO=$(/bin/find /var/lib/pulp -printf '%T@\n' | md5sum)
execom "/usr/bin/rsync --partial --progress --delete -alv /var/lib/pulp ${BDIR}/${VER}/"
CHKREPOB=$(/bin/find /var/lib/pulp -printf '%T@\n' | md5sum)
/bin/echo "MD5 before tar: $CHKREPO after tar: $CHKREPOB" >> $LOGFILE 2>&1
if [ ! "$CHKREPO" == "$CHKREPOB" ]
then
/bin/echo "ERROR doing online repositories backup. Aborting backup process" >> $LOGFILE 2>&1 exit 1
fi
# Optional: O[ine Database Backup
# rhs6 must be stopped
execom "/usr/bin/katello-service stop"
execom "/bin/tar --selinux -czvf ${BDIR}/${VER}/mongo_data.tar.gz /var/lib/mongodb"
execom "/bin/tar --selinux -tzvf ${BDIR}/${VER}/mongo_data.tar.gz"
execom "/bin/tar --selinux -czvf ${BDIR}/${VER}/pgsql_data.tar.gz /var/lib/pgsql/data"
execom "/bin/tar --selinux -tzvf ${BDIR}/${VER}/pgsql_data.tar.gz"
execom "/usr/bin/katello-service start"
# Postgres online database backup
# Extract schema names from "grep db_name /etc/katello/katello-configure.conf"
execom "/sbin/runuser - postgres -c \"pg_dump -Fc candlepin > ${BDIR}/${VER}/candlepin.dump\""
execom "/sbin/runuser - postgres -c \"pg_dump -Fc foreman > ${BDIR}/${VER}/foreman.dump\""
# Mongodb online database backup
execom "/usr/bin/mongodump --host localhost --out ${BDIR}/${VER}/mongo_dump"
# End script
/bin/echo "Execution of $0 $1 at $VER finished with return = 0" >> $LOGFILE 2>&1

