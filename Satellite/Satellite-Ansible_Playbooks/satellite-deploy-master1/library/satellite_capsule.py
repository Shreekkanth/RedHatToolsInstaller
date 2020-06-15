#!/usr/bin/python
from ansible.module_utils.basic import *
from libs.ansible_satellite import *

DOCUMENTATION = """
---
module: satellite_capsule
version_added: 0.1
short_description: Manipulate Red Hat Satellite 6 Capsules
options:
    action:
        description:
            - Action to be performed by the module
        required: True
        choices: [ "set-locations", "set-organizations", "set-environment", "sync-content" ]
    name:
        description:
            - Capsule name
        required: True
    organizations:
        description:
            - Organizations name, comma separated
        required: False
    locations:
        description:
            - Locations name, comma separated
        required: False
    environment:
        description:
            - Environment to assign the capsule to. Caution: Case sensitive
        required: False
    organization:
        description:
            - Organization where environment is created
        required: False 
"""

def sync_content(module):
    capsule_name = module.params['name']
    capsule = Capsule()
    sync_started = capsule.sync_content(capsule_name)
    if sync_started == 0:
        change = True
        output = "Synchronization has started"
    elif sync_started == 1:
        change = False
        output = "Capsule " + str(capsule_name) + " is not a pulp node"
    else:
        change = False
        output = "Error happened"
        module.fail_json(changed=change, msg=output)
    return change, output

def set_locations(module):
    capsule_name = module.params['name']
    locations = module.params['locations']
    capsule = Capsule()
    locations_assigned = capsule.set_locations(capsule_name, locations)
    if locations_assigned == 0:
        change = True
        output = "Locations " + str(locations) + " assigned to Capsule " + str(capsule_name)
    else:
        change = False
        output = "Error happened"
        module.fail_json(changed=change, msg=output)
    return change, output

def set_organizations(module):
    capsule_name = module.params['name']
    organizations = module.params['organizations']
    capsule = Capsule()
    organizations_assigned = capsule.set_organizations(capsule_name, organizations)
    if organizations_assigned == 0:
        change = True
        output = "Organizations " + str(organizations) + " assigned to Capsule " + str(capsule_name)
    else:
        change = False
        output = "Error happened"
        module.fail_json(changed=change, msg=output)
    return change, output

def set_environment(module):
    capsule_name = module.params['name']
    environment = module.params['environment']
    organization = module.params['organization']
    capsule = Capsule()
    environment_assigned = capsule.set_lifecycle_env(capsule_name, organization, environment)
    if environment_assigned == 0:
        change = False
        output = "Environment already assigned"
    elif environment_assigned == 1:
        change = True
        output = "Environment " + str(environment) + " assigned to Capsule " + str(capsule_name)
    elif environment_assigned == 2:
        change = False
        output = "Capsule " + str(capsule_name) + " is not a pulp node"
    else:
        change = False
        output = "Error happened"
        module.fail_json(changed=change, msg=output)
    return change, output


def main():

  module = AnsibleModule(
      argument_spec     = dict(
          action        = dict(choices=['set-locations' , 'set-organizations', 'set-environment', 'sync-content'], required=True),
          name          = dict(required=True, type='str'),
          organizations = dict(required=False, type='str'),
          organization  = dict(required=False, type='str'),
          locations     = dict(required=False, type='str'),
          environment   = dict(required=False, type='str')
      ),
      required_if = [
                    [ 'action', 'set-locations', [ 'locations' ]],
                    [ 'action', 'set-organizations', [ 'organizations' ]],
                    [ 'action', 'set-environment', [ 'environment', 'organization' ]]
      ]
  )
  if module.params['action'] == "set-locations":
      result, result_msg = set_locations(module)
  elif module.params['action'] == "set-organizations":
      result, result_msg = set_organizations(module)
  elif module.params['action'] == "set-environment":
      result, result_msg = set_environment(module)
  elif module.params['action'] == "sync-content":
      result, result_msg = sync_content(module)
  else:
      module.exit_json(changed=False, msg="not-implemented")

  module.exit_json(changed=result, msg=result_msg)

if __name__ == '__main__':
    main()

