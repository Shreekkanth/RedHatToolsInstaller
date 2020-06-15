#!/usr/bin/env python

# Copyright 2017 Reuben Stump, Alex Mittell

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing
# permissions and limitations under the License.
'''
ServiceNow Inventory Script
=======================
Retrieve information about machines from a ServiceNow CMDB
This script will attempt to read configuration from an INI file with the same
base filename if present, or `now.ini` if not.  It is possible to create
symlinks to the inventory script to support multiple configurations, e.g.:
* `now.py` (this script)
* `now.ini` (default configuration, will be read by `now.py`)
The path to an INI file may also be specified via the `NOW_INI` environment
variable, in which case the filename matching rules above will not apply.
Host and authentication parameters may be specified via the `SN_INSTANCE`,
`SN_USERNAME` and `SN_PASSWORD` environment variables; these options will
take precedence over options present in the INI file.  An INI file is not
required if these options are specified using environment variables.

For additional usage details see: https://github.com/ServiceNowITOM/ansible-sn-inventory
'''

import os
import sys
import requests
import base64
import json
import re
import configparser
import time
import ldap

from cookielib import LWPCookieJar


class NowInventory(object):
    def __init__(
            self,
            hostname,
            username,
            password,
            fields=None,
            groups=None,
            selection=None,
            proxy=None):
        self.hostname = hostname

        # requests session
        self.session = requests.Session()

        self.auth = requests.auth.HTTPBasicAuth(username, password)
        # request headers
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        # request cookies
        self.cookies = LWPCookieJar(os.getenv("HOME") + "/.sn_api_session")
        try:
            self.cookies.load(ignore_discard=True)
        except IOError:
            pass
        self.session.cookies = self.cookies

        if fields is None:
            fields = []

        if groups is None:
            groups = []

        if selection is None:
            selection = []

        if proxy is None:
            proxy = []

        # extra fields (table columns)
        self.fields = fields

        # extra groups (table columns)
        self.groups = groups

        # selection order
        self.selection = selection

        # proxy settings
        self.proxy = proxy

        # initialize inventory
        self.inventory = {'_meta': {'hostvars': {}}}

        return

    def _put_cache(self, name, value):
        cache_dir = os.environ.get('SN_CACHE_DIR')
        if not cache_dir and config.has_option('defaults', 'cache_dir'):
            cache_dir = os.path.expanduser(config.get('defaults', 'cache_dir'))
        if cache_dir:
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)
            cache_file = os.path.join(cache_dir, name)
            with open(cache_file, 'w') as cache:
                json.dump(value, cache)

    def _get_cache(self, name, default=None):
        cache_dir = os.environ.get('SN_CACHE_DIR')
        if not cache_dir and config.has_option('defaults', 'cache_dir'):
            cache_dir = config.get('defaults', 'cache_dir')
        if cache_dir:
            cache_file = os.path.join(cache_dir, name)
            if os.path.exists(cache_file):
                cache_max_age = os.environ.get('SN_CACHE_MAX_AGE')
                if not cache_max_age:
                    if config.has_option('defaults', 'cache_max_age'):
                        cache_max_age = config.getint('defaults',
                                                      'cache_max_age')
                    else:
                        cache_max_age = 0
                cache_stat = os.stat(cache_file)
                if (cache_stat.st_mtime + int(cache_max_age)) >= time.time():
                    with open(cache_file) as cache:
                        return json.load(cache)
        return default

    def __del__(self):
        self.cookies.save(ignore_discard=True)

    def _invoke(self, verb, path, data):

        cache_name = '__snow_inventory__'
        inventory = self._get_cache(cache_name, None)
        if inventory is not None:
            return inventory

        # build url
        url = "https://%s/%s" % (self.hostname, path)

        # perform REST operation
        response = self.session.get(
            url, auth=self.auth, headers=self.headers, proxies={
                'http': self.proxy, 'https': self.proxy})
        if response.status_code != 200:
            print >> sys.stderr, "http error (%s): %s" % (response.status_code,
                                                          response.text)

        self._put_cache(cache_name, response.json())
        return response.json()

    def add_group(self, target, group, groupvar=None):
        ''' Transform group names:
                        1. lower()
                        2. non-alphanumerical characters to '_'
        '''

        # Ignore empty group names
        if group == '' or group is None:
            return

        group = group.lower()
        group = re.sub(r' ', '', group)

        self.inventory.setdefault(group, {'hosts': []})
        self.inventory[group]['hosts'].append(target)

        if groupvar:
            self.inventory[group]['vars'] = groupvar 
        return

    def add_var(self, target, key, val):
        if target not in self.inventory['_meta']['hostvars']:
            self.inventory['_meta']['hostvars'][target] = {}

        self.inventory['_meta']['hostvars'][target]["sn_" + key] = val
        return

    def ldap_search(self, nisMapName, domain):
        l = ldap.initialize("ldap://unixldap.gap.chevron.net")
        basedn = "nisMapName=" + nisMapName + ",dc=" + domain + ",dc=sr"
        searchFilter = "(cn=*)"
        searchAttribute = ["cn", "nisMapEntry"]
        #this will scope the entire subtree under UserUnits
        searchScope = ldap.SCOPE_SUBTREE

        try:
            l.protocol_version = ldap.VERSION3
        except ldap.INVALID_CREDENTIALS:
            sys.exit(0)
        except ldap.LDAPError, e:
            if type(e.message) == dict and e.message.has_key('desc'):
                print e.message['desc']
            else:
                print e
            sys.exit(0)

        result = l.search_s(basedn, searchScope, searchFilter, searchAttribute)

        erp_hosts = {}
        ah_hosts = {}
        
        for dn,ldap_entry in result:
            server_shortname = ldap_entry['cn'][0].split('.')[0]

            if domain == "afis":
                server_filter = re.compile('^\d|\*|localhost|gdc0n|gdc0p')
                nisMapName_filter = re.compile('-ah')
                env_filter = re.compile('gmlp|hl|cp')
                sap_filter = re.compile('sap')
                jde_filter = re.compile('jd')
                ari_filter = re.compile('ari')
                inf_filter = re.compile('uxe|inf|cde|afis|vnc')
                dmz_filter = re.compile('dmz')

                # print ldap_entry['nisMapEntry']
                if not re.match(server_filter, server_shortname) and not re.search(nisMapName_filter, ldap_entry['nisMapEntry'][0]):
                    erp_hosts[server_shortname] = []
                    erp_hosts[server_shortname].append('erp')

                    if re.match(env_filter, server_shortname):
                        erp_hosts[server_shortname].append('erp-prd')
                    else:
                        erp_hosts[server_shortname].append('erp-dev')

                    if re.search(sap_filter, server_shortname):
                        erp_hosts[server_shortname].append('sap')
                    elif re.search(jde_filter, server_shortname):
                        erp_hosts[server_shortname].append('jde')
                    elif re.search(ari_filter, server_shortname):
                        erp_hosts[server_shortname].append('ari')
                    elif re.search(inf_filter, server_shortname):
                        erp_hosts[server_shortname].append('inf') 
                    else:
                        erp_hosts[server_shortname].append('misc')

                    if re.search(dmz_filter, ldap_entry['nisMapEntry'][0]):
                        erp_hosts[server_shortname].append('erp-dmz')
                
                ldap_result = erp_hosts

            elif domain == "bayarea":
                ah_tst_filter = re.compile("tst", re.IGNORECASE)
                ah_dev_filter = re.compile("dev", re.IGNORECASE)
                ah_prd_filter = re.compile("prd", re.IGNORECASE)
                ah_dmz_filter = re.compile("dmz", re.IGNORECASE)
                ah_pci_filter = re.compile("pci", re.IGNORECASE)

                env = ldap_entry['nisMapEntry'][0].split()[1]

                ah_hosts[server_shortname] = []
                ah_hosts[server_shortname].append('ah')
                
                if re.match(ah_tst_filter, env):
                    ah_hosts[server_shortname].append('ah-tst')
                    # print "ah-tst " + server_shortname
                elif re.match(ah_dev_filter, env):
                    ah_hosts[server_shortname].append('ah-dev')
                    # print "ah-dev " + server_shortname
                elif re.match(ah_prd_filter, env):
                    ah_hosts[server_shortname].append('ah-prd')
                
                if re.search(ah_dmz_filter, ldap_entry['nisMapEntry'][0]):
                    ah_hosts[server_shortname].append('ah-dmz')

                if re.search(ah_pci_filter, ldap_entry['nisMapEntry'][0]):
                    ah_hosts[server_shortname].append('ah-pci')

                ldap_result = ah_hosts
        
        return ldap_result

    def generate(self):

        table_server = 'cmdb_ci_server'
        table_app = 'cmdb_ci_appl'
        table_rel = 'cmdb_rel_ci'
        base_fields = [
            u'name', u'host_name', u'fqdn', u'ip_address', u'sys_class_name'
        ]
        base_groups = [u'sys_class_name']
        options_server = "?sysparm_exclude_reference_link=true&sysparm_display_value=true"
        options_app = "?sysparm_display_value=true"
        options_rel = "?sysparm_exclude_reference_link=true&type=60bc4e22c0a8010e01f074cbe6bd73c3"

        columns_server = list(
            set(base_fields + base_groups + self.fields + self.groups))
        columns_app = ['name', 'u_inscopeforsox', 'sys_id']
        columns_rel = ['parent', 'child']

        path_server = '/api/now/table/' + table_server + options_server + \
            "&sysparm_fields=" + ','.join(columns_server)
        path_app = '/api/now/table/' + table_app + options_app + \
            "&sysparm_fields=" + ','.join(columns_app)
        path_rel = '/api/now/table/' + table_rel + options_rel + \
            "&sysparm_fields=" + ','.join(columns_rel)

        # Default, mandatory group 'sys_class_name'
        groups = list(set(base_groups + self.groups))
        content_server = self._invoke('GET', path_server, None)
        content_app = self._invoke('GET', path_app, None)
        content_rel = self._invoke('GET', path_rel, None)

        app_records = {}
        rel_records = {}
        app_records = content_app['result']
        rel_records = content_rel['result']

        ah_ldap_result = self.ldap_search("hosttype","bayarea")
        erp_ldap_result = self.ldap_search("netgroup.byhost","afis")

        all_ldap_result = dict(ah_ldap_result, **erp_ldap_result)

        app_rec = {}
        for a_record in app_records:
            #print ("this is record: %s", a_record['name'])
            app_name = a_record['name']
            app_sox = a_record['u_inscopeforsox']
            app_sysid = a_record['sys_id']
            app_rec[app_sysid] = {}
            app_rec[app_sysid]['name'] = app_name
            app_rec[app_sysid]['u_inscopeforsox'] = app_sox

        host_app = {}
        for r_record in rel_records:
            if r_record['child'] == '':
                continue
            if r_record['parent'] == '':
                continue
            try:
                if host_app[r_record['child']] == False:
                    pass
            except KeyError:
                host_app[r_record['child']] = { "name": [], "sox": 'false'}

            host_app[r_record['child']]['name'].append(app_rec[r_record['parent']]['name'])

            # print app_rec[r_record['parent']]
            
            try:
                if host_app[r_record['child']]['sox'] == False:
                    pass
            except KeyError:
                host_app[r_record['child']]['sox'] = 'false'

            if app_rec[r_record['parent']]['u_inscopeforsox'] == 'true':
                host_app[r_record['child']]['sox'] = 'true'

        for server_record in content_server['result']:
            ''' Ansible host target selection order:
                        1. ip_address
                        2. fqdn
                        3. host_name

                        '''
            
            target = None

            selection = self.selection

            if not selection:
                selection = ['fqdn', 'host_name', 'ip_address']
            for k in selection:
                #print ("This is k %s", k)
                if server_record[k] != '':
                    target = server_record[k].lower()
                    #print ("This is target %s", target)
           
            # Skip if no target available
            if target is None:
                continue

            # Only show values with NOW_SUPPORT_GROUP env
            if os.environ.get('NOW_SUPPORT_GROUP'):
                if server_record['support_group'] not in os.environ.get('NOW_SUPPORT_GROUP').split(':'):
                    continue

            # Only show values with NOW_OS env
            if os.environ.get('NOW_OS'):
                linux_filter = re.compile('CENT|HP-UX|LINUX|RED HAT|RHEL|SOLARIS|SUSE', re.IGNORECASE)
                win_filter = re.compile('W2K|WINDOWS', re.IGNORECASE)

                if os.environ.get('NOW_OS') == 'Linux':
                    now_os_filter = linux_filter
                elif os.environ.get('NOW_OS') == 'Windows':
                    now_os_filter = win_filter
                else:
                    now_os_filter = ''

                if server_record['os'] and not re.search(now_os_filter, server_record['os']):
                    continue

            # hostvars
            for k in server_record.keys():
                if k == 'sys_id':
                    try:
                        if host_app[server_record[k]] != False:
                            self.add_var(target, 'hosted_apps', host_app[server_record[k]]['name'])    
                            self.add_var(target, 'inscopeforsox', host_app[server_record[k]]['sox'])    
                    except KeyError:
                        self.add_var(target, 'hosted_apps', [])    
                        self.add_var(target, 'inscopeforsox', 'false')    

                else:
                    self.add_var(target, k, server_record[k])

            # groups
            ldap_target = target.split('.')[0]
            for k in groups:
                k = k.lower()
                try:
                    if k == 'virtual' and server_record[k] == 'true':
                        self.add_group(target, k)
                    elif k == 'virtual' and server_record[k] == 'false':
                        self.add_group(target, 'physical')
                    elif k == 'erp' and k in all_ldap_result[ldap_target]:
                        gv = {'cvx_linux_domain' : k}
                        self.add_group(target, k, groupvar=gv)
                    elif k == 'erp-dev' and k in all_ldap_result[ldap_target]:
                        gv = {'cvx_linux_env' : k}
                        self.add_group(target, k, groupvar=gv)
                    elif k == 'erp-prd' and k in all_ldap_result[ldap_target]:
                        gv = {'cvx_linux_env' : k}
                        self.add_group(target, k, groupvar=gv)
                    elif k == 'erp-dmz' and k in all_ldap_result[ldap_target]:
                        self.add_group(target, k)
                    elif k == 'sap' and k in all_ldap_result[ldap_target]:
                        self.add_group(target, k)
                    elif k == 'ariba' and k in all_ldap_result[ldap_target]:
                        self.add_group(target, k)
                    elif k == 'jde' and k in all_ldap_result[ldap_target]:
                        self.add_group(target, k)
                    elif k == 'inf' and k in all_ldap_result[ldap_target]:
                        self.add_group(target, k)
                    elif k == 'ah' and k in all_ldap_result[ldap_target]:
                        gv = {'cvx_linux_domain' : k}
                        self.add_group(target, k, groupvar=gv)
                    elif k == 'ah-tst' and k in all_ldap_result[ldap_target]:
                        gv = {'cvx_linux_env' : k}
                        self.add_group(target, k, groupvar=gv)
                    elif k == 'ah-dev' and k in all_ldap_result[ldap_target]:
                        gv = {'cvx_linux_env' : k}
                        self.add_group(target, k, groupvar=gv)
                    elif k == 'ah-prd' and k in all_ldap_result[ldap_target]:
                        gv = {'cvx_linux_env' : k}
                        self.add_group(target, k, groupvar=gv)
                    elif k == 'ah-pci' and k in all_ldap_result[ldap_target]:
                        self.add_group(target, k)
                    elif k == 'ah-dmz' and k in all_ldap_result[ldap_target]:
                        self.add_group(target, k)
                    else:
                        self.add_group(target, server_record[k])

                except KeyError as e:
                    pass

        return

    def json(self):
        return json.dumps(self.inventory, sort_keys=True, indent=4)


def main(args):

    global config
    config = configparser.SafeConfigParser()

    if os.environ.get('NOW_ENV', ''):
        os.environ['NOW_INI'] = 'environment/' + os.environ['NOW_ENV'] + '/now.ini'
   
    if os.environ.get('NOW_INI', ''):
        config_files = [os.environ['NOW_INI']]
    else:
        config_files = [
            os.path.abspath(sys.argv[0]).rstrip('.py') + '.ini', 'now.ini'
        ]

    for config_file in config_files:
        if os.path.exists(config_file):
            config.read(config_file)
            break

    # Read authentication information from environment variables (if set),
    # otherwise from INI file.
    instance = os.environ.get('SN_INSTANCE')
    if not instance and config.has_option('auth', 'instance'):
        instance = config.get('auth', 'instance')

    username = os.environ.get('SN_USERNAME')
    if not username and config.has_option('auth', 'user'):
        username = config.get('auth', 'user')

    password = os.environ.get('SN_PASSWORD')
    if not password and config.has_option('auth', 'password'):
        password = config.get('auth', 'password')

    # SN_SEL_ORDER
    selection = os.environ.get("SN_SEL_ORDER", [])

    if not selection and config.has_option('config', 'selection_order'):
        selection = config.get('config', 'selection_order')
        selection = selection.encode('utf-8').replace('\n', '\n\t')
    if isinstance(selection, str):
        selection = selection.split(',')

    # SN_GROUPS
    groups = os.environ.get("SN_GROUPS", [])

    if not groups and config.has_option('config', 'groups'):
        groups = config.get('config', 'groups')
        groups = groups.encode('utf-8').replace('\n', '\n\t')
    if isinstance(groups, str):
        groups = groups.split(',')

    # SN_FIELDS
    fields = os.environ.get("SN_FIELDS", [])

    if not fields and config.has_option('config', 'fields'):
        fields = config.get('config', 'fields')
        fields = fields.encode('utf-8').replace('\n', '\n\t')
    if isinstance(fields, str):
        fields = fields.split(',')

    # SN_PROXY
    proxy = os.environ.get('SN_PROXY')
    if not proxy and config.has_option('config', 'proxy'):
        proxy = config.get('config', 'proxy')

    inventory = NowInventory(
        hostname=instance,
        username=username,
        password=password,
        fields=fields,
        groups=groups,
        selection=selection,
        proxy=proxy)
    inventory.generate()
    print(inventory.json())

if __name__ == "__main__":
    main(sys.argv)
