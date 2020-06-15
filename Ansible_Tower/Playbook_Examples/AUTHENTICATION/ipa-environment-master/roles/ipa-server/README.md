ipa-server
=========

ipa-server can be used to automate the provisioning of Red Hat IdM servers into
an Red Hat Identity Management Realm.

Requirements
------------


Role Variables
--------------
* `realm_name`: Name of the ipa realm. (string, mandatory)
* `external_dns`: Address of external_dns provider (string, default: nil)
* `ipa_server_enable_dns`: Enable self managed dns provider. This option is currently experimental. (string, default: nil)
* `ipa_server_ds_secret`: Password for cn=Directory Manager (string, mandatory)
* `ipa_server_admin_secret`: Password for admin user (string, mandatory)

This role currently supports two modes for the certificate authority, self signed
(default), and no CA-less.
* `ipa_server_enable_ca`: Deploy self signed certificate authority. By disabling
the self signed certificate authority certificates for the http and ldap interfaces to IPA are required (boolean, default: true)
* `ipa_server_http_cert_file`: File containing the Apache Server SSL certificate (string, default: nil)
* `ipa_server_http_key_file`: File containing the Apache Server SSL private key (string, default: nil)
* `ipa_server_http_pin`: The password to unlock the Apache Server private key (string, default: nil)
* `ipa_server_dirsrv_cert_file`: File containing the Directory Server SSL certificate (string, default: nil)
* `ipa_server_cert_key_file`: File containing the Directory Server SSL private key (string, default: nil)
* `ipa_server_dirsrv_pin`: The password to unlock the Directory Server private key (string, default: nil)
* `ipa_server_ca_cert_file`: File containing CA certificates for the service certificate files (string, default: nil)
* `ipa_server_recovery_path`: Where CA artefacts are stored on completion (string, default: nil)

* `ipa_server_no_hbac_allow_all`: Don't install allow_all HBAC rule. This can be toggled post installation (boolean, default: false)
* `ipa_server_recovery_path`: Directory to recover CA private keys on the control host. (string, Default: "")
* `ipa_server_start_uid`: The starting value for the IDs range (int, default: nil)
* `ipa_server_max_uid`: The max value for the IDs range (int, default: nil)

Example Playbook
----------------

    - hosts: ipa-server
      vars:
        ipa_server_enable_ca: true
        ipa_server_enable_dns: false
      roles:
        - role: ipa-server
          ipa_server_no_hbac_allow_all: true

License
-------

LGPL

Author Information
------------------

Devil Horn project

maintainer: tbd@tbd.com

JIRA: https://redhat-anzservices.atlassian.net/secure/RapidBoard.jspa?rapidView=7
