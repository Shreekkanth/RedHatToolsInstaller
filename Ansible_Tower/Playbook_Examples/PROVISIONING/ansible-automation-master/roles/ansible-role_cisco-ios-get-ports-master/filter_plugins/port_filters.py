# Copyright (c) 2018 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re
from datetime import timedelta

# from ansible.module_utils.six import string_types
# from ansible.errors import AnsibleFilterError

regex = re.compile(r'((?P<years>\d+?)y)?((?P<weeks>\d+?)w)?((?P<days>\d+?)d)?((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?((?P<never>never))?')

def to_seconds(time_str):
    parts = regex.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    seconds = 0
    for (name, param) in parts.items():
        if name == "years" and param:
            seconds += int(param) * (365 * 24 * 60 * 60)
        elif name == "weeks" and param:
            seconds += int(param) * (7 * 24 * 60 * 60)
        elif name == "days" and param:
            seconds += int(param) * (24 * 60 * 60)
        elif name == "hours" and param:
            seconds += int(param) * (60 * 60)
        elif name == "minutes" and param:
            seconds += int(param) * (60)
        elif name == "seconds" and param:
            seconds += int(param)
        elif name == "never" and param:
            return(int(630720000))

    return(int(timedelta(seconds=seconds).total_seconds()))

class FilterModule(object):
    ''' Network interface filter '''

    def filters(self):
        return {
            'to_seconds': to_seconds
        }

# def main():
#     test_strings = [
#         '1y27w6d12h5m',
#         '18w5d3h2m',
#         '4d2h5m',
#         '2h10m'
#     ]
#     for item in test_strings:
#         print(f"{item} : {to_seconds(item)}")
#
# if __name__ == '__main__':
#     main()
