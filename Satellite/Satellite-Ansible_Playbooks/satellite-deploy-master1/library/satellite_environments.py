#!/usr/bin/python
from ansible.module_utils.basic import *
from libs.ansible_satellite import *

DOCUMENTATION = """
---
module: satellite_environments
version_added: 0.1
short_description: Manipulate Red Hat Satellite 6 Life Cycle Environments
options:
    name:
        description:
            - Environment name
        required: True
    previous_envionment:
        description:
            - Previous environment name in the Life cycle
        required: True
    force:
        description:
            - If an environment with the same name already exists, it will be created anyway
        required: False
        default: False
    organization:
        description:
            - Organization name
        required: True
"""

def create_environment(module):
    environment_name = module.params['name']
    previous_environment_name = module.params['previous_environment']
    organization = module.params['organization']
    lifecycle_env = LifecycleEnvs()
    lf_created = lifecycle_env.create_lifecycle_env(environment_name, previous_environment_name, organization)
    if lf_created == 0:
        change = False
        output = "Environment already exists"
    elif lf_created == 1:
        change = True
        output = "Environment " + str(environment_name) + " created"
    else:
        change = False
        output = "Error happened"
        module.fail_json(changed=change, msg=output)
    return change, output

def main():

  module = AnsibleModule(
      argument_spec             = dict(
          name                  = dict(required=True, type='str'),
          previous_environment  = dict(required=True, type='str'),
          organization          = dict(required=True, type='str')
      )
  )

  result, result_msg = create_environment(module)
  module.exit_json(changed=result, msg=result_msg)

if __name__ == '__main__':
    main()
