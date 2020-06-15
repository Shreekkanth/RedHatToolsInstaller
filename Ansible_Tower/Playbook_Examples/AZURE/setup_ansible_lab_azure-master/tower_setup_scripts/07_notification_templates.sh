#!/bin/bash

source variables.sh

for i in $(seq 1 ${orgs}); do

  tower-cli notification_template create -n "slack_notification_${i}" -d "Notify the #notifications channel on ansible-handson-lab.slack.com" --organization org${i} --notification-type slack --channels "${SLACK_CHANNEL}" --token ${TOKEN} -u admin -p $TOWERPW 

done
