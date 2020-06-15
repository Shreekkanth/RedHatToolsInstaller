#!/bin/bash
CONFIG="~/.hammer/cli_config.yaml"
if ! $( gem list hammer_cli > /dev/null )
then
    echo "Install hammer cli and try again"
    exit 1
fi

HAMMER_CMD=$(gem contents hammer_cli | grep bin)

$HAMMER_CMD -c $CONFIG template list | grep -vi "default"

