# Environments

## Hosting
Environments that are hosted within this repository must be maintained on the
lowside to prevent merge conflicts on the highside. It is advisable that
highside environments be stored in their own version control system is cloned
into the ipa-environment project root at provisioning time.

## New Environment
For illustration purposes the environment we will create will be called _myenv_

### Directory Layout
Create a directory layout similar to the structure illustrate below:
```
+-- myenv
|   +-- group_vars
|   |   +-- all.yml
|   |   +-- ipa-replica.yml
|   |   +-- ipa-server.yml
|   |   +-- ipa-masters.yml
|   +-- inventory
|   +-- README.md
```
* `inventory` is the ansible inventory file for this environment; hosts and
alignment to groups is done in here. The groups defined here will determine the
files that exist in the `group_vars` directory.

* `group_vars` contains all the groups that have been specified in the with
exception of the special _all_ group `all.yml` which is internal catch all group.

* `README.md` please provide a README file for the environment so nuances can
be explained as well as sample execution process.

## Minimal Variables
The environment does provide some sane default variables however the following
variables must be provided to successfully execution an environment
* `env_name`: The name of the environment - Default: " "
* `realm_name`: The name of the Kerberos Realm - Default: " "

## Executing the environment
Selecting the new environment for deployment through use of the `-i` |
`--inventory-file=` parameter.
```shell
ansible-playbook -i myenv site.yml
```
## Example environment
Please refer to the integration environment as a good (mostly static) example of
an environment.
