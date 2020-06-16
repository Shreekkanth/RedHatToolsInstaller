#!/usr/bin/python
from ansible.module_utils.basic import *
from libs.ansible_satellite import *

DOCUMENTATION = """
---
module: satellite_contentview
version_added: 0.1
short_description: Manipulate Red Hat Satellite 6 Content Views
options:
    action:
        description:
            - Action to be performed by the module
        required: True
        choices: [ "create", "publish", "promote", "add-module" ]
    name:
        description:
            - Content view name
        required: True
    organization:
        description:
            - Organization name
        required: True
    repositories:
        description:
            - Repositories to be added to the content view, comma separated
        required: False
    environment:
        description:
            - Environment to promote the content view to. Caution: Case sensitive
        required: False
    module:
        description:
            - Name of the module to be added to the content view
        required: False
    version:
        description:
            - Content view version to be promoted
        default: Latest
        required: False
    bypass_restrictions:
        description:
            - Bypass lifecycle environment restrictions when promoting a cv
        default: False
        required: False
"""

def create_contentview(module):
    contentview_name = module.params['name']
    organization = module.params['organization']
    repositories = module.params['repositories']
    contentviews = ContentViews()
    contentview_created = contentviews.create_contentview(contentview_name, organization, repositories)
    if contentview_created == 0:
        change = False
        output = "Content view already exists"
    elif contentview_created == 1:
        change = True
        output = "Content view " + str(contentview_name) + " created"
    else:
        change = False
        output = "Error happened"
        module.fail_json(changed=change, msg=output)
    return change, output

def publish_contentview(module):
    contentview_name = module.params['name']
    organization = module.params['organization']
    contentviews = ContentViews()
    contentview_published = contentviews.publish_contentview(contentview_name, organization)
    if contentview_published == 0:
        change = True
        output = "Content view " + str(contentview_name) + " published"
    else:
        change = False
        output = "Error happened"
        module.fail_json(changed=change, msg=output)
    return change, output

def promote_contentview(module):
    contentview_name = module.params['name']
    organization = module.params['organization']
    environment = module.params['environment']
    version = module.params['version'] 
    restrictions = module.params['bypass_restrictions']
    if restrictions == None:
      restrictions = False
    if version == None:
      version = "latest"
    contentviews = ContentViews()
    contentview_promoted = contentviews.promote_contentview(contentview_name, organization, environment, version, restrictions)
    if contentview_promoted == 0:
        change = True
        output = "Content view " + str(contentview_name) + " promoted"
    else:
        change = False
        output = "Error happened"
        module.fail_json(changed=change, msg=output)
    return change, output
    
def add_module(module):
    contentview_name = module.params['name']
    module_name = module.params['module']
    organization = module.params['organization']
    contentviews = ContentViews()
    added_module = contentviews.add_module(contentview_name, organization, module_name)
    if added_module == 0:
        change = False
        output = "Module " + str(module_name) + " already exists in the cv"
    elif added_module == 1:
        change = True
        output = "Module " + str(module_name) + " added to the content view"
    else:
        change = False
        output = "Error happened"
        module.fail_json(changed=change, msg=output)
    return change, output
def main():

  module = AnsibleModule(
      argument_spec    = dict(
          action       = dict(choices=['create' , 'publish', 'promote', 'add-module'], required=True),
          name         = dict(required=True, type='str'),
          organization = dict(required=True, type='str'),
          module       = dict(required=False, type='str'),
          repositories = dict(required=False, type='str'),
          environment  = dict(required=False, type='str'),
          version      = dict(required=False, type='str'),
          bypass_restrictions = dict(required=False, type='bool')
      ),
      required_if = [
                    [ 'action', 'promote', [ 'environment' ]],
                    [ 'action', 'add-module', [ 'module' ]]
      ]
  )
  if module.params['action'] == "create":
      result, result_msg = create_contentview(module)
  elif module.params['action'] == "publish":
      result, result_msg = publish_contentview(module)
  elif module.params['action'] == "promote":
      result, result_msg = promote_contentview(module)
  elif module.params['action'] == "add-module":
      result, result_msg = add_module(module)
  else:
      module.exit_json(changed=False, msg="not-implemented")

  module.exit_json(changed=result, msg=result_msg)

if __name__ == '__main__':
    main()

