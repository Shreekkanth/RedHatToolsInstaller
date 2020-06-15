#!/usr/bin/python
from ansible.module_utils.basic import *
from libs.ansible_satellite import *

DOCUMENTATION = """
---
module: satellite_ldap
version_added: 0.1
short_description: Manipulate Red Hat Satellite 6 ldap auth
options:
    name:
        description:
            - Ldap connection name
        required: True
    ldap_host:
        description:
            - Ldap Host
        required: True
    ldap_port:
        description:
            - Ldap Port, defaults to 389
        required: False
    ldap_account:
        description:
            - Account used to bind. $login can be used and will be changed with the user that actually logs on
        required: False
    account_password:
        description:
            - Password of bind user. If $login is used, it should be empty
        required: False
    base_dn:
        description:
            - Ldap base dn
        required: False
    group_base:
        description:
            - Ldap group dn
        required: False
    auto_register:
        description:
            - Auto register ldap users in satellite
        required: False
    group_sync:
        description:
            - Sync ldap groups in satellite
        required: False
    attr_login:
        description:
            - Ldap login attribute
        required: False
    attr_name:
        description:
            - Ldap name attribute
        required: False
    attr_lastname:
        description:
            - Ldap surname attribute
        required: False
    attr_mail:
        description:
            - Ldap email attribute
        required: False
    attr_photo:
        description:
            - Ldap photo attribute
        required: False
    tls:
        description:
            - Use TLS connection (ldaps)
        required: False
    server_type:
        description:
            - Ldap server type
        required: False
        choices: [ "free_ipa", "active_directory", "posix" ]
    ldap_filter:
        description:
            - Ldap filter to be applied on user queries
        required: False
    locations:
        description:
            - Locations to be assigned to the ldap auth method, comma separated 
        required: False
    organizations:
        description:
            - Organizations to be assigned to the ldap auth method, comma separated 
        required: False
"""

def config_ldap(module):
    name = module.params['name']
    ldap_host = module.params['ldap_host']
    ldap_port = module.params['ldap_port']
    ldap_account = module.params['ldap_account']
    account_password = module.params['account_password']
    base_dn = module.params['base_dn']
    group_base = module.params['group_base']
    auto_register = module.params['auto_register']
    group_sync = module.params['group_sync']
    attr_login = module.params['attr_login']
    attr_name = module.params['attr_name']
    attr_lastname = module.params['attr_lastname']
    attr_mail = module.params['attr_mail']
    attr_photo = module.params['attr_photo']
    tls = module.params['tls']
    server_type = module.params['server_type']
    ldap_filter = module.params['ldap_filter']
    locations = module.params['locations']
    organizations = module.params['organizations']



    settings = Settings()
    ldap_added = settings.ldap_auth(name, ldap_host, ldap_port, ldap_account, account_password, base_dn,                                    attr_login, attr_name, attr_lastname, attr_mail, attr_photo,                                            auto_register, group_sync, tls, group_base, server_type,
                                    ldap_filter, locations, organizations)
    if ldap_added == 0:
        change = True
        output = "Ldap Configured"
    elif ldap_added == 1:
        change = False
        output = "Ldap already configured"
    else:
        change = False
        output = "Error happened"
        module.fail_json(changed=change, msg=output)
    return change, output

def main():

  module = AnsibleModule(
      argument_spec = dict(
          name             = dict(required=True, type='str'),
          ldap_host        = dict(required=True, type='str'),
          ldap_port        = dict(required=False, type='str'),
          ldap_account     = dict(required=False, type='str'),
          account_password = dict(required=False, type='str'),
          base_dn          = dict(required=False, type='str'),
          attr_login       = dict(required=False, type='str'),
          attr_name        = dict(required=False, type='str'),
          attr_lastname    = dict(required=False, type='str'),
          attr_mail        = dict(required=False, type='str'),
          attr_photo       = dict(required=False, type='str'),
          auto_register    = dict(required=False, type='bool'),
          group_sync       = dict(required=False, type='bool'),
          tls              = dict(required=False, type='bool'),
          group_base       = dict(required=False, type='str'),
          server_type      = dict(choices=['free_ipa','active_directory','posix'], required=False),
          ldap_filter      = dict(required=False, type='str'),
          locations        = dict(required=False, type='str'),
          organizations    = dict(required=False, type='str')
      )
  )

  result, result_msg = config_ldap(module)
  module.exit_json(changed=result, msg=result_msg)

if __name__ == '__main__':
    main()
