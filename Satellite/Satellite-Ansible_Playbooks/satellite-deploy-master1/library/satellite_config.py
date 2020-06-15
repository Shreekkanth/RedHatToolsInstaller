#!/usr/bin/python
from ansible.module_utils.basic import *
from libs.ansible_satellite import *

DOCUMENTATION = """
---
module: satellite_config
version_added: 0.1
short_description: Manipulate Red Hat Satellite 6 settings
options:
    setting:
        description:
            - Setting's name
        required: True
    value:
        description:
            - Setting's value
        required: True
"""

def change_setting(module):
    setting_name = module.params['setting']
    setting_value = module.params['value']
    settings = Settings()
    setting_modified = settings.update_setting(setting_name, setting_value)
    if setting_modified == 0:
        change = True
        output = "Setting updated"
    else:
        change = False
        output = "Error happened"
        module.fail_json(changed=change, msg=output)
    return change, output

def main():

  module = AnsibleModule(
      argument_spec    = dict(
          setting      = dict(required=True, type='str'),
          value        = dict(required=True, type='str')
      )
  )

  result, result_msg = change_setting(module)
  module.exit_json(changed=result, msg=result_msg)

if __name__ == '__main__':
    main()
