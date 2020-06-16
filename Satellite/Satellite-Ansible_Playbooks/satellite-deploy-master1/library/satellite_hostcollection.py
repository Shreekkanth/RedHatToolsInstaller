#!/usr/bin/python
from ansible.module_utils.basic import *
from libs.ansible_satellite import *

DOCUMENTATION = """
---
module: satellite_hostcollection
version_added: 0.1
short_description: Manipulate Red Hat Satellite 6 hostcollections
options:
    name:
        description:
            - Host collection name
        required: True
    organization:
        description:
            - Organization name
        required: True
"""

def create_hostcollection(module):
    hostcollection_name = module.params['name']
    organization = module.params['organization']
    hostcollections = HostCollections()
    hostcollection_created = hostcollections.create_hostcollection(hostcollection_name, organization)
    if hostcollection_created == 0:
        change = False
        output = "Host collection already exists"
    elif hostcollection_created == 1:
        change = True
        output = "Host collection " + str(hostcollection_name) + " created"
    else:
        change = False
        output = "Error happened"
        module.fail_json(changed=change, msg=output)
    return change, output

def main():

  module = AnsibleModule(
      argument_spec    = dict(
          name         = dict(required=True, type='str'),
          organization = dict(required=True, type='str')
      )
  )

  result, result_msg = create_hostcollection(module)
  module.exit_json(changed=result, msg=result_msg)

if __name__ == '__main__':
    main()
