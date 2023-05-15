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
#        $PUBLISHER_PROGRAM  program name
#        $PUBLISHER_TIMER    number of seconds between program iterations
#
fname=filter.json
wget https://raw.githubusercontent.com/netcraftsmen/cfic_filters/main/meraki/$fname  -O /tmp/$fname

while true; do python3 $PUBLISHER_PROGRAM -f /tmp/$fname; sleep $PUBLISHER_TIMER; done