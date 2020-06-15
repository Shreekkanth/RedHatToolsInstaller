#!/bin/bash

source variables.sh

for i in $(seq 1 ${orgs}); do
  # To interface with Azure
  tower-cli credential create --name azure_creds${i} --description "Credentials to interface with Azure" --organization org${i} --credential-type="Microsoft Azure Resource Manager" --inputs="{subscription: ${SUB_ID}, client: ${CLIENTID}, tenant: ${TENANT}, secret: ${SECRET}}" -u admin -p ${TOWERPW}

  # To log into the Tower server itself
  tower-cli credential create --name localcreds${i} --description "Credentials to interface with localhost" --organization org${i} --credential-type="Machine" --inputs="username: awx" -u admin -p ${TOWERPW}
done
