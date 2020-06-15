#! /bin/bash

set -eu

################################################################################
# This script runs through a full Ansible Tower Installation into a docker container spun up locally


#### Parameters

SCRIPT_DIR="./scripts"
TEST_DIR="./tests"
PLAYBOOKS_DIR="./playbooks"
ANSIBLE_TOWER_SETUP_DIR="./playbooks/ansible-tower-setup"
INVENTORY_DIR="${TEST_DIR}"
TARGET_INVENTORY="test-inventory"

#### Script and playbook invocation
#### Do not edit below this line

INVENTORY_PATH="${INVENTORY_DIR}/${TARGET_INVENTORY}"
export ANSIBLE_CONFIG="${TEST_DIR}/ansible.cfg"

#### Download all role dependencies
./"${SCRIPT_DIR}"/download-role-dependencies.sh

#### Provision test infrastructure
ansible-playbook "${TEST_DIR}/provision-test-infra.yml" \
    --inventory "${INVENTORY_PATH}"

#### Check connectivity
ansible all \
    -m ping \
    --inventory "${INVENTORY_PATH}" \

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
