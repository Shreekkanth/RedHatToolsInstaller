#!/usr/bin/python
from ansible.module_utils.basic import *
from libs.ansible_satellite import *

DOCUMENTATION = """
---
module: satellite_repository
version_added: 0.1
short_description: Manipulate Red Hat Satellite 6 Repositories
options:
    action:
        description:
            - Action to be performed by the module
        required: True
        choices: [ "create", "manage", "synchronize", "upload-content" ]
    product_name:
        description:
            - Product name where repositories to be enabled reside. Only used when action is manage
        required: False
    repo_name:
        description:
            - Repository name.
        required: False
    content_type:
        description:
            - When creating a repo, defines the repo type: must be one of: puppet, yum, ostree, file, docker
        choices: [ "puppet", "yum", "ostree", "file", "docker" ]
        required: False
    content_file:
        description:
            - File to be uploaded to the repository
        required: False
    basearch:
        description:
            - Repository basearch
        required: False
    releasever:
        description:
            - Repository release version
        required: False
    task:
        description:
            - Action to perform against the repo
        required: False
        choices: [ "enable", "disable" ]
    organization:
        description:
            - Organization name
        required: True
"""

def create_repository(module):
    product_name = module.params['product_name']
    repo_name = module.params['repo_name']
    organization = module.params['organization']
    content_type = module.params['content_type']

    repositories = Repositories()
    create_repo = repositories.create_repo(organization, product_name, repo_name, content_type)
  
    if create_repo == 0:
        change = False
        output = "Repo " + str(repo_name) + " already exists"
    elif create_repo == 1:
        change =  True
        output = "Repo " + str(repo_name) + " has been created"
    else:
        change = False
        output = "Error happened" 
        module.fail_json(changed=change, msg=output)
    return change, output

def upload_content(module):
    organization = module.params['organization']
    repo_name = module.params['repo_name']
    content_file = module.params['content_file']
   
    repositories = Repositories()
    upload_content = repositories.upload_content(organization, content_file, repo_name)
    
    if upload_content == 0:
        change = True
        output = "Content " + str(content_file) + " uploaded"
    else:
        change = False
        output = "Error happened"
        module.fail_json(changed=change, msg=output)
    return change, output

def manage_repository(module):
    product_name = module.params['product_name']
    repo_name = module.params['repo_name']
    basearch = module.params['basearch']
    releasever = module.params['releasever']
    organization = module.params['organization']
    task = module.params['task']
    
    repositories = Repositories()
    manage_repo = repositories.manage_repo(organization, product_name, repo_name, basearch, releasever, task)

    if manage_repo == 0:
        change = True
        output = "Repo " + str(repo_name) + " successfully " + str(task)
    elif manage_repo == 1:
        change = False
        output = "Repo " + str(repo_name) + " is already " + str(task)
    else:
        change = False
        output = "Error happened while trying to perform " + str(task) + " on repository " + str(repo_name)
        module.fail_json(changed=change, msg=output)
    return change, output


def synchronize_repository(module):
    repo_name = module.params['repo_name']
    organization = module.params['organization']

    repositories = Repositories()
    repo_sync = repositories.synchronize_repo(organization, repo_name.strip())
    if repo_sync == 0:
        change = True
        output = "Repo has been scheduled to be synched"
    else:
        change = False
        output = "Error happened while trying to synchronize the repository"
        module.fail_json(changed=change, msg=output)
    return change, output


def main():

  module = AnsibleModule(
      argument_spec     = dict(
          action        = dict(choices=['create', 'manage', 'synchronize', 'upload-content'], required=True),
          product_name  = dict(required=False, type='str'),
          repo_name     = dict(required=False, type='str'),
          content_type  = dict(choices=['puppet', 'yum', 'ostree', 'file', 'docker'], required=False, type='str'),
          content_file  = dict(required=False, type='str'),
          basearch      = dict(required=False, type='str'),
          releasever    = dict(required=False, type='str'),
          task          = dict(choices=['enable', 'disable'], required=False),
          organization  = dict(required=True, type='str')
      ),
      required_if = [
                    [ 'action', 'create', [ 'product_name', 'repo_name', 'content_type' ]],
                    [ 'action', 'upload-content', ['repo_name', 'content_file' ]],
                    [ 'action', 'manage', [ 'product_name', 'repo_name', 'basearch', 'releasever', 'task' ]],
                    [ 'action', 'synchronize', [ 'repo_name' ]]
      ]
#      required_together = [ 
#                          ['product_name', 'repo_name', 'basearch', 'releasever', 'task'],
#                          ['repo_name', 'task']
#      ]
  )
  if module.params['action'] == "create":
      result, result_msg = create_repository(module)
  elif module.params['action'] == "manage":
      result, result_msg = manage_repository(module)
  elif module.params['action'] == "upload-content":
      result, result_msg = upload_content(module)
  elif module.params['action'] == "synchronize":
      result, result_msg = synchronize_repository(module)
  else:
     module.fail_json(changed=False, msg="not-implemented")

  module.exit_json(changed=result, msg=result_msg)

if __name__ == '__main__':
    main()

