Ansible Tower Management
========================

This is a repository that contains playbooks for installation, upgrades, and maintainance of an Ansible Tower Cluster.  Since each environment is different, different pre and post installation and upgrade tasks may be neccessary. Edit the pre and post installation playbooks as neccessary.

All playbooks in this repository as well as the Ansible Tower setup script should be run from the top level of this repository, i.e in the same directory ansible.cfg file. This ensures that all proper Ansible configurations will be applied for each playbook run.

If you do not have a License to use tower, [request one here](https://www.ansible.com/license). 

Use of this Repository
-----------------------

### Installation:

1. Clone repository to the machine that will run the Ansible Tower Installation. After cloning this playbook, make the following alterations:
2. Re-key the vaulted vars files. The default Ansible vault password is `password`.
3. Update or add an inventory file for the environment Tower will be installed in.
4. Update group vars for the environment Tower will be installed in. Please update all password variables to set strong passwords.
5. Run Ansible Tower installation. From the root of the cloned tower repository, run `./scripts/test-tower-installation.sh`

### Development

1. Clone repository to machine that will be used for development
2. Add Tower license to the `files` directory. Call this file tower-license.txt. Make sure the json in this file has the `eula_accepted` key present, and set to "true".
3. Ensure Docker is installed, the docker daemon is running, and the docker-py python package is installed.
4. Choose container image with an init system to test installation. By default, centos/systemd is used. If another image is desired, update the `tower_docker_image` variable in the tests/test-inventory file.
5. Run the test installation into the container - `./scripts/test-tower-installation.yml. The container name that will be running is ansible-tower-test, with ports 80 and 443 open on localhost on the development machine.
6. After installation is complete, browse to https://localhost. A Tower instance should now be up and running.

Scripts
-----------

### download-role-dependencies.sh

Uses `ansible-galaxy` to download roles in `roles/requirements.yml`.

```
./scripts/download-role-dependencies.sh
```

### run-tower-installation.sh

Run through a full Ansible Tower installation. By default, it will run against the 'sandbox' inventory. To select another inventory, provide a parameter that is the inventory name.

```
# Run sandbox cluster installation
./scripts/run-tower-installation.sh
# Run production tower installation, using ./inventories/production
./scripts/run-tower-installation.sh production
```

### test-tower-installation.sh

Test the tower installation in a centos 7 container. Uses the inventory in the tests directory.

```
./scripts/test-tower-installation.sh
```


Playbooks
-----------------------

### pre-installation.yml

The pre-installation playbook should be run against all nodes in the Ansible Tower cluster before installation is attempted. This file currently configure anything, since it is highly dependent on each environment.

### post-installation.yml

The post-installation playbook should be run after the Ansible Tower Cluster installation has successfully completed. It ensures a Tower License is applied and enforces Tower application configuration.

This playbook can upload a license if an `ansible_tower_license` variable with license file content is defined. This can be a JSON string in an inventory, use a file lookup, or a yaml dictionary and use the `to_json` filter. Make sure the `elua_accepted` key is set to true. This [support article has more information](https://access.redhat.com/solutions/3065701).

### update-ansible.yml

The update-ansible playbook upgrades the version of Ansible Core on all of the Ansible Tower nodes. Ansible Core can be updated independently of Ansible Tower. This can be done without taking downtime for the Ansible Tower Cluster. Here is a [related support case](https://access.redhat.com/solutions/3078371). Be sure to consult the [Ansible Tower docs](http://docs.ansible.com/ansible-tower/latest/html/installandreference/requirements_refguide.html#requirements) to ensure the version of Ansible Core you are using is compatible with Ansible Tower.

Running Tests
------------------

This repository contains simple local provisioning tests for Ansible Tower. This is to simplify development of pre and post installation configuration routines. The `test-tower-installation.sh` script starts a centOS 7 systemd container, downloads the setup bundle, then runs through a full installation. To use the tower instance after installation into the centOS container, upload a valid tower license. You may need to [disable Tower bubblewrap functionality](http://docs.ansible.com/ansible-tower/latest/html/administration/troubleshooting.html#bubblewrap-functionality-and-variables).
