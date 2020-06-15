# Ansible Tower Genie Installation Playbook
![Ansible Tower Genie](files/tower-genie.png)
## Table of Contents
- [Description](#description)
- [Requirements](#requirements)
- [Process and Required Information to Install](#process-and-required-information-to-install)
- [Author](#author)

## Description
The purpose of this playbook is to configure and prepare Ansible Tower Genie for use in an Ansible Tower Environment.

## Requirements
This playbook could be run from any system where Ansible Core is installed.  This playbook ensures Git is installed to be able to perform its work.  This should be run as a user with sudo (ALL) privileges for ease of installation.  The sudo privileges are namely to ensure git and Ansible Tower CLI are installed.

## Process and Required Information to Install
The Ansible Tower Genie Installation Playbook conducts a survey/questionnaire to properly build the onboarding-vars.yml and onboarding-secrets.yml variable files.

The initial prompts that the installation playbook conducts pertain to requirements for building a fully functional Ansible Tower Genie Project which will be assembled and pushed into your on premise Git solution as well as connectivity into your preferred Ansbile Tower Server/Cluster.  You will need a Git repository with a single branch (master), the URL to the Git repository, a Git user account and password or SSH key (assumes user executing playbook has the appropriate SSH key for access) to the Git repository, the path to your SSH private key (if using SSH Based Git access to properly build the Ansible Tower credential to the project), the base URL to Ansible Tower environment you will be intalling the Ansible Tower Genie job templates, the Administrative user account and password to the Ansible Tower environment, the Ansible Tower Organization to install to, a password to encrypt (ansible-vault) sensitive information with, the number of Ansible Tower environments to configure with Ansible Tower Genie, and whether or not you would like to create (onboard) new source control repositories/projects as part of platform onboarding.  Currently Ansible Tower Genie only supports creating new repositories in Gitlab.

If you choose to build new Repositories/Projects as a part of the Platform Onboarding process (currently Gitlab is the only supported system,) a series of prompts will ask you about your Source Control environment.  You will need to have a user account with administrative rights to create new Repositories/Projects and Orgs/Groups in the system as well as an API user impersonation token (Gitlab).  

Depending on how many environments/clusters you are configuring Ansible Tower Genie to handle, you will be prompted for information about each of those environments.  You will need the base URL for each Ansible Tower environment, the administrative user account and password, Ansible Tower Organization, if you chose to onboard new repositories into your source control system the branch to map to this environment/cluster, whether or not to allow Teams to create their own job templates (use access on their project branch), and the level of access to grant the new Team on the inventories granted to them (i.e. use, admin, etc).

## Author
[Andrew J. Huffman](mailto:ahuffman@redhat.com)
[Edward Quail](mailto:equail@redhat.com)
