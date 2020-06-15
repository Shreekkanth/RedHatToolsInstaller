#! /bin/bash

set -eu

################################################################################
# This script runs through a full Ansible Tower Installation
# 
# Ensure all options neccessary for installation are either specified in the
# + group vars, inventory file, or the ansible.cfg file in the root of this
# + repository


#### Parameters

SCRIPT_DIR="./scripts"
PLAYBOOKS_DIR="./playbooks"
ANSIBLE_TOWER_SETUP_DIR="./playbooks/ansible-tower-setup"
INVENTORY_DIR="./inventories"
TARGET_INVENTORY="${1:-sandbox}"

#### Script and playbook invocation
#### Do not edit below this line

INVENTORY_PATH="${INVENTORY_DIR}/${TARGET_INVENTORY}"

#### Download all role dependencies
./"${SCRIPT_DIR}"/download-role-dependencies.sh

#### Check connectivity
ansible all \
    -m ping \
    --inventory "${INVENTORY_PATH}"

#### Download setup tarball
ansible-playbook "${PLAYBOOKS_DIR}/download-tower-setup-tarball.yml"

#### Run Pre-Installation Tasks
ansible-playbook "${PLAYBOOKS_DIR}/pre-installation.yml" \
    --inventory "${INVENTORY_PATH}"

#### Install Tower
./"${ANSIBLE_TOWER_SETUP_DIR}"/setup.sh \
    -i "${INVENTORY_PATH}"

#### Run Post-Installation Tasks
ansible-playbook "${PLAYBOOKS_DIR}/post-installation.yml" \
    --inventory "${INVENTORY_PATH}"
