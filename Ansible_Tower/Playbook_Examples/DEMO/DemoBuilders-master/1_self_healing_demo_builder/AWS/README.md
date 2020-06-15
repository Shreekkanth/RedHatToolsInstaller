Self Healing Website Demo

* Self Healing Demo in AWS
1 aws_provision_instances - provision 2 VMs 
2 aws_order_eip - order 3 elastic IP addresses
3 aws_assign_eip - assign IP addresses to a previously provisioned VMs
4 gdomain_update_a_record - update google domains A records with the IP information
5 windows_install_iis - install webserver
6 windows_deploy_corpsite - deploy website
7 aws_configure_elb - configure load balancer with the two provisoned VMs
8 aws_configure_cloudwatch - configure cloudwatch monitor
9 test_demo - simulate the demo and verify success
