#!/usr/bin/python
from ansible.module_utils.basic import *
from libs.ansible_satellite import *

DOCUMENTATION = """
---
module: satellite_manifest
version_added: 0.1
short_description: Manipulate Red Hat Satellite 6 Subscriptions Manifest
options:
    manifest_zip:
        description:
            - Path to the subscription manifest zip file
        required: True
    force:
        description:
            - If a subscription is already uploaded delete it and then import the new one
        required: False
        default: False
    organization:
        description:
            - Organization name
        required: True
"""

def upload_manifest(module):
    manifest_zip = module.params['manifest_zip']
    force_upload = module.params['force']
    organization = module.params['organization']
    if force_upload == None:
      force_upload = False
    subscription_manifest = SubscriptionManifest()
    manifest_uploaded = subscription_manifest.upload_subscription_manifest(organization, manifest_zip, force_upload)
    if manifest_uploaded == 0:
        change = True
        output = "Manifest file successfully uploaded"
    elif manifest_uploaded == 1:
        change = False
        output = "A manifest file is already uploaded to this organization"
    else:
        change = False
        output = "Error happened"
        module.fail_json(changed=change, msg=output)
    return change, output

def main():

  module = AnsibleModule(
      argument_spec             = dict(
          manifest_zip          = dict(required=True, type='str'),
          force                 = dict(required=False, type='bool'),
          organization          = dict(required=True, type='str')
      )
  )

  result, result_msg = upload_manifest(module)
  module.exit_json(changed=result, msg=result_msg)

if __name__ == '__main__':
    main()
