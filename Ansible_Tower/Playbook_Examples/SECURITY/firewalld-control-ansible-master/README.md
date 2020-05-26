# BBVA Workplace firewalld control

## reset_firewalld

reset_firewalld is a playbook which runs the reset_firewalld role.

This role uploads the RHEL7.5 default firewall rules, so there are only two services enabled, ssh and dhcpv6-client

## open_ports

This playbook/role requires a variable called ports, which contains a list of ports to be opened.

It calls the reset_firewalld role, so **the specified ports are the only ones which are going to be at the system, with the ssh and dhcpv6-client services too**

ports var example:

```yaml
- ports:
  - 80/tcp
  - 8080/tcp
```
