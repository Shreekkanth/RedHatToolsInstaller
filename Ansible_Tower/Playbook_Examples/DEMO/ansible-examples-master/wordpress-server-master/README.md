Role Name
=========

Ansible Playbook to install and configure WordPress on a RHEL 7 / CentOS 7 machine.

Requirements
------------
This can be deployed on a bare CentOS 7 / RHEL 7 server, provided it has a working yum repository.  This should not run on a server with anything else.  Don't run this playbook against a server that contains any valuable data.  By design, it should only interact with the components involved, but I cannot be responsible for your unique situation.  Please familiarize yourself with this playbook or only run it on a fresh server with nothing else crucial installed.

This playbook will specifically install / remove services for MySQL, HTTPD, as well as specific PHP versions and repositories.

Description
------------

This role will: 

- Install PHP, MariaDB, httpd from default repos
- Import generic SQL and deploy the new instance with the variables you set

Role Variable Defaults (make changes in the file vars/main.yml)
--------------

DBName for MariaDB:   WordPress
Username for MariaDB: wordpress
Password for MariaDB: wordpress

Dependencies
------------

There is no role dependency for this role.

Host File
----------

The host file for this role is hosts.target and the format is: 

[wordpress]
IP FOR WORDPRESS SERVER

How to run the playbook
------------------------

** Edit the variable file on vars/main.yml to set it to your environment. 

** Run the playbook

** Make sure to include the safety word in your command.  I added this to put one extra annoying step to make sure no one breaks something without first reading this or confirming what this playbook actually does.

* ansible-playbook -i hosts.target --extra-vars "safety_word=wordpress-install" wordpress-install.yml
* ansible-playbook -i hosts.target --extra-vars "safety_word=wordpress-remove" wordpress-remove.yml

License
-------

GPLv3

Author Information
------------------

Kevin Holmes <kev@gokev.com> more at: https://github.com/GoKEV/
