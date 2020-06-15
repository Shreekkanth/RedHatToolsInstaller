#!/bin/bash

source variables.sh

for i in $(seq 1 ${orgs}); do
  tower-cli organization create -n org${i} -d "Organization ${i}" -u admin -p ${TOWERPW}
done
