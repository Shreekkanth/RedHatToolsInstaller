#!/usr/bin/python
from ansible.module_utils.basic import *
from libs.ansible_satellite import *

DOCUMENTATION = """
---
module: satellite_syncplan
version_added: 0.1
short_description: Manipulate Red Hat Satellite 6 Content Views
options:
    name:
        description:
            - Sync Plan name
        required: True
    description:
        description:
            - Sync Plan description
        required: False
    organization:
        description:
            - Organization name
        required: True
    interval:
        description:
            - Synchronization schedule
        choices: [ "hourly", "daily", "weekly" ]
        required: True 
    startdate:
        description: 
            - When first sync will occur, afterwards it will follow the interval defined. e.g: 2017/03/31 18:25:00 CEST 
        required: True
    products:
        description:
            - Products to be added to the sync plan, comma separated
        required: False
    enabled:
        description:
            - Enable / disable sync plan on creation
        required: False
        choices: [ "yes", "no" ]
        default: false
"""

def create_syncplan(module):
    syncplan_name = module.params['name']
    description = module.params['description'] 
    organization = module.params['organization']
    interval = module.params['interval']
    startdate = module.params['startdate']
    products = module.params['products']
    enabled = module.params['enabled']
    if description == None:
        description = "No description"
    if enabled == None or enabled.lower() not in ("yes", "no"):
        enable_syncplan = False
    if enabled.lower() == "yes":
        enable_syncplan = True   
    syncplans = SyncPlans()
    syncplan_created = syncplans.create_syncplan(syncplan_name, organization, interval, startdate, description, products, enable_syncplan)
    if syncplan_created == 0:
        change = False
        output = "Sync plan already exists"
    elif syncplan_created == 1:
        change = True
        output = "Sync plan " + str(syncplan_name) + " created"
    else:
        change = False
        output = "Error happened"
        module.fail_json(changed=change, msg=output)
    return change, output

def main():

  module = AnsibleModule(
      argument_spec    = dict(
          name         = dict(required=True, type='str'),
          description  = dict(required=False, type='str'),
          organization = dict(required=True, type='str'),
          interval     = dict(choices=['hourly','daily','weekly'], required=True, type='str'),
          startdate    = dict(required=True, type='str'),
          products     = dict(required=False, type='str'),
          enabled      = dict(required=False, type='str')
      )
  )
  
  result, result_msg = create_syncplan(module)

  module.exit_json(changed=result, msg=result_msg)

if __name__ == '__main__':
    main()

