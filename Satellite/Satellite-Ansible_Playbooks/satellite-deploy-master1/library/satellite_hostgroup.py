#!/usr/bin/python
from ansible.module_utils.basic import *
from libs.ansible_satellite import *

DOCUMENTATION = """
---
module: satellite_hostgroup
version_added: 0.1
short_description: Manipulate Red Hat Satellite 6 Hostgroup
options:
    action:
        description:
            - Action to be performed by the module
        required: True
        choices: [ "create", "update" ]
    name:
        description:
            - Host group name
        required: True
    organization:
        description:
            - Organization name to be assigned to the content view
        required: True
    location:
        description:
            - Location name to be assigned to the content view
    contentview:
        description:
            - Content view to be assigned to the content view
        required: False
    environment:
        description:
            - Environment to be assigned to the HostGroup 
        required: False
    puppetenv:
        description:
            - Puppet environment to be assigned to the HostGroup
    puppetclasses:
        description:
            - Name of the puppet classes to be assigned to the HostGroup, if more than one comma sepparated
        required: False
"""

def manage_hostgroup(module):
    action = module.params['action']
    hostgroup_name = module.params['name']
    organization = module.params['organization']
    location = module.params['location']
    contentview = module.params['contentview']
    environment = module.params['environment']
    puppetenv = module.params['puppetenv']
    puppetclasses = module.params['puppetclasses']
    has_organization = False
    has_location = False  
    has_contentview = False
    has_environment = False
    has_puppetenv = False
    has_puppetclasses = False
    if organization != None:
        has_organization = True
    if location != None:
        has_location = True
    if contentview != None:
        has_contentview = True
    if environment != None:
        has_environment = True
    if puppetenv != None:
        has_puppetenv = True
    if puppetclasses != None:
        has_puppetclasses = True
 
    hostgroups = HostGroups()
    hostgroup_created = hostgroups.create_hostgroup(hostgroup_name)
    if hostgroup_created == 0 and action == "create":
        change = False
        output = "Hostgroup already exists"
    elif hostgroup_created == 1 or (hostgroup_created == 0 and action == "update"):
        change = True
        output = "Hostgroup " + str(hostgroup_name) + " created."
        if has_organization:
            organization_attached = hostgroups.attach_organization(hostgroup_name, organization)
            if organization_attached == 0:
                output = output + " Organization " + str(organization) + " attached."
            else:
                output = output + " Fail while attaching organization " + str(organization) + "."
        if has_location:
            location_attached = hostgroups.attach_location(hostgroup_name, location)
            if location_attached == 0:
                output = output + " Location " + str(location) + " attached."
            else:
                output = output + " Fail while attaching location " + str(location) + "." 
        if has_contentview or has_environment:
            content_attached = hostgroups.attach_content(hostgroup_name, contentview, environment, organization) 
            if content_attached  == 0:
                output = output + " Content view " + str(contentview) + " Env " + str(environment) + " attached."
            else:
                output = output + " Fail while attaching content view " + str(contentview) + " Env " + str(environment) + "."
        if has_puppetenv:
            puppetenv_attached = hostgroups.attach_puppetenv(hostgroup_name, puppetenv)
            if puppetenv_attached == 0:
                output = output + " Puppet env " + str(puppetenv) + " attached."
            else:
                output = output + " Fail while attaching puppet env " + str(puppetenv) + "."
        if has_puppetclasses:
            puppetclasses_attached = hostgroups.attach_puppetclass(hostgroup_name, puppetclasses)
            if puppetclasses_attached == 0:
                output = output + " Puppet classes " + str(puppetclasses) + " attached."
            else:
                output = output + " Fail while attaching puppet classes " + str(puppetclasses) + "."
    else:
        change = False
        output = "Error happened"
        module.fail_json(changed=change, msg=output)
    return change, output

def main():

  module = AnsibleModule(
      argument_spec     = dict(
          action        = dict(choices=['create' , 'update'], required=True),
          name          = dict(required=True, type='str'),
          organization  = dict(required=True, type='str'),
          location      = dict(required=False, type='str'),
          contentview   = dict(required=False, type='str'),
          environment   = dict(required=False, type='str'),
          puppetenv     = dict(required=False, type='str'),
          puppetclasses = dict(required=False, type='str')
      )
  )
  if module.params['action'] == "create" or module.params['action'] == "update":
      result, result_msg = manage_hostgroup(module)
  else:
      module.exit_json(changed=False, msg="not-implemented")

  module.exit_json(changed=result, msg=result_msg)

if __name__ == '__main__':
    main()

