# (c) 2017, David Sastre Medina <d.sastre.medina@gmail.com>
#
# This file is part of Ansible
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

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError, AnsibleFilterError

import os


def basename(path):
    ''' Given a path, return its `basename(1)`
    '''
    if path is None:
        raise AnsibleError('Path not found')
    return os.path.basename(path)


class FilterModule(object):
    ''' Query filter '''

    def filters(self):
        return {
            'basename': basename
        }
