#!/bin/bash

source variables.sh

for i in $(seq 1 ${orgs}); do
  tower-cli user create --username wsadmin${i} --password "${TEMPPW}" -u admin -p ${TOWERPW} --email "root@localhost" --first-name "WorkshopAdmin${i}" --last-name "ForOrg${i}" --is-superuser false
  tower-cli organization associate_admin --organization org${i} --user wsadmin${i} -u admin -p $TOWERPW

  tower-cli user create --username wsuser${i} --password "${TEMPPW}" -u admin -p ${TOWERPW} --email "root@localhost" --first-name "WorkshopUser${i}" --last-name "ForOrg${i}" --is-superuser false
  tower-cli organization associate --organization org${i} --user wsuser${i} -u admin -p $TOWERPW

  tower-cli team create -n team${i} --organization org${i} -d "User team for org${i}" -u admin -p $TOWERPW
  tower-cli team associate --team team${i} --user wsuser${i} -u admin -p $TOWERPW
done
