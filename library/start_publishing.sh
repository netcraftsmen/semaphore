#!/bin/bash
#
#      Copyright (c) 2023
#      All rights reserved
#
#      Bash shell to invoke a Python program to publish Kafka messages
#
#      Usage:  ./start_publishing.sh
#
#      Environment variables:
#
#        export PUBLISHER_PROGRAM=./publish_clients.py  program name
#        export PUBLISHER_TIMER=300                     number of seconds between program iterations
#        export PUBLISHER_FILTER=filter.json            filename of the filter
#        export PUBLISHER_REPO=https://raw.githubusercontent.com/netcraftsmen/cfic_filters/main/meraki/
#
if [ -z "$1" ]; then
    fname=$PUBLISHER_FILTER
else
    fname=$1
fi
if [ -z "$2" ]; then
    repo=$PUBLISHER_REPO
else
    repo=$2
fi
#
# Download a the file
#
wget $repo$fname  -O /tmp/$fname

while true; do python3 $PUBLISHER_PROGRAM -f /tmp/$fname; sleep $PUBLISHER_TIMER; done