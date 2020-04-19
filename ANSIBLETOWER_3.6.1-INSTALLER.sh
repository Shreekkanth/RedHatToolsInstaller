#!/bin/bash
echo -ne "\e[8;45;120t"
reset
if [ "$(whoami)" != "root" ]
then
echo "This script must be run as root - if you do not have the credentials please contact your administrator"
exit
else
echo 'ANSIBLE-TOWER 3.6.1 INSTALLER FOR RHEL 7.x AND RHEL 8.x
FOR SETTING UP A SIMPLE SINGLE NODE CONFIGURATION FOR P.O.C.'
read -p "To Continue Press [Enter] or use Ctrl+c to exit the installer"
fi
#-------------------------
function ANSIBLETOWERTXT {
#-------------------------
reset
HNAME=$(hostname)
echo " "
echo " "
echo " "
echo "
ANSIBLE-TOWER BASE HARDWARE REQUIREMENTS

1. Ansible-Tower will require a RHEL subscription and an Ansible Tower License.
Please register and download your lincense at http://www.ansible.com/tower-trial

2. Hardware requirement depends, however whether 
   it is a KVM or physical-Tower will require atleast 1 node with:

        Min Storage 35GB
        Directorys  Recommended
        /boot  1024MB
        /swap  8192MB
        / Rest of drive


        Min RAM 4096
        Min CPU 2 (4 Reccomended)

3. Network
    Connection to the internet so the installer can download the required packages"
echo " "
echo " "
echo " "
read -p "Press [Enter] to continue"
reset
echo " "
echo "

REQUIREMENTS CONTINUED

4. For this POC you must have a RHN User ID and password with entitlements
   to channels below. (item 6)

5. Install ansible tgz will be downloaded and placed into the FILES directory created by the sript on the host machine:

6. This install was tested with:
        * RHEL_7.x in a KVM environment.
        * Ansible Tower 3.6.1 https://releases.ansible.com/ansible-tower/setup-bundle/ansible-tower-setup-bundle-3.6.1-1.el7.tar.gz
        * Red Hat subscriber channels:
            rhel-7-server-ansible-2.8-rpms
            rhel-7-server-extras-rpms
            rhel-7-server-optional-rpms
            rhel-7-server-rpms
            https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

        * RHEL_8.x in a KVM environment.
        * Ansible Tower 3.6.1 https://releases.ansible.com/ansible-tower/setup-bundle/ansible-tower-setup-bundle-3.6.1-1.el8.tar.gz
        * Red Hat subscriber channels:
            ansible-2.9-for-rhel-8-x86_64-rpms
            rhel-8-for-x86_64-appstream-rpms
            rhel-8-for-x86_64-baseos-rpms
            rhel-8-for-x86_64-supplementary-rpms
            rhel-8-for-x86_64-optional-rpms
            https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm

URL Resources 
        http://www.ansible.com
        https://www.ansible.com/tower-trial
        http://docs.ansible.com/ansible-tower/latest/html/quickinstall/index.html"
echo " "
echo " "
read -p "If you have met all of the minimum requirements from above please Press [Enter] to continue"
echo " "
reset
}

#----------------------
function CHECKCONNECT {
#----------------------
echo "********************************************"
echo "Verifying the server can get to the internet"
echo "********************************************"
wget -q --tries=10 --timeout=20 --spider http://google.com
if [[ $? -eq 0 ]]; then
    echo "Online: Continuing to Install"
            sleep 2
else
    echo "Offline"
    echo "This script requires access to 
              the network to run please fix your settings and try again"
    sleep 2
    exit 1
fi
}

#------------------
function REGISTER {
#------------------
    echo "****************************"
    echo "Registering system if needed"
    echo "****************************"
        subscription-manager status | awk -F ':' '{print $2}'|grep Current > /dev/null
        status=$?
        if test $status -eq 1
        then
            echo "System is not registered, Please provide Red Hat CDN username and password when prompted"
            subscription-manager register --auto-attach
    
        else
            echo "System is registered with Red Hat or Red Hat Satellite, Continuing!"
    sleep 2 
    fi
echo " "
echo " "
}

#------------------------
function PREPFORINSTALL {
#------------------------
echo "***************************************************************************"
echo "SET SELINUX TO PERMISSIVE FOR THE INSTALL AND CONFIG OF Ansible Tower 3.6.1"
echo "***************************************************************************"
    sed -i 's/SELINUX=enforcing/SELINUX=permissive/g' /etc/selinux/config
    setenforce 0
    service firewalld stop
echo " "
echo " "
echo "*******************"
echo "FIRST DISABLE REPOS"
echo "*******************"
    subscription-manager repos --disable "*"
    yum-config-manager --disable "*"
echo " "
echo " "
}

#---------------------
function SYSTEMREPOS {
#---------------------
grep -q -i "release 7." /etc/redhat-release
status=$?
if test $status -eq 1
then
    echo "*******************"
    echo "ENABLE REPOS RHEL7 "
    echo "*******************"
    yum -q list installed epel &>/dev/null && echo "epel is installed" || yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm --skip-broken
    subscription-manager repos --enable rhel-7-server-rh-common-rpms --enable rhel-7-server-extras-rpms --enable rhel-7-server-optional-rpms --enable rhel-7-server-supplementary-rpms --enable rhel-server-rhscl-7-rpms --enable rhel-7-server-rpms --enable rhel-7-server-ansible-2.9-rpms
    yum clean all
    rm -rf /var/cache/yum
    yum-config-manager --setopt=\*.skip_if_unavailable=1 --save \*
echo " "
echo " "
sleep 2
    echo "********************************"
    echo "CHECKING AND INSTALLING PACKAGES"
    echo "********************************"
    yum -q list installed wget &>/dev/null && echo "wget is installed" || yum install -y wget --skip-broken --noplugins
    yum -q list installed python3-pip-wheel &>/dev/null && echo "wgpython3-pip-wheel is installed" || yum install -y python3-pip-wheel --skip-broken --noplugins
    yum -q list installed python3-pip &>/dev/null && echo "python3-pip is installed" || yum install -y python3-pip --skip-broken --noplugins
    yum -q list installed platform-python-pip &>/dev/null && echo "platform-python-pip is installed" || yum install -y platform-python-pip --skip-broken --noplugins
    yum -q list installed yum-utils &>/dev/null && echo "yum-utils is installed" || yum install -y yum-util* --skip-broken --noplugins
    yum -q list installed dialog &>/dev/null && echo "dialog is installed" || yum localinstall -y dialog --skip-broken --noplugins
    yum -q list installed bash-completion-extras &>/dev/null && echo "bash-completion-extras" || yum install -y bash-completion-extras --skip-broken --noplugins
    yum -q list installed dconf &>/dev/null && echo "dconf" || yum install -y dconf* --skip-broken --noplugins
    yum-config-manager --disable epel
echo " "
echo " "
elif test $status -eq 0
then
    echo '*******************'
    echo 'ENABLE REPOS RHEL 8' 
    echo '*******************'
    yum -q list installed epel &>/dev/null && echo "epel is installed" || yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm --skip-broken
    subscription-manager repos --enable ansible-2.8-for-rhel-8-x86_64-rpms --enable rhel-8-for-x86_64-appstream-rpms --enable rhel-8-for-x86_64-baseos-rpms --enable rhel-8-for-x86_64-supplementary-rpms --enable rhel-8-for-x86_64-optional-rpms
    dnf clean all
    rm -rf /var/cache/yum
    rm -rf /var/cache/dnf
    yum-config-manager --setopt=\*.skip_if_unavailable=1 --save \*
echo " "
echo " "
sleep 2
    echo "********************************"
    echo "CHECKING AND INSTALLING PACKAGES"
    echo "********************************"
    yum -q list installed wget &>/dev/null && echo "wget is installed" || yum install -y wget --skip-broken --noplugins
    yum -q list installed python3-pip-wheel &>/dev/null && echo "wgpython3-pip-wheel is installed" || yum install -y python3-pip-wheel --skip-broken --noplugins
    yum -q list installed python3-pip &>/dev/null && echo "python3-pip is installed" || yum install -y python3-pip --skip-broken --noplugins
    yum -q list installed platform-python-pip &>/dev/null && echo "platform-python-pip is installed" || yum install -y platform-python-pip --skip-broken --noplugins
    yum -q list installed yum-utils &>/dev/null && echo "yum-utils is installed" || yum install -y yum-util* --skip-broken --noplugins
    yum -q list installed dialog &>/dev/null && echo "dialog is installed" || yum localinstall -y dialog --skip-broken --noplugins
    yum -q list installed bash-completion-extras &>/dev/null && echo "bash-completion-extras" || yum install -y bash-completion-extras --skip-broken --noplugins
    yum -q list installed dconf &>/dev/null && echo "dconf" || yum install -y dconf* --skip-broken --noplugins
    yum -q list installed dnf-utils &>/dev/null && echo "dnf-utils is installed" || yum install -y dnf-utils --skip-broken --noplugins
    yum -q list installed dnf &>/dev/null && echo "dnf is installed" || yum install -y dnf --skip-broken --noplugins
    yum-config-manager --disable epel
echo " "
echo " "
sleep 2
fi
}

#---------------------------
function LINUXUPGRADE {
#---------------------------
grep -q -i "release 7." /etc/redhat-release
status=$?
if test $status -eq 1
then
    echo "*******************"
    echo "Upgrade RHEL7 "
    echo "*******************"
        yum upgrade -y
echo " "
echo " "
elif test $status -eq 0
then
    echo "*******************"
    echo "Upgrade RHEL8 "
    echo "*******************"
        dnf upgrade --best --allowerasing -y
echo " "
echo " "
fi
}

#---------------------------
function CloudRequirements {
#---------------------------
    echo '*********************************************'
    echo 'Installing Cloud Requirements (Ignore Errors)'
    echo '*********************************************'
        source /var/lib/awx/venv/ansible/bin/activate
        umask "0022"
        yum install python3-pip 
        pip install pip --upgrade
        pip install six
        pip install six --upgrade
        pip freeze | grep six
echo " "
echo " "
        pip install awscli
        pip install awscli --upgrade 
        pip freeze | grep awscli
echo " "
echo " "
        for i in $(pip freeze | grep azure | awk -F '=' '{print $1}') ; do pip install "$i" --upgrade  ; done
        pip install azure
        pip install azure  --upgrade
        pip install azure-common
        pip install azure-common --upgrade
        pip install azure-mgmt-authorization
        pip install azure-mgmt-authorization --upgrade
        pip install azure-mgmt
        pip install azure-mgmt --upgrade 
        pip freeze | grep azure
echo " "
echo " "
        pip install boto
        pip install boto --upgrade 
        pip install boto3
        pip install boto3 --upgrade 
        pip install botocore
        pip install botocore --upgrade
        pip freeze | grep boto
echo " "
echo " "
        pip install pywinrm
        pip install pywinrm --upgrade
        pip freeze | grep pywinrm
echo " "
echo " "
        rpm -e --nodeps requests
        pip install requests
        pip install requests --upgrade
        pip freeze | grep requests
echo " "
echo " "
        pip install requests-credssp
        pip install requests-credssp --upgrade
        pip freeze | grep requests-credssp
echo " "
echo " "
        pip install PyVmomi
        pip install PyVmomi --upgrade
        pip freeze | grep PyVmomi
    deactivate
echo " "
echo " "
}

#----------------------
function INSTALLTOWER {
#----------------------
grep -q -i "release 7." /etc/redhat-release
status=$?
if test $status -eq 1
then
    echo '****************************************************************'
    echo 'Getting, Expanding, and installing Ansible Tower 3.6.1 for RHEL7'
    echo '****************************************************************'
        wget https://releases.ansible.com/ansible-tower/setup-bundle/ansible-tower-setup-bundle-3.6.1-1.el7.tar.gz
        tar -zxvf ansible-tower-setup-bundle-3.6.1-1.el7.tar.gz
        yum localinstall ansible-tower-setup-bundle-3.6.1-1.el7/bundle/repos/*.rpm
        cd ansible-tower-setup-bundle-3.6.1-1.el7
    echo 'What would you like your default Ansible Tower user "admin" password to be?'
        read ADMINPASSWORD
        sed -i 's/admin_password="''"/admin_password="'$ADMINPASSWORD'"/g' inventory
        sed -i 's/redis_password="''"/redis_password="'$ADMINPASSWORD'"/g' inventory
        sed -i 's/pg_password="''"/pg_password="'$ADMINPASSWORD'"/g' inventory
        sed -i 's/rabbitmq_password="''"/rabbitmq_password="'$ADMINPASSWORD'"/g' inventory
        sh setup.sh
        sleep 10
echo " "
echo " "
elif test $status -eq 0
then
    echo '****************************************************************'
    echo 'Getting, Expanding, and installing Ansible Tower 3.6.1 for RHEL8'
    echo '****************************************************************'
        wget https://releases.ansible.com/ansible-tower/setup-bundle/ansible-tower-setup-bundle-3.6.1-1.el8.tar.gz
        tar -zxvf ansible-tower-setup-bundle-3.6.1-1.el8.tar.gz
        yum localinstall ansible-tower-setup-bundle-3.6.1-1.el8/bundle/repos/*.rpm
        cd ansible-tower-setup-bundle-3.6.1-1.el8
    echo 'What would you like your default Ansible Tower user "admin" password to be?'
        read ADMINPASSWORD
        sed -i 's/admin_password="''"/admin_password="'$ADMINPASSWORD'"/g' inventory
        sed -i 's/redis_password="''"/redis_password="'$ADMINPASSWORD'"/g' inventory
        sed -i 's/pg_password="''"/pg_password="'$ADMINPASSWORD'"/g' inventory
        sed -i 's/rabbitmq_password="''"/rabbitmq_password="'$ADMINPASSWORD'"/g' inventory
        sh setup.sh
        sleep 10
echo " "
echo " "
fi
}

CHECKCONNECT
ANSIBLETOWERTXT
REGISTER
PREPFORINSTALL
SYSTEMREPOS
LINUXUPGRADE
INSTALLTOWER
#CloudRequirements

