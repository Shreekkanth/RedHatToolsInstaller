#! /bin/bash

ROLES_PATH="${1:-./roles}"
ROLES_FILE="${2:-$ROLES_PATH/requirements.yml}"

ansible-galaxy install \
    --role-file="${ROLES_FILE}" \
    --roles-path="${ROLES_PATH}" \
    --force \
    --verbose
