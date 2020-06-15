#!/bin/bash

source variables.sh

for i in $(seq 1 ${orgs}); do

  # If you really need to change the initial default password for the student VMs on Azure, change below.

  tower-cli job_template create --name "create_azure_vm_${i}" --description "Job to create a VM in Azure for org${i}" --job-type run -i localhost_only${i} --project azurevms${i} --playbook create_vms.yml --credential=localcreds${i} -u admin -p $TOWERPW --survey-enabled true --survey-spec '{
    "description": "",
    "name": "",
    "spec": [
        {
            "question_description": "Please listen to us explain this part before pressing any buttons!",
            "min": 6,
            "default": "change_me",
            "max": 1024,
            "required": true,
            "choices": "",
            "variable": "vm_name",
            "question_name": "Name of the VM",
            "type": "text"
        },
        {
            "question_description": "The name of the user you (and Ansible) will use to log into this machine",
            "min": 0,
            "default": "change_me",
            "max": 1024,
            "required": true,
            "choices": "",
            "new_question": true,
            "variable": "admin_user",
            "question_name": "Admin account",
            "type": "text"
        },
        {
            "question_description": "The password for the above user (needs 1 lowercase, 1 uppercase, 1 digit, minimum of 6 chars)",
            "min": 8,
            "default": "",
            "max": 32,
            "required": true,
            "choices": "",
            "new_question": true,
            "variable": "admin_password",
            "question_name": "Admin password",
            "type": "password"
        }
    ]
}'


  tower-cli job_template create --name "delete_azure_vm_${i}" --description "Job to delete a VM in Azure for org${i}" --job-type run -i localhost_only${i} --project azurevms${i} --playbook destroy_vms.yml --credential=localcreds${i} -u admin -p $TOWERPW --survey-enabled true --survey-spec '{
    "description": "",
    "name": "",
    "spec": [
        {
            "question_description": "Please listen to us explain this part before pressing any buttons!",
            "min": 6,
            "default": "change_me",
            "max": 1024,
            "required": true,
            "choices": "",
            "variable": "vm_name",
            "question_name": "Name of the VM",
            "type": "text"
        }
    ]
}'

  tower-cli job_template associate_credential --job-template "delete_azure_vm_${i}" --credential "azure_creds${i}" -u admin -p $TOWERPW
  tower-cli job_template associate_credential --job-template "create_azure_vm_${i}" --credential "azure_creds${i}" -u admin -p $TOWERPW

  tower-cli role grant --team team${i} --job-template delete_azure_vm_${i} --type execute -u admin -p $TOWERPW
  tower-cli role grant --team team${i} --job-template create_azure_vm_${i} --type execute -u admin -p $TOWERPW

done
