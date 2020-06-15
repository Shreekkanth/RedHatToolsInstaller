#!/bin/bash

source variables.sh

for i in $(seq 1 ${orgs}); do

  tower-cli inventory create --name "localhost_only${i}" --description "Inventory to use with azurevms${i} project" --organization org${i} -u admin -p $TOWERPW

  tower-cli group create -n "localhost" -d "Only localhost in here" -i "localhost_only${i}" -u admin -p $TOWERPW

  tower-cli host create -n localhost --variables="ansible_connection: local" -d "The local machine" --enabled true -u admin -p $TOWERPW -i localhost_only${i}

  inv_id=$(tower-cli inventory list -a -u admin -p $TOWERPW | grep "localhost_only${i} " | sed -e 's/^[[:space:]]*//' | cut -f1 -d " ")
  echo inv_id=${inv_id}

  host_id=$(tower-cli host list --name localhost -a -u admin -p $TOWERPW | sed -e 's/^[[:space:]]*//' | awk -F" " -v inv_id=${inv_id} '{if($3==inv_id) print $1; }')
  echo host_id=${host_id}

  group_id=$(tower-cli group list --name localhost -a -u admin -p $TOWERPW | sed -e 's/^[[:space:]]*//' | awk -F" " -v inv_id=${inv_id} '{if($3==inv_id) print $1; }')
  echo group_id=${group_id}

  tower-cli host associate --host ${host_id} --group ${group_id} -u admin -p $TOWERPW

  tower-cli role grant --team team${i} -i localhost_only${i} --type use -u admin -p $TOWERPW
done

