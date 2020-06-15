#!/usr/bin/python

#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# (c) 2012, Red Hat, Inc
# Written by Jean Figarella <jean at redhat.com>
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

import os
#import json

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'core',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: ntp_conf_check
version_added: historical
short_description: Check for configuration lines in ntp configuration

description:
     - Checks for configuration in the /etc/ntp.conf file

options:

# informational: requirements for nodes
author:
    - "Red Hat Consulting (NAPS)"
    - "Jean Figarella"
'''

EXAMPLES = '''
  - name: Get subscription manager indentity informnation
    redhat_subscription_identity:
    resgister: response

  - debug: var=response

'''
def is_line_in_file(line, file):
    #print line
    for j in open(file):
        if line == j.rstrip():
            return 'present'
    return 'absent'


def check_ntp_config(lines, ntp_file):
    tempjson = {}
    rc = 0

    for line in lines:
        #print line
        tempjson[line] = is_line_in_file(line, ntp_file)
        if tempjson[line] == 'absent':
            rc = 1
    return rc, tempjson


def main():
    module = AnsibleModule(
        argument_spec = dict(
            config_lines  = dict(required=True, type='list'),
            ntp_version   = dict(default='chrony', choices=['chrony', 'ntp']),
            state         = dict(default='present', choices=['present', 'absent'])
        ),
        supports_check_mode = True
    )

    params = module.params

    config_lines = params.get('config_lines', '')
    ntp_version = params.get('ntp_versions', '')
    state = params.get('state', '')

    if ntp_version == "chrony":
        ntp_file = "/etc/chrony.conf"
    else:
        ntp_file = "/etc/ntp.conf"

    exists=os.path.isfile(ntp_file)
    if exists:
        rc,linestat = check_ntp_config(config_lines, ntp_file)
    else:
        rc = 1
        
    tempjson = {}

    if rc == 0:
        tempjson["linestat"] = linestat
        module.exit_json(**tempjson)
    elif exists == False:
        failmsg = "File %s does not exist. Please make sure that %s is installed on target system." % (ntp_file, ntp_version)
        tempjson["linestat"] = linestat
        module.exit_json(rc=rc, **tempjson)
    else:
        failmsg = "One of more configuration lines are absent"
        tempjson["linestat"] = linestat
        module.exit_json(rc=rc, **tempjson)
        #module.fail_json(rc=rc, msg=failmsg)

# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
if __name__ == '__main__':
    main()
