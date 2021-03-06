# PCDB Dynamic Inventory for Ansible
## Table of Contents
- [Purpose](#purpose)
- [Description, Design, and Specifications](#description-design-and-specifications)
- [Using pcdb_dynamic_inventory.py with Ansible on the command line](#using-pcdbdynamicinventorypy-with-ansible-on-the-command-line)
	- [Environment Variables Accepted by pcdb_dynamic_inventory.py](#environment-variables-accepted-by-pcdbdynamicinventorypy)
	- [Arguments Accepted by pcdb_dynamic_inventory.py](#arguments-accepted-by-pcdbdynamicinventorypy)
	- [System Requirements](#system-requirements)
	- [Using pcdb_dynamic_inventory.py with the ansible-inventory command](#using-pcdbdynamicinventorypy-with-the-ansible-inventory-command)
	- [Using pcdb_dynamic_inventory.py with the ansible-playbook command](#using-pcdbdynamicinventorypy-with-the-ansible-playbook-command)
- [Configuring for Use with Ansible Tower](#configuring-for-use-with-ansible-tower)
	- [System Requirements](#system-requirements)
	- [Configuring an Ansible Tower Project](#configuring-an-ansible-tower-project)
	- [Configuring an Ansible Tower Credential Type](#configuring-an-ansible-tower-credential-type)
		- [Name](#name)
		- [Description](#description)
		- [Input Configuration](#input-configuration)
		- [Injector Configuration](#injector-configuration)
	- [Configuring an Ansible Tower Credential](#configuring-an-ansible-tower-credential)
	- [Configuring an Ansible Tower Inventory](#configuring-an-ansible-tower-inventory)
		- [Configuring an Ansible Tower Inventory Source](#configuring-an-ansible-tower-inventory-source)
- [Author](#author)

<!-- /TOC -->

## Purpose
To build a consumable inventory from SWIFT's PCDB data.  

## Description, Design, and Specifications
The `pcdb_dynamic_inventory.py` was developed in accordance with Ansible's guide on [developing dynamic inventory sources.](https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html#developing-dynamic-inventory-sources)  

SWIFT stores files in YAML format within a Git repository which is known as the PCDB.  This repository has files for every host and follows a particular naming convention: `[2 letter location code][3 letter application code][remainder of hostname]_runtime.yml`.  

The `pcdb_dynamic_inventory.py` script is capable of obtaining the latest data from a specified Git repository URL and parsing that data into a dynamic inventory for use with Ansible and Ansible Tower.  

The `pcdb_dynamic_inventory.py` generates Ansible inventory groups for locations based off of characters 1 to 2 of each `.yml` file contained in the PCDB Git repository, as well as Ansible inventory groups for applications based off of characters 3 to 5 of each `.yml` file contained in the PCDB Git repository.  The `pcdb_dynamic_inventory.py` script nests each inferred location group in a top-level `Locations` Ansible inventory group, as well as each inferred application group in a top-level `Applications` Ansible inventory group.  

The `pcdb_dynamic_inventory.py` infers each host's hostname as everything prior to `_runtime.yml` or `_runtime.yaml`.  The script will only consume data if the filename ends with `.yml` or `.yaml` and is in the top-level (flat - i.e. not in sub-directories) of the Git repository.  The data stored in each `.yml` or `.yaml` file from the PCDB Git repository will be consumed by the `pcdb_dynamic_inventory.py` script and attached to the appropriate host generated by the dynamic inventory script and stored as Ansible host variables.

The `pcdb_dynamic_inventory.py` script was designed to be reusable as a source for multiple inventories and is configurable with a host filter to limit the scope and size for more refined use-cases.  This can be useful when you only want to allow a Team access to a small subset of available hosts definitons in the PCDB repository.

For the purpose of validating the appropriate settings (Environment Variables) being passed to the script, you can look in the `pcdb_dynamic_inventory.log` file.  The `pcdb_dynamic_inventory.log` will tell you when the last run-time occurred, along with the values from the Environment that the `pcdb_dynamic_inventory.py` received along with some other useful information to assist in debugging.  Password and SSH private key values are never logged to `pcdb_dynamic_inventory.log`, but the path to a SSH private key will be stored in the log when an execution of the script occurs.

## Using pcdb_dynamic_inventory.py with Ansible on the command line
The following sections describe how to use the `pcdb_dynamic_inventory.py` script with Ansible Core/Engine.  

### Environment Variables Accepted by pcdb_dynamic_inventory.py
Each Environment Variable listed in the table below can be set on the Operating System by using the `export` command.  Example: `export PCDB_GIT_URL="https://mygitserver/project.git"` while replacing `https://mygitserver/project.git` with a valid URL to your repository.

| Environment Variable Name | Default Value | Required for Execution | Description |
| --- | :---: | :---: | --- |
|PCDB_GIT_URL|None|Yes|URL to the PCDB Git repository.  If using private SSH key authentication, the URL must begin with `ssh`.  If using username/password authentication, the URL must begin with either `http` or `https`.|
|PCDB_GIT_BRANCH|"master"|No|If desired, a Git repository branch can be specified.  Otherwise the `master` branch of the specified `PCDB_GIT_URL` is used.|
|PCDB_GIT_DIR|"pcdb_data"|No|The directory where a local copy of the `PCDB_GIT_URL` repository will be stored and parsed from.|
|PCDB_GIT_USER|''|No|If using password based authentication to access the `PCDB_GIT_URL` a username is required.  If the repository is publically available, then this is not necessary.|
|PCDB_GIT_PASS|''|No|If using password based authentication to access the `PCDB_GIT_URL` a password is required.  If the repository is publically available, then this is not necessary.|
|PCDB_GIT_SSH_KEY|''|No|When using SSH based authentication to access the `PCDB_GIT_URL` a private key is required for authentication.  This is the fully-qualified path to a SSH private key.  If the repository is publically available, then this is not necessary.|
|PCDB_HOST_FILTER|None|No|This can filter which PCDB Git repository files are parsed by the script.  This is a regular expression that can be specified. Example to obtain only hosts in the US location: `PCDB_HOST_FILTER="^us.*$"`.  Please refer to this [document](https://docs.python.org/2/library/re.html#regular-expression-syntax) for acceptable use of regular expression syntax.  Please note that the Python 'r' character is not required prior to the regular expression, as Environment Variables are read in as raw text from the Operating System.|


### Arguments Accepted by pcdb_dynamic_inventory.py
Please note that at a minimum, the `PCDB_GIT_URL` must be set.

|Argument|Usage|Description|
|---|---|---|
|none|`./pcdb_dynamic_inventory.py`|Returns the `_meta` json object (which is a list of every host in the inventory along with their host specific variables) and all inventory groups and host membership.|
|--list|`./pcdb_dynamic_inventory.py --list`|Returns a json structure of all inventory groups and host membership.|
|--host <hostname>|`./pcdb_dynamic_inventory.py --host myhostname`|Returns a json structure of a specific host's host variables.|

### System Requirements
The system executing the `pcdb_dynamic_inventory.py` must meet the following requirements:
* Python 2.7 or newer
* git 1.7.0 or newer
* gitpython python library
* pyyaml python library

First ensure that you have the `python-pip` package installed, run: `yum install -y python-pip`.

To install the `gitpython` Python library, run: `pip install gitpython`.
To install the `pyyaml` Python library, run: `pip install pyyaml`.

For Ansible Tower, you must install these packages into the Ansible Tower [virtual environment](https://docs.ansible.com/ansible-tower/latest/html/upgrade-migration-guide/virtualenv.html).

### Using pcdb_dynamic_inventory.py with the ansible-inventory command
To view a visual representation of the inventory generated by the `pcdb_dynamic_inventory.py` script the following command can be run: `ansible-inventory -i ./pcdb_dynamic_inventory.py --graph`.  

### Using pcdb_dynamic_inventory.py with the ansible-playbook command
To use `pcdb_dynamic_inventory.py` with the `ansible-playbook` command, you can run the following: `ansible-playbook myplaybook.yml -i /path/to/pcdb_dynamic_inventory.py`, while replacing `myplaybook.yml` with a valid Ansible playbook filename and `/path/to/pcdb_dynamic_inventory.py` with the valid path to the `pcdb_dynamic_inventory.py` script.

Alternatively you could modify your `ansible.cfg` `[defaults]` `inventory` setting to point to the path of the `pcdb_dynamic_inventory.py` script.

## Configuring for Use with Ansible Tower
The following sections describe how to configure your environment to use the `pcdb_dynamic_inventory.py` script as a dynamic inventory source in Ansible Tower.  

### System Requirements
The Python libraries `gitpython` and `pyyaml` must be installed into Ansible Tower's [virtual environment](https://docs.ansible.com/ansible-tower/latest/html/upgrade-migration-guide/virtualenv.html) for the `pcdb_dynamic_inventory.py` script to function:
```
source /var/lib/awx/venv/ansible/bin/activate
umask 0022
pip install gitpython
pip install pyyaml #should already come with Ansible
deactivate
```

### Configuring an Ansible Tower Project
The `pcdb_dynamic_inventory.py` and `git_ssh_command.sh` at minimum should be stored in a Git repository.  It is recommended to store this `README.md` within the repository for reference.  Ansible Tower should be configured to be able to obtain those files for use in inventory sources by [creating an Ansible Tower project](https://docs.ansible.com/ansible-tower/3.2.5/html/userguide/projects.html#add-a-new-project).  

An Ansible Tower project requires a "Source Control" Credential to access a Git repository, therefore a Credential should be created first.  Please refer to the Ansible Tower documentation on creating a new [Credential](https://docs.ansible.com/ansible-tower/3.2.5/html/userguide/credentials.html#add-a-new-credential).

Choose type "Source Control" when creating your new "Source Control" credential, enter the appropriate information for accessing the Git repository storing the script code, and click "Save".

Now a new [Ansible Tower Project](https://docs.ansible.com/ansible-tower/3.2.5/html/userguide/projects.html#add-a-new-project) can be created.

### Configuring an Ansible Tower Credential Type
In order to access the PCDB Git repository securley, a custom Credential Type will need to be defined in Ansible Tower.  The settings that get defined will securely inject any password or SSH private key into the Environment Variables of `pcdb_dynamic_inventory.py`.  

Please refer to the Ansible Tower documentation on [Credential Types](https://docs.ansible.com/ansible-tower/3.2.5/html/userguide/credential_types.html#getting-started-with-credential-types) and fill in the fields of the new Credential Type with the following settings:

#### Name
```
PCDB Inventory
```
#### Description
```
Credentials to access SWIFT PCDB Git repository
```
#### Input Configuration
```yaml
fields:
  - type: "string"
    id: "git_username"
    label: "PCDB Git Username"
    help_text: "Username for the Git user allowed to access the PCDB repository - Required if PCDB Git Password is set.  Do not set this if you are using an SSH key."
  - type: "string"
    id: "git_password"
    label: "PCDB Git Password"
    secret: True
    help_text: "Password for the Git user allowed to access the PCDB repository - Required if PCDB Git Username is set.  Do not set this if you are using an SSH key."
  - type: "string"
    id: "git_ssh_private_key"
    label: "PCDB Git SSH Private Key"
    secret: True
    multiline: True
    format: "ssh_private_key"
    help_text: "SSH private key for the Git user allowed to access the PCDB repository.  Do not set this if you are using a username and password pair."
```
#### Injector Configuration
```yaml
env:
  PCDB_GIT_PASS: "{{ git_password }}"
  PCDB_GIT_SSH_KEY:
    "{% if git_ssh_private_key is defined and git_ssh_private_key != '' %}{{ tower.filename }}{{ endif }}"
  PCDB_GIT_USER: "{{ git_username }}"
file:
  template: "{{ git_ssh_private_key }}"
```

### Configuring an Ansible Tower Credential
Once you have created the "PCDB Inventory" Credential Type, a new Credential can be created for use with the `pcdb_dynamic_inventory.py` script.

Please refer to the Ansible Tower documentation on creating a new [Credential](https://docs.ansible.com/ansible-tower/3.2.5/html/userguide/credentials.html#add-a-new-credential).

Choose the type "PCDB Inventory" when creating your new credential for use with the `pcdb_dynamic_inventory.py`.  

If you are using password based authentication, the "PCDB Git Username" and "PCDB Git Password" fields should be filled in and the "PCDB Git SSH Private Key" field should be left blank.  Click "Save".

If you are using SSH based git authentication, the "PCDB Git Username" and "PCDB Git Password" fields should be left blank, and the "PCDB Git SSH Private Key" field should be populated with the contents of your SSH Private Key file that has access to the PCDB Git repository.  Click "Save".

### Configuring an Ansible Tower Inventory
[Create a new Inventory](https://docs.ansible.com/ansible-tower/3.2.5/html/userguide/inventories.html#add-a-new-inventory) in Ansible Tower.

Provide a name and description for the inventory, and click "Save".

#### Configuring an Ansible Tower Inventory Source
On the inventory you created in the previous step, click on the "Sources" button.  You may refer to the guide on [Inventory Sources](https://docs.ansible.com/ansible-tower/3.2.5/html/administration/scm-inv-source.html#custom-dynamic-inventory-scripts).

* Provide a "name" and a "description" for the inventory source.  
* Choose type "Sourced from a project".  
* Choose the "PCDB Inventory" credential you created.  
* Choose the Project that is connected to the Git repository where the `pcdb_dynamic_inventory.py` script is stored.  
* Choose the `pcdb_dynamic_inventory.py` from the "inventory file" drop down.
* Check "Overwrite" and "Update on Launch" from the "Update Options".
* Click "Save".

You can now click the "Sync All" button or the "Sync" icon to generate the inventory off of the current PCDB data.

Due to the "Update on Launch" setting, anytime an Ansible Tower Job Template is launched, the inventory script will run and update the inventory in Ansible Tower.  The script is only designed to pull new content from the PCDB Git repository if the local branch's commit hash differs from the remote copy.

## Author
[Andrew J. Huffman](ahuffman@redhat.com)
