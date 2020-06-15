![Sat-deploy](spaceship.png)

# Sat-deploy: Blasting Satellite into your environment

This repository holds scripts and configuration to deploy Satellite through
Vagrant and Ansible. The repository is not designed to be stand-alone and requires the
upstream [forklift](https://github.com/theforeman/forklift) repository.

## Setup

This repository focuses on using Vagrant and Ansible to setup and configure Satellite and Capsule installations. The Ansible playbooks may be used directly if bringing your own hardware. The minimal requirement is Ansible. Vagrant is only required if using the built-in box configurations and setup that is the primary use case of this repository.

Dependencies

 * Ansible Latest
 * Vagrant 2.X

```
# only needed when RH IT cert is not known
update-ca-trust enable
curl https://password.corp.redhat.com/RH-IT-Root-CA.crt > /etc/pki/ca-trust/source/anchors/redhat.crt
update-ca-trust extract

git clone https://gitlab.sat.engineering.redhat.com/satellite6/sat-deploy.git
cd sat-deploy
git clone https://github.com/theforeman/forklift.git
```

If using Vagrant, check that everything is configured correctly:

```
vagrant status
```

## Spin Up Latest Satellite Snap Box

If using Ansible directly instead of Vagrant, you will need to define an inventory for your Satellite and/or Capsule. Ensure that the Satellite is in a 'server' group and the Capsule in a 'capsule' group.

### Running installation and upgrade pipelines

An installation test would look like:

```
ansible-playbook pipelines/satellite_install.yml -e pipeline_os=rhelX (rhel version) -e pipeline_version=X.X (satellite version)
```

An upgrade pipeline test would look like:

```
ansible-playbook pipelines/satellite_upgrade.yml -e pipeline_os=rhelX (rhel version) -e pipeline_version=X.X (base satellite version) upgrade_vesion=X.X (version upgrading to)
```

### Satellite 6.4+

The latest Satellite 6.y box can be built with:

```
vagrant up sat-6.{y}-qa-rhel7
```

If using Ansible directly:

```
ansible-playbook playbooks/satellite.yml -e satellite_version=6.{y} -e activation_key='satellite-6.{y}-qa-rhel7'
```

The latest Capsule 6.y box can be built with (ensure you have spun up the sat-6.y-qa-rhel7 box first):

```
vagrant up capsule-6.{y}-qa-rhel7
```

If using Ansible directly:

```
ansible-playbook playbooks/capsule.yml -e satellite_version=6.{y} -e activation_key='capsule-6.{y}-qa-rhel7'
```

### Upgrade to 6.4+

To upgrade an existing box to 6.5, the following playbook can be run:

```
ansible-playbook playbooks/satellite_upgrade.yml -e satellite_version=6.{y} -l <hostname>
```

Where `<hostname>` can either be the hostname or the box name of an existing box.

### Satellite 6.3

The latest Satellite 6.3 box can be built with:

```
vagrant up sat-6.3-qa-rhel7
```

If using Ansible directly:

```
ansible-playbook playbooks/satellite.yml -e satellite_version=6.3 -e activation_key='satellite-6.3-qa-rhel7'
```

The latest Satellite 6.3 box with Puppet 4 can be built with:

```
vagrant up sat-6.3-qa-rhel7-puppet4
```

The latest Capsule 6.3 box can be built with (ensure you have spun up the sat-6.3-qa-rhel7 box first):

```
vagrant up capsule-6.3-qa-rhel7
```

If using Ansible directly:

```
ansible-playbook playbooks/capsule.yml -e satellite_version=6.3 -e activation_key='capsule-6.3-qa-rhel7'
```

#### Running 6.3 Load Balance Capsules pipeline

After cloning `sat-deploy` and `forklift` as shown in the Setup section, this playbook also requires foreman-ansible-modules:

```
cd sat-deploy
git clone https://github.com/theforeman/foreman-ansible-modules.git
cd foreman-ansible-modules
pip install -r requirements.txt
cd ..
ansible-playbook -e "forklift_state=up" pipelines/qa_test_63_rhel7_lbcaps.yml
```

### Upgrade to 6.3

To upgrade an existing box to 6.3, the following playbook can be run:

```
ansible-playbook playbooks/satellite_upgrade.yml -e satellite_version=6.3 -l <hostname>
```

Where `<hostname>` can either be the hostname or the box name of an existing box.
