# Development Environment
The purpose of this environment is for developer use. The creation of the
infrastructure is entirely automated and access the infrastructure is provided
through ssh.

## Supported Domains
* Low side

## Inventory
The inventory file is created automatically by the Azure development environment
automation. Deploying new development infrastructure is done by running:
```shell
make spin
```
When utilising the Azure development environment you need to provide a `secrets.tf`
file. Copying or linking into the project root.

### Static Inventory
This environment can be used with static infrastructure and hand written
inventory file. If you want the ipa-environment to manage the hosts DNS provider
add `external_dns` variable to the _all_ group.
Using the Azure development environment this handled automatically by appending
the var to the inventory:
```shell
  [all:vars]
  external_dns=172.16.0.4
```
The ipa-environment expects DNS to be handed outside of IPA.
Therefore you must ensure your DNS server is serving the following records.

* An A record for each host participating in the environment
* The following SRV records for all IPA hosts.
  * `_kerberos._udp, 88, 100`
  * `_kerberos._tcp, 88, 100`
  * `_kerberos-master._udp, 88, 100`
  * `_kerberos-master._tcp, 88, 100`
  * `_kpasswd._udp, 88, 100`
  * `_kpasswd._tcp, 88, 100`
  * `_ldap,_tcp, 389, 100`
  * `_kerberos, EXAMPLE.COM`
  * A TXT record for the Domain

### Secrets Management
Ansible Vault is used to encrypt several strings used throughout the playbook.
Talk to a fellow developer to be informed of the encryption password.

## Execution

```shell
ansible-playbook -i development site.yml --vault-id @prompt
```
