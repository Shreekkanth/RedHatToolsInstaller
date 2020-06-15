#!/bin/bash
#This assumes you've setup your private key in gitlab.consulting.redhat.com (to obtain sample PCDB data)
#Run this with the source command to set testing vars:
#example: source ./setup_env_vars.sh
export PCDB_GIT_URL="ssh://git@gitlab.consulting.redhat.com:2222/SWIFT/pcdb-sample-data.git"
export PCDB_GIT_BRANCH="test"
export PCDB_GIT_DIR="git-data"

export | grep PCDB
