#!/usr/bin/python
from ansible.module_utils.basic import *
from libs.ansible_satellite import *

DOCUMENTATION = """
---
module: satellite_product
version_added: 0.1
short_description: Manipulate Red Hat Satellite 6 Products
options:
    action:
        description:
            - Action to be performed by the module
        required: True
        choices: [ "create" ]
    product_name:
        description:
            - Product name 
        required: False
    organization:
        description:
            - Organization name
        required: True
"""

def create_product(module):
    product_name = module.params['product_name']
    organization = module.params['organization']

    repositories = Repositories()
    create_product = repositories.create_product(organization, product_name)
  
    if create_product == 0:
        change = False
        output = "Product " + str(product_name) + " already exists"
    elif create_product == 1:
        change =  True
        output = "Product " + str(product_name) + " has been created"
    else:
        change = False
        output = "Error happened" 
        module.fail_json(changed=change, msg=output)
    return change, output

def main():

  module = AnsibleModule(
      argument_spec     = dict(
          action        = dict(choices=['create'], required=True),
          product_name  = dict(required=False, type='str'),
          organization  = dict(required=True, type='str')
      ),
  )

  if module.params['action'] == "create":
      result, result_msg = create_product(module)
  else:
     module.fail_json(changed=False, msg="not-implemented")

  module.exit_json(changed=result, msg=result_msg)

if __name__ == '__main__':
    main()

