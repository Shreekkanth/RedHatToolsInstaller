
````
               _   _           _
              | | | |         | |
  _ __ ___  __| | | |__   __ _| |_
 | '__/ _ \/ _` | | '_ \ / _` | __|
 | | |  __/ (_| | | | | | (_| | |_
 |_|  \___|\__,_| |_| |_|\__,_|\__|

````

A new vault file
=========

Create a vault file:


````
> cd rh-dm-7-ansible/roles/rhdm/vars
> ansible-vault create var-secret.yml

````

Download Software
=========

Execute:

````
> cd rh-dm-7-ansible
> ansible-playbook download.yml -i inventory

````

Install from scratch
=========

Execute:

````
> cd rh-dm-7-ansible
> ansible-playbook main.yml -i inventory --ask-vault-pass

> ansible-playbook main_local.yml -i inventory --ask-vault-pass --ask-become-pass

````

Uninstall JBoss EAP & DM
=========

Execute:

````
> cd rh-dm-7-ansible
> ansible-playbook uninstall.yml -i inventory --ask-vault-pass --tags "rhdm_uninstall"
> ansible-playbook uninstall_local.yml -i inventory --ask-vault-pass --ask-become-pass --tags "rhdm_uninstall"

````


Create User
=========

Execute:

````
> cd rh-dm-7-ansible
> ansible-playbook rhdm_user.yml -i inventory --tags "jboss_sso_user,sudoers" --ask-pass --ask-vault-pass

````


JBoss EAP Run as a Service and systemctl
=


````
$JBOSS_HOME/bin/init.d/jboss-eap.conf
$JBOSS_HOME/bin/init.d/jboss-eap-rhel.sh
````

Refs:
[JBoss EAP Run as a Service](https://access.redhat.com/documentation/en-us/red_hat_jboss_enterprise_application_platform/7.1/html-single/installation_guide/#configuring_jboss_eap_to_run_as_a_service "Run as a Service")
[What is --admin-only mode in Jboss](https://access.redhat.com/solutions/341813 "admin-only mode")


---