To build Ansible Tower you must use Ubuntu as the Tower server, VM or otherwise, as it uses the apt module to download and update packages.

Run assemble.sh to remove the NTC modules as they conflict with the native Ansible linux gather facts

Unlike other Starbucks playbooks, Tower Deploy uses an inventory consisting of only the server(s) to which Ansible Tower will be deployed. You will need to update inventory.txt to point to your server(s) (recommended size is 2 CPUs and 8GB memory).

The ANSIBLE_TOWER_VERSION must be set due to the version being named in in the path for the Tower installation files, and will need to be updated as the version changes.

Vars needed:

export ANSIBLE_LX_USERNAME='m-Account'
export ANSIBLE_LX_PASSWORD='m-Password'
export ANSIBLE_TOWER_VERSION="3.2.2"

# tower_deploy
