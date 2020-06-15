# STIG Info For Satellite 6

## Summary

Utilized OpenSCAP & SCAP Work Bench to generate the baseline remediation script of 243 checks for the built RHEL 7 DISA STIG profile. Since the STIG breaks Satellite 6.3 by default, I had to comment out all checks and turn them on one by one to identify every single check that broke some aspect of Satellite. Used the newly identified checks to create a custom STIG profile 232 checks from the builtin RHEL 7 DISA STIG profile.

*BEFORE running the remediation script ensure that you have either a RHEL DVD mounted or registered to a CDN / Satellite.
## Repo Contents
* bash-remediation-latest.sh  <-- Custom Remediation Script
* ssg-rhel7-ds.xml  <-- Base Profile
* tailoring-xccdf.xml  <-- Custom Profile

**Breaks Satellite**  (Removed all FIPS related items regardless of it did not directly impact or Satellite to avoid confusion)
* xccdf_org.ssgproject.content_rule_sshd_use_approved_ciphers
* xccdf_org.ssgproject.content_rule_sshd_use_approved_macs
* xccdf_org.ssgproject.content_rule_grub2_enable_fips_mode
* xccdf_org.ssgproject.content_rule_package_dracut-fips_installed
* xccdf_org.ssgproject.content_rule_aide_use_fips_hashes
* xccdf_org.ssgproject.content_rule_sebool_fips_mode

**Breaks IDM SSO / Kerberos Integration**
* xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny_root
* xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny

**Needed for TFTP Provided Provisioning Services**
* xccdf_org.ssgproject.content_rule_service_tftp_disabled
* xccdf_org.ssgproject.content_rule_package_tftp-server_removed
* xccdf_org.ssgproject.content_rule_tftpd_uses_secure_mode

## ENV:

### Virtual Box running below VM's on laptop

* RHEL 7.5 Disconnected Satellite 6.3
* RHEL 7.5 Disconnected External Capsule 6.3 Server
* RHEL 7.5 IDM Server on RHEL 7.5
* RHEL 7.5 Client
* RHEL 7.5 Repo Server

## Test Cases:

* Baseline Environment via VM clones
* Run STIG remediation script
* Disconnected Satellite Server Installation
* Org created
* Location x2 created
* Manifest upload
* CDN changed to Repo Server
* RHEL 7Server Repo Enabled
* RHEL 7.5 Kick Start Enabled
* Product Sync
* Custom Product Created
* Test RPM uploaded to Custom Product
* Content View Created x2
* Life Cycle Configured x2
* Host Collection Created
* Activation Key Created
* Host Group Configured
* Operating System Configured
* Installation Medium Created
* Domain Configured
* Subnet Configured
* DHCP Configured
* IDM Integration for SSO/Kerberos based login
* Realm Capsule Configured
* Client Registration to Satellite
* Client Successfully Accessed repos from Satellite
* External Capsule Installation
* External Capsule Configured for dedicated Content View
* External Capsule Configured for dedicated Life Cycle
* External Capsule Content Sync
* Client Registration to External Capsule
* Client Sucessfully Access repos from Capsule
* Satellite & Capsule services restart

## To Do / Not Tested:

* Configure External Capsule for Provisioning Services
* Configure Discovery Based Provisioning
* Test Provisioning Features
* Puppet
* Remote Execution
* etc


## For systems that have IDM client installed:
It was discovered that this script will break the systems ability for the IDM client to work properly. Currently Kyle Ritchie has developed an ansible based patch that will go back and restore the ability for the IDM client to connect.
At a later point I will migrate that work into this script.

https://github.com/superky13/ansible-admin-playbooks/blob/master/idmStigPatch.yml
