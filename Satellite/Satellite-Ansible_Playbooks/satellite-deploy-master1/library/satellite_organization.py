#!/usr/bin/python
from ansible.module_utils.basic import *
from libs.ansible_satellite import *

DOCUMENTATION = """
---
module: satellite_organization
version_added: 0.1
short_description: Manipulate Red Hat Satellite 6 organizations
options:
    name:
        description:
            - Organization name
        required: True
"""

def create_organization(module):
    organization_name = module.params['name']
    organizations = Organizations()
    organization_created = organizations.create_organization(organization_name)
    if organization_created == 0:
        change = False
        output = "Organization already exists"
    elif organization_created == 1:
        change = True
        output = "Organization " + str(organization_name) + " created"
    else:
        change = False
        output = "Error happened"
        module.fail_json(changed=change, msg=output)
    return change, output

def main():

  module = AnsibleModule(
      argument_spec = dict(
          name      = dict(required=True, type='str')
      )
  )

  result, result_msg = create_organization(module)
  module.exit_json(changed=result, msg=result_msg)

if __name__ == '__main__':
    main()
