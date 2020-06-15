#!/bin/bash

source variables.sh

for i in $(seq 1 ${orgs}); do

  tower-cli project create --scm-clean true --scm-update-on-launch false --description "Project for org${i} that holds playbooks to manage VMs on Azure" --name "azurevms${i}" --scm-url "${VCS_URL}" --scm-type git -u admin -p $TOWERPW --organization org${i}

  tower-cli role grant --team team${i} --project azurevms${i} --type use -u admin -p $TOWERPW

done
