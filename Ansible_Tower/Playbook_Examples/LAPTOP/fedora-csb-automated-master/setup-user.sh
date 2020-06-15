#!/bin/bash

# TODO check that local configuration file has been adapted

# And then call the right book as the current user
ansible-playbook fedora-user.yml "$@"
