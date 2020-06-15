#!/usr/bin/python
from ansible.module_utils.basic import *
from libs.ansible_satellite import *

DOCUMENTATION = """
---
module: satellite_task
version_added: 0.1
short_description: Control Red Hat Satellite 6 tasks
options:
    task_type:
        description:
            - Task type to check for
        required: True
        choices: [ "repository_sync", "contentview_publish", "activationkey_create", "manifest_import", "enable_repository", "capsule_sync" ]
    check_every:
        description:
            - Check every X seconds
        required: True
    timeout:
        description:
            - Timeout after X seconds
        required: True
"""

def task_wait(module):
    task_type = module.params['task_type']
    check_every = module.params['check_every']
    timeout = module.params['timeout']

    tasks = Tasks()
    tasks_result = tasks.wait_for_task(task_type, check_every, timeout)

    if tasks_result == 0:
        change = False
        output = "No tasks running"
    else:
        change = False
        output = "Timeout while waiting"
        module.fail_json(changed=change, msg=output)
    return change, output

def main():

  module = AnsibleModule(
      argument_spec   = dict(
          task_type   = dict(choices=['repository_sync','contentview_publish','activationkey_create', 'manifest_import', 'enable_repository', 'capsule_sync'], required=True),
          check_every = dict(required=True, type='int'),
          timeout     = dict(required=True, type='int')
      )
  )

  result, result_msg = task_wait(module)
  module.exit_json(changed=result, msg=result_msg)

if __name__ == '__main__':
    main()
