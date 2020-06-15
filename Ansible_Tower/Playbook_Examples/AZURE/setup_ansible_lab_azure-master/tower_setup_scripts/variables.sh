#!/bin/bash

# the Tower password to run API calls with
export TOWERPW=""

# SSH Private key to connect to the Tower server
export SSH_LOCALHOST_KEY_FILE="PATH_TO_SSH_PRIVATE_KEY"

# SSH Private key to connect to a VCS like Github or Bitbucket
export SSH_VCS_KEY_FILE="PATH_TO_SSH_PRIVATE_KEY"

# VCS URL - project that holds playbook to create and destroy VMs on Azure
export VCS_URL="https://github.com/dieterdm/azure_create_vms.git"

# amount of organizations to create
export orgs=

# temporary password for the wsuserX and wsadminX accounts
export TEMPPW=""

# azure service principal credentials
export SUB_ID= 				# this is the ID of your subscription itself
export TENANT=					# this is the ID of the AD you use in Azure 
export CLIENTID= 				# this is the ID of the application (app registration) you created
export SECRET=					# this is the secret key you assigned to that application

# Slack token
export TOKEN=

# Name of Slack channel to send notifications to; variable is only used in comment
export SLACK_CHANNEL="ansible-handson-lab.slack.com"

