# **Standard Chartered Bank f5 GSLB configuration**

This directory contains the Ansible playbooks for the GSLB configuration


Playbooks:
* f5.yml
* f5_testing.yml

## **Introduction**
This repoository contains the playbooks that were created for SCB-F5-Ansible POC. The playbooks were created to test the suite of BIGIP Ansible Modules (https://docs.ansible.com/ansible/latest/modules/list_of_network_modules.html#f5), with the main purpose being to update *A Records* on F5 GSLB.

## **Playbooks**
f5.yml contains the tested and working plays with their individual link to the playbook module, here are the plays:
1.  Collect BIG-IP facts
2.  Create a GTM pool
3.  Create a nameserver
  
f5_testing.yml containes plays that are currently working and undergoing testing as well. Here are the plays:
1.  Collect BIG-IP facts
2.  Create a GTM pool
3.  Create a nameserver
4.  Create a Datacenter

