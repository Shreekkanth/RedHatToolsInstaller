ipa-audit
=========

ipa-audit can be used to automate the configuration of audit feeds on Red Hat
Identity Management Servers.

Requirements
------------

ipa-audit requires that the 389DS audit functionality is enabled and configured via ldapmodify
LDIF - this is not performed by this role.

We also rely on the ldap-access-parser package. This is a Github project located at
https://github.com/aidan-/ldap-access-parser, and has been packaged as an RPM available for installation
inside the customer environment.


Role Variables
--------------
* `audit_repo_url`:  URL of the ldap-access-parser package (string, mandatory)
* `ipa_server_ds_secret`: Directory Manager password
* `realm_name`: Domain of the IPA realm (string, mandatory)
* `lap_bin_path`: Full path to 'lap' binary (string, mandatory)
* `audit_server_url`: URL of the audit collector
* `audit_prefix`: Prefix of the audit collector variables in the configs (string, mandatory)
* `audit_system`: System Name to use within the audit feed (string, mandatory)
* `audit_environment`: Environment of the IPA system (e.g. Quality) (string, mandatory)
* `audit_audit_feed_name`: Name of the Audit feed log (string, mandatory)
* `audit_access_feed_name`: Name of the Access log feed (string, mandatory)
* `audit_feed_package_name`: Name of the RPM package that delivers the audit feed (string, mandatory)


Example Playbook
----------------

    ---
    # site.yml
    # Role inclusion workflow

    - hosts: servers
      roles:
        - role: ipa-audit
          audit_repo_url: https://repo.example.com/rpms/ldap-access-parser-0.2.2-1.el7.x86_64.rpm
          ipa_server_ds_secret: "N0b0dykn0w$"
          realm_name: "QA.EXAMPLE.COM.AU"
          lap_bin_path: "/usr/local/bin/lap"
          audit_server_url: "https://audit.example.com/datafeed"
          audit_prefix: "AUDIT"
          audit_system: "DEVILHORN"
          audit_environment: "Quality"
          audit_audit_feed_name: "IPA-LDAP-AUDIT-EVENTS"
          audit_access_feed_name: "IPA-LDAP-ACCESS-EVENTS"
          audit_feed_package_name: "my_auditd_agent"


Author Information
------------------

Devil Horn project

maintainer: tbd@tbd.com

JIRA: https://redhat-anzservices.atlassian.net/secure/RapidBoard.jspa?rapidView=7
