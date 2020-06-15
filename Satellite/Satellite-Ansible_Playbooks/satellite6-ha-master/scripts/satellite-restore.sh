#!/bin/bash
# Benjamin Chardi bchardim@redhat.com, v1.0 - 03/2014
# Satellite 6.1.3
# Disclaimer | This script is NOT SUPPORTED by Red Hat Global Support Service.
# Global Variables
export LOGFILE=/var/log/satellite6-restore.log
# First and unique argument must be back dir to restore
RESDIR=$1
# Function to launch commands
execom () {
command=$1
if [ `/bin/echo $command | grep -P .+ | wc -l` -ne 0 ]
then
datecom=`/bin/date +%Y%m%d%H%M%S`
/bin/echo "$datecom Executing command : '$command >> $LOGFILE 2>&1'" >> $LOGFILE 2>&1
/bin/sh -c "$command >> $LOGFILE 2>&1"
RET=$?
/bin/echo "$datecom Return from command '$command >> $LOGFILE 2>&1' is '$RET'" >> $LOGFILE 2>&1
if [ ! "$RET" == "0" ]
then
/bin/echo "$datecom Return from command '$command >> $LOGFILE 2>&1' '$RET' != '0' . Aborting script : 'exit 1'" >> $LOGFILE 2>&1
/bin/echo "$datecom Return from command '$command >> $LOGFILE 2>&1' '$RET' != '0' . Aborting script : 'exit 1'"
/usr/bin/katello-service stop >> $LOGFILE 2>&1
exit 1
fi
fi
}
# Script begin
/bin/echo "Starting execution of $0 $1 at $VER" >> $LOGFILE 2>&1
# Stop sat6
execom "/usr/bin/katello-service stop"
sleep 6
execom "/usr/bin/systemctl stop postgresql.service "
sleep 6
# Restore system files
execom "/bin/tar --selinux -xzvf ${RESDIR}/config_files.tar.gz -C /"
execom "/bin/tar --selinux -xzvf ${RESDIR}/pgsql_data.tar.gz -C /"
execom "/bin/tar --selinux -xzvf ${RESDIR}/mongo_data.tar.gz -C /"
execom "/usr/bin/rsync --partial --progress --delete -alv ${RESDIR}/pulp/ /var/lib/pulp/"
execom "/usr/bin/rsync --partial --progress --delete -alv ${RESDIR}/pulp/ /var/lib/pulp/"
# Drop the existing Red Hat Satellite PostgreSQL databases if any exist
execom "/usr/bin/systemctl start postgresql.service "
sleep 30
execom "/sbin/runuser - postgres -c \"dropdb candlepin\""
execom "/sbin/runuser - postgres -c \"dropdb foreman\""
# Restore Red Hat Satellite PostgreSQL databases with the following commands
execom "/sbin/runuser - postgres -c \"pg_restore -C -d postgres ${RESDIR}/candlepin.dump\""
execom "/sbin/runuser - postgres -c \"pg_restore -C -d postgres ${RESDIR}/foreman.dump\""
# Ensure MongoDB is running, delete the old data and restore new one
execom "/usr/bin/systemctl start  mongod.service"
sleep 30
execom "/bin/echo 'db.dropDatabase();' | mongo pulp_database"
execom "/usr/bin/mongorestore --host localhost ${RESDIR}/mongo_dump/pulp_database/"
# Start Sat6 and verify it
execom "/usr/bin/katello-service start"
execom "/usr/bin/systemctl start  postgresql.service"
###execom "/sbin/reboot"
# End script
/bin/echo "Execution of $0 $1 at $VER finished with return = 0" >> $LOGFILE 2>&1
