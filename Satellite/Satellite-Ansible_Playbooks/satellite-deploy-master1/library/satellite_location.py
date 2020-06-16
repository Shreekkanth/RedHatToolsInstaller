#!/usr/bin/python
from ansible.module_utils.basic import *
from libs.ansible_satellite import *

DOCUMENTATION = """
---
module: satellite_location
version_added: 0.1
short_description: Manipulate Red Hat Satellite 6 locations
options:
    name:
        description:
            - Location name
        required: True
"""

def create_location(module):
    location_name = module.params['name']
    locations = Locations()
    location_created = locations.create_location(location_name)
    if location_created == 0:
        change = False
        output = "Location already exists"
    elif location_created == 1:
        change = True
        output = "Location " + str(location_name) + " created"
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

  result, result_msg = create_location(module)
  module.exit_json(changed=result, msg=result_msg)

if __name__ == '__main__':
    main()
