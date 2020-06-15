#!/usr/bin/env python
"""
PCDB Dynamic Inventory for Ansible
==================================

Author: Andrew J. Huffman: ahuffman@redhat.com

Requirements:
  python 2.7 or newer
  git 1.7.0 or newer
  gitpython python library
  pyyaml python library


Script accepts the following environment variables:
  PCDB_GIT_URL - (required) - git URL for PCDB data
  PCDB_GIT_BRANCH - (optional) - defaults to "master"
  PCDB_GIT_DIR - (optional) - defaults to "[current working directory]/pcdb_data" - where to store git repo relative to the current working directory
  PCDB_GIT_USER - (optional) - if passed, a PCDB_GIT_PASS must also be provided
  PCDB_GIT_PASS - (optional) - if passed, a PCDB_GIT_USER must also be provided
  PCDB_GIT_SSH_KEY - (optional) - path to a SSH private key - if passed, PCDB_GIT_USER and PCDB_GIT_PASS will be ignored
  PCDB_HOST_FILTER - (optional) - defaults to None - Regex to refine hosts in an inventory
"""

#for reading in files/open files, get environment vars
from os import getcwd, getenv, listdir
#for ensuring we have only .yml or .yaml files,
#  making sure we're not listing directories, and joining paths from strings
from os.path import splitext,isfile,join
import argparse #to accept command line arguments
import datetime #for logging
import json #for formatting inventory
import yaml #pip install pyyaml(comes with Ansible) - for reading yaml vars out of PCDB files
import git #for pulling down git repo that stores PCDB - pip install gitpython
import re #for regular expression support - used for host filtering and grouping of hosts

class PCDBInventory(object):
    def __init__(self):
        #initialize log for run
        self.run_date = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
        self.dir = getcwd() #capture current working directory path
        self.write_log('\n' * 2 + 'PCDB Dynamic Inventory ran at ' + self.run_date + ':\n')
        self.inventory = dict() #initialize empty inventory dictionary
        self.hosts = dict() #initialize empty hosts dictionary
        self.groups = dict() #initialize empty groups dictionary
        self.parse_env_vars() #reads in environment variables
        self.parse_cli_args() #captures/processes user command line arguments
        self.ssh_command = None #initialize empty ssh command for Git environment usage
        self.output = "" #stores final formatted inventory output - initialize empty output

        #Validate git url if PCDB_GIT_SSH_KEY is provided
        if self.git_ssh_key != '' and self.git_url.split(':')[0] != "ssh":
            #invalid git URL protocol to use with SSH key
            print('PCDB_GIT_URL does not begin with "ssh"')
            self.write_log('PCDB_SSH_KEY provided, but PCDB_GIT_URL does not begin with "ssh"\n')
            exit(1)
        elif self.git_ssh_key != '' and self.git_url.split(':')[0] == "ssh":
            self.ssh_command = join(self.dir, 'git_ssh_command.sh')
        else:
            self.write_log('PCDB_GIT_SSH_KEY not provided')

        #get git content to parse for dynamic inventory
        self.get_pcdb_repo()

        #Based on aruments provided
        if self.args.host:
            #--host <host> argument passed
            self.output = self.get_host()
        elif self.args.list:
            #--list argument passed
            self.get_hosts()
            for group in self.groups:
                self.inventory[group] = self.groups[group]
            self.output = self.json_format_dict(self.inventory)
        else:
            #no argument passed
            self.get_hosts()
            self.inventory['_meta'] = {'hostvars': {}}
            for hostname in self.hosts:
                self.inventory['_meta']['hostvars'][hostname] = self.hosts[hostname]
            for group in self.groups:
                self.inventory[group] = self.groups[group]
            self.output = self.json_format_dict(self.inventory)
        print(self.output)

    # Capture command line arguments: --list and --host <host>
    def parse_cli_args(self):
        parser =  argparse.ArgumentParser(description='Produce an Ansible dynamic inventory from SWIFT PCDB')
        parser.add_argument('--list', action='store_true', help='List all available hosts from PCDB')
        parser.add_argument('--host', action='store', help='Get variables for a specific host from PCDB')
        self.args = parser.parse_args()

    # Capture environment variables for script execution
    def parse_env_vars(self):
        self.git_url = getenv('PCDB_GIT_URL', None)
        self.git_branch = getenv('PCDB_GIT_BRANCH', 'master')
        self.git_user = getenv('PCDB_GIT_USER', '')
        self.git_pass = getenv('PCDB_GIT_PASS', '')
        self.git_ssh_key = getenv('PCDB_GIT_SSH_KEY', '')
        self.pcdb_dir = getenv('PCDB_GIT_DIR', 'pcdb_data')
        self.host_filter = getenv('PCDB_HOST_FILTER', None)
        if self.git_url == None or self.git_url == "":
            print("PCDB_GIT_URL environment variable not provided.")
            self.write_log("PCDB_GIT_URL environment variable not provided")
            exit(1)
        if (self.git_user != "" and self.git_pass == "") or (self.git_user == "" and self.git_pass != ""):
            print("Both a PCDB_GIT_USER and PCDB_GIT_PASS must be provided if using password based authentication.")
            self.write_log("Both a PCDB_GIT_USER and PCDB_GIT_PASS must be provided if using password based authentication.")
            exit(1)
        #Output parsed environment variables to log (but no password)
        self.write_log('Parsed Environment Variables:\n' + \
                        'git_url: ' + str(self.git_url) + '\n' + \
                        'git_branch: ' + self.git_branch + '\n' + \
                        'git_user: ' + self.git_user + '\n' + \
                        'git_ssh_key: ' + self.git_ssh_key + \
                        '\n' + 'git_dir: ' + self.pcdb_dir + \
                        '\n' + 'host_filter: ' + \
                        str(self.host_filter) + '\n')

    def write_log(self, data):
        logfile = open(join(self.dir, 'pcdb_dynamic_inventory.log'), 'a')
        logfile.write(data)
        logfile.close

    def get_pcdb_repo(self):
        self.pcdb_data = join(self.dir, self.pcdb_dir)
        self.pcdb_git_dir = git.Repo.init(self.pcdb_data)
        self.pcdb_remotes = self.pcdb_git_dir.remotes
        #Test for existing configured remotes
        if not self.pcdb_git_dir.remotes:
            #Check for git user and pass and update URL
            if self.git_user != "" and self.git_pass != "":
                self.git_url_split = self.git_url.split('//')
                self.pw_git_url = self.git_url_split[0] + '//' + self.git_user + ':' + self.git_pass + '@' + self.git_url_split[1]
                self.pcdb_origin = self.pcdb_git_dir.create_remote('origin', self.pw_git_url)
            else:
                self.pcdb_origin = self.pcdb_git_dir.create_remote('origin', self.git_url)
        else:
            for remote in self.pcdb_remotes:
                if "origin" == str(remote):
                    #Check for git user and pass and update URL
                    if self.git_user != "" and self.git_pass != "":
                        self.git_url_split = self.git_url.split('//')
                        self.pw_git_url = self.git_url_split[0] + '//' + self.git_user + ':' + self.git_pass + '@' + self.git_url_split[1]
                        self.pcdb_origin = self.pcdb_git_dir.remotes.origin.set_url(self.pw_git_url)
                    else:
                        #ensure existing origin URL set to PCDB_GIT_URL
                        self.pcdb_origin = self.pcdb_git_dir.remotes.origin.set_url(self.git_url)
        if self.ssh_command is None:
            self.pcdb_origin.fetch()
        else:
            #we have an SSH key to use
            self.write_log('git_ssh_command: ' + self.ssh_command + '\n')
            with self.pcdb_git_dir.git.custom_environment(GIT_SSH=self.ssh_command):
                self.pcdb_origin.fetch()
        #Test for existing HEADs
        if not self.pcdb_git_dir.heads:
            #Setup head to match remote branch
            self.pcdb_git_dir.create_head(self.git_branch, self.pcdb_origin.refs[self.git_branch])
        else:
            if self.git_branch not in self.pcdb_git_dir.heads:
                self.pcdb_git_dir.create_head(self.git_branch, self.pcdb_origin.refs[self.git_branch])

        #Ensure we set local tracking branch to the remote copy of the branch
        self.pcdb_git_dir.heads[self.git_branch].set_tracking_branch(self.pcdb_origin.refs[self.git_branch])

        #Ensure no local changes are kept around compared to remote copy of branch
        self.pcdb_git_dir.heads[self.git_branch].checkout()
        self.pcdb_git_dir.git.reset('--hard')
        self.pcdb_git_dir.git.clean('-xdf')

        #Check for local and remote matching commit - *only if not, then pull latest commit
        if self.pcdb_git_dir.commit(self.git_branch) != self.pcdb_origin.refs[self.git_branch].commit:
            if self.ssh_command is None:
                self.pcdb_origin.pull(self.git_branch)
            else:
                #we have an SSH key to use
                print(self.ssh_command)
                with self.pcdb_git_dir.git.custom_environment(GIT_SSH=self.ssh_command):
                    self.pcdb_origin.pull(self.git_branch)

        #for security, scrub user:pass from git config
        if self.git_user != "" and self.git_pass != "":
            self.git_url_split = self.git_url.split('//')
            self.pcdb_origin = self.pcdb_git_dir.remotes.origin.set_url(self.git_url)

    # --host <host> command line argument passed
    def get_host(self):
        self.get_hosts()
        if self.args.host not in self.hosts:
            #error handling for a host that doesn't exist
            print self.args.host, "does not exist in the source, or has been filtered out of the inventory."
            exit(1)
        else:
            return self.json_format_dict(self.hosts[self.args.host], True)


    # --list or no argument passed (--host runs this as well to obtain invdividual host data)
    def get_hosts(self):
        #setup top level grouping
        self.groups['all'] = {'children': ['ungrouped', 'Applications', 'Locations']}
        self.groups['Applications'] = {'children': [], 'hosts': [], 'vars': {}}
        self.groups['Locations'] = {'children': [], 'hosts': [], 'vars': {}}
        self.groups['ungrouped'] = {'hosts': []}

        #Get filelist from current working directory to build inventory:
        self.pcdb_files = [filename for filename in listdir(self.pcdb_data) if isfile(join(self.pcdb_data, filename))]
        #filter file list
        if self.host_filter is not None:
            #Build clean list of files that match filter
            self.pcdb_files_final = [fn for fn in self.pcdb_files if re.search(self.host_filter, fn, re.I)]
        else:
            self.pcdb_files_final = self.pcdb_files

        #Process the PCDB data
        for filename in self.pcdb_files_final:
            if (splitext(filename)[1] == '.yml') or (splitext(filename)[1] == '.yaml'): # make sure we only have yaml files
                self.host = filename.split('_')[0] #cut off everything after the character '_' (i.e. drop '_runtime.yml')
                self.pcdb_file = file(self.dir + '/' + self.pcdb_dir + '/' + filename, 'r')
                self.pcdb_yaml_data = yaml.load(self.pcdb_file)

                #Build inventory structure for host
                self.hosts[self.host] = {'pcdb_hostname': self.host}
                self.hosts[self.host].update(self.pcdb_yaml_data)

                #Host Grouping
                self.inv_groups = re.search(r'^(.{2})(.{3}).*$', self.host, re.I)
                #Location Grouping
                if self.inv_groups.group(1).upper() not in self.groups['Locations']['children']:
                    #Location group does not exist, add location to "Locations"
                    #  group and then add host to the specific location
                    self.groups['Locations']['children'].append(self.inv_groups.group(1).upper())
                    self.groups[self.inv_groups.group(1).upper()] = {'hosts': [self.host], 'vars': {}, 'children': []}
                else:
                    #Location exists, add host to location group
                    self.groups[self.inv_groups.group(1).upper()]['hosts'].append(self.host)
                #Application Grouping
                if self.inv_groups.group(2).upper() not in self.groups['Applications']['children']:
                    #Application group does not exist, add application to "Applications"
                    #  group and then add host the specific applicaiton
                    self.groups['Applications']['children'].append(self.inv_groups.group(2).upper())
                    self.groups[self.inv_groups.group(2).upper()] = {'hosts': [self.host], 'vars': {}, 'children': []}
                else:
                    #Application exists, add host to application group
                    self.groups[self.inv_groups.group(2).upper()]['hosts'].append(self.host)

    # Formats inventory data into Ansible consumable json format
    def json_format_dict(self, data, pretty=True):
        if pretty:
            return json.dumps(data, sort_keys=False, indent=2)
        else:
            return json.dumps(data)

#Build the inventory:
PCDBInventory()
