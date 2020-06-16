#!/usr/bin/python
from ansible.module_utils.basic import *
from libs.ansible_satellite import *

DOCUMENTATION = """
---
module: satellite_activationkey
version_added: 0.1
short_description: Manipulate Red Hat Satellite 6 Activation Keys
options:
    action:
        description:
            - Action to be performed by the module
        required: True
        choices: [ "create", "add-subscription", "add-hostcollection", "content-override" ]
    name:
        description:
            - Content view name
        required: True
    organization:
        description:
            - Organization name
        required: True
    contentview:
        description:
            - Content view to be attached to the activation key
        required: False
    subscription:
         description:
            - Subscription to be attached to the activation key
         required: False
    hostcollection:
        description:
            - Host collection to be attached to the activation key
        required: False
    content_override:
        description:
            - Content to override. Content override pairs are supported with dictionary structure.
              eg.  content_override:
                     - content_name: rhel-7-server-satellite-tools-6.2-rpms
                       content_value: enable
                     - content_name: ... 
        required: False
"""

def create_activationkey(module):
    activationkey_name = module.params['name']
    organization = module.params['organization']
    contentview = module.params['contentview']
    subscription = module.params['subscription']
    hostcollection = module.params['hostcollection']
    content_override = module.params['content_override']
    has_subscription = False
    has_hostcollection = False
    has_content_override = False
    if subscription != None:
      has_subscription = True
    if hostcollection != None:
      has_hostcollection = True
    if content_override != None:
      has_content_override = True 
      for content in content_override:
          content_value = content["content_value"]
          if content_value not in ('enable', 'disable', 'default'):
              module.fail_json(changed=False, msg="content_value has to be one of: enable, disable or default. Got " + str(content_value))  
    akeys = ActivationKeys()
    ak_created = akeys.create_activationkey(activationkey_name, contentview, organization)
    if ak_created == 0:
        change = False
        output ="Activation key already exists"
    elif ak_created == 1:
        change = True
        output = "Activation key " + str(activationkey_name) + " created."
        if has_subscription:
            subscription_added = akeys.add_subscription(activationkey_name, subscription, organization)
            if subscription_added == 0 or subscription_added == 1:
                output = str(output) + "Subscription " + str(subscription) + " added." 
            else:
                output = str(output) + "Failed adding subscription " + str(subscription)
                module.fail_json(changed=change, msg=output)
        if has_hostcollection:
            hostcollection_added = akeys.add_hostcollection(activationkey_name, hostcollection, organization)
            if hostcollection_added == 0:
                output = str(output) + "Host collection " + str(hostcollection) + " added."
            else:
                output = str(output) + "Failed adding host collection " + str(hostcollection)
                module.fail_json(changed=change, msg=output)
        if has_content_override:
            for content in content_override:
                content_name = content["content_name"]
                content_value = content["content_value"]
                content_ovrr = akeys.content_override(activationkey_name, content_name, content_value, organization)
                if content_ovrr == 0:
                    output = str(output) + "Content " + str(content_name) + " set to " + str(content_value) + "."
                else:
                    output = str(output) + "Failed overriding content " + str(content_name) + " to " + str(content_value) + "."
                    module.fail_json(changed=change, msg=output)
    else:
        change = False
        output = "Error happened"
        module.fail_json(changed=change, msg=output)
    return change, output

def add_subscription(module):
    activationkey_name = module.params['name']
    organization = module.params['organization']
    subscription = module.params['subscription']
    akeys = ActivationKeys()
    subscription_added = akeys.add_subscription(activationkey_name, subscription, organization)
    if subscription_added == 0:
        change = True
        output = "Subscription " + str(subscription) + " added"
    elif subscription_added == 1:
        change = False
        output = "Subscription already present in activation key"
    else:
        change = False
        output = "Failed adding subscription"
        module.fail_json(changed=change, msg=output)
    return change, output

def add_hostcollection(module):
    activationkey_name = module.params['name']
    organization = module.params['organization']
    hostcollection = module.params['hostcollection']
    akeys = ActivationKeys()
    hostcollection_added = akeys.add_hostcollection(activationkey_name, hostcollection, organization)
    if hostcollection_added == 0:
        change = True
        output = "Host collection " + str(hostcollection) + " assigned"
    else:
        change = False
        output = "Failed adding host collection"
        module.fail_json(changed=change, msg=output)
    return change, output

def content_override(module):
    activationkey_name = module.params['name']
    organization = module.params['organization']
    content_override = module.params['content_override']
    change = False
    output = ""
    for content in content_override:
        content_value = content["content_value"]
        if content_value not in ('enable', 'disable', 'default'):
            module.fail_json(changed=False, msg="content_value has to be one of: enable, disable or default. Got " + str(content_value))  
    akeys = ActivationKeys()
    for content in content_override:
        content_name = content["content_name"]
        content_value = content["content_value"]
        content_ovrr = akeys.content_override(activationkey_name, content_name, content_value, organization)
        if content_ovrr == 0:
            change = True
            output = str(output) + "Content " + str(content_name) + " set to " + str(content_value) + "."
        else:
            output = str(output) + "Failed overriding content " + str(content_name) + " to " + str(content_value) + "."
            module.fail_json(changed=change, msg=output)
    return change, output


def main():

  module = AnsibleModule(
      argument_spec        = dict(
          action           = dict(choices=['create', 'add-subscription', 'add-hostcollection', 'content-override'], required=True),
          name             = dict(required=True, type='str'),
          organization     = dict(required=True, type='str'),
          contentview      = dict(required=False, type='str'),
          subscription     = dict(required=False, type='str'),
          hostcollection   = dict(required=False, type='str'),
          content_override = dict(required=False, type='list')
      ),
      required_if = [
                    [ 'action', 'create', [ 'contentview' ]],
                    [ 'action', 'add-subscription', [ 'subscription' ]],
                    [ 'action', 'add-hostcollection', [ 'hostcollection' ]],
                    [ 'action', 'content-override', [ 'content_override' ]]
      ]
  )

  if module.params['action'] == "create":
      result, result_msg = create_activationkey(module)
  elif module.params['action'] == "add-subscription":
      result, result_msg = add_subscription(module)
  elif module.params['action'] == "add-hostcollection":
      result, result_msg = add_hostcollection(module)
  elif module.params['action'] == "content-override":
      result, result_msg = content_override(module)
  else:
      module.exit_json(changed=False, msg="not-implemented")

  module.exit_json(changed=result, msg=result_msg)

if __name__ == '__main__':
    main()

