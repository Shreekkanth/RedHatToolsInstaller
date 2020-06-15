this is a project for all my demonstration builder playbooks

works in progress

* custom ansible tower builder
** this will auto populate a tower instance with customer specific templates, projects and use cases

* vmware poc provision to lock down vmware user permissions to ensure we only see their VMs
** this will ensure that when I show users vmware that they are only seeing the VMs and folders I want them to see

* build self healing demo in AWS
1 provision 2 VMs 
2 order 3 elastic IP addresses
3 assign 2 IP addresses to the previously provisioned VMs
4 update google domains A records with the IP information
5 install webserver
6 deploy website
7 configure load balancer with the two provisoned VMs
8 verify app is up.

