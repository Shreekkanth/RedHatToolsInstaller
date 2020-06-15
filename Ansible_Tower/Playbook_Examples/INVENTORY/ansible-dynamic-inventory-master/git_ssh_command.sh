#!/bin/sh
#Overrides git's default SSH behavior and uses this script for SSH operations
exec /usr/bin/ssh -o StrictHostKeyChecking=no -i $PCDB_GIT_SSH_KEY "$@"
