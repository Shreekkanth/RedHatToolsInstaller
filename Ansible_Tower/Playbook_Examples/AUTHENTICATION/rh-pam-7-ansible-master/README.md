
````
               _   _           _
              | | | |         | |
  _ __ ___  __| | | |__   __ _| |_
 | '__/ _ \/ _` | | '_ \ / _` | __|
 | | |  __/ (_| | | | | | (_| | |_
 |_|  \___|\__,_| |_| |_|\__,_|\__|

````

Download Software
=========

Execute:

````
> cd rh-pam-7-ansible
> ansible-playbook download.yml -i inventory

````

Install from scratch RHPAM & MySQL
=========

Execute:

````
> cd rh-pam-7-ansible
> ansible-playbook main_local.yml -i inventory --ask-vault-pass --ask-become-pass
````

Install RHPAM (using MySQL)
=========

Execute:

````
> cd rh-pam-7-ansible
> vi main_local.yml, change the flags to false:
mysql_user_remove:        false
mysql_user_create:        false
mysql_service_active:     false
mysql_install:            false
is_oracle_ds:             false
--> change the flags to true:
is_mysql_ds:              true

> ansible-playbook main_local.yml  -i inventory --ask-vault-pass --ask-become-pass
````

Install RHPAM (using Oracle)
=========

Execute:

````
> cd rh-pam-7-ansible
> vi main_local.yml
--> change the flags to false:
mysql_user_remove:        false
mysql_user_create:        false
mysql_service_active:     false
mysql_install:            false
is_mysql_ds:              false
--> change the flags to true:
is_oracle_ds:             true

> ansible-playbook main_local.yml  -i inventory --ask-vault-pass --ask-become-pass
````

Uninstall RHPAM & MySQL
=========

Execute:

````
> cd rh-pam-7-ansible
> ansible-playbook uninstall_local.yml -i inventory --ask-vault-pass --ask-become-pass --tags "mysql_uninstall,rhpam_uninstall"

````

Uninstall RHPAM
=========
````
> cd rh-pam-7-ansible
> ansible-playbook uninstall_local.yml -i inventory --ask-vault-pass --ask-become-pass --tags "rhpam_uninstall"

````

Uninstall MySQL
=========
````
> > cd rh-pam-7-ansible
> ansible-playbook uninstall_local.yml -i inventory --ask-vault-pass --ask-become-pass --tags "mysql_uninstall"

````

A new vault file
=========

Create a vault file:


````
> cd rh-pam-7-ansible/roles/rhpam/vars
> ansible-vault create vars_secret.yml

````


Create 'rhpam' User
=========

Execute:

````
> cd rh-pam-7-ansible
> ansible-playbook rhpam_user.yml -i inventory --tags "rhpam_user,sudoers" --ask-pass --ask-vault-pass

````


Create 'mysql' User
=========


Execute:

````
> cd rh-pam-7-ansible
> ansible-playbook rhpam_user.yml -i inventory --tags "rhpam_user,sudoers" --ask-pass --ask-vault-pass

````


Install mysql
=========

Requeriments:

````
sudo yum repolist all
sudo yum install libaio
sudo yum install unzip
sudo yum install java-1.8.0-openjdk-devel.x86_64

sudo yum install java-1.8.0-openjdk.x86_64
sudo yum remove java-1.8.0-openjdk.x86_64


````


For testing
=========

````
> cd rh-pam-7-ansible
> ansible-playbook mysql_user.yml -i inventory --ask-vault-pass --tags="mysql_user_remove,mysql_user"
> ansible-playbook main.yml       -i inventory --ask-vault-pass --tags="mysql_install"
> ansible-playbook main.yml       -i inventory --ask-vault-pass


> ansible-playbook main.yml       -i inventory --ask-vault-pass --tags="jboss_eap,jboss_eap_create_users"

> ansible-playbook main.yml       -i inventory --ask-vault-pass --tags="jboss_eap,jboss_eap_patch"

> ansible-playbook main.yml       -i inventory --ask-vault-pass --tags="rhpam_install"

> ansible-playbook main.yml       -i inventory --ask-vault-pass --tags="mysql_rhpam_model"

> ansible-playbook main.yml       -i inventory --ask-vault-pass --tags="rhpam_extra_libs"

````


## MySQL

Access to MySQL Prompt:

````
/rhpam/mysql/mysql/bin/mysql --defaults-file=/rhpam/mysql/mysql-files/conf/dev.cnf  -u root --password=Redhat1
show databases;
use RHPAM;
show tables;
````

jdbc:mysql://node-0.rhpam7.quicklab.pnq2.cee.redhat.com:3306/RHPAM
