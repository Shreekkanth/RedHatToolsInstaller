#!/bin/bash

# TODO check that local configuration file has been adapted

# we do this here because the first upgrade might break ansible itself
sudo dnf -y upgrade

# Wait a bit to make sure dnf locks are released (had issues)
sleep 5

# And then call the right book, asking again for SUDO password
ansible-playbook -K fedora-csb.yml "$@"
