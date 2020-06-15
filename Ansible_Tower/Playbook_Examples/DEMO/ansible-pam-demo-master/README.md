# Ansible PAM Demo

These roles create and remove the HR PAM Demo and all its supporting infrastructure (Jenkins, Nexus) on OpenShift.

Please note that these roles will only deploy onto clusters with the capability to provide storage to workloads.

## Prerequisites

* An OpenShift Cluster

* A currently logged in user on that cluster!

* A route for that cluster - the demo uses path-based routing e.g. pam.apps.${cluster}.demolab.local

* A Git username

* A Gitlab [Personal Access Token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#creating-a-personal-access-token)

See the individual projects for more information on how to use the demo material.

## Usage

Please note that this playbook is a terrible example of how to write a playbook. Or more accurately, it is an excellent example of how *not* to write a playbook. It is not idempotent in any way - to make it so would introduce system level dependencies that cannot be gauranteed between executing hosts.

To avoid any unexpected issues, please run `site-uninstall.yml` between (attempted) deployments as this will clean up the deployed resources.

### Install

`ansible-playbook -i example.hosts site-install.yml -e git_username= -e git_access_token=`

### Uninstall

`ansible-playbook -i example.hosts site-uninstall.yml`