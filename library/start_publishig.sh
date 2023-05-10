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
while true; do python3 $PUBLISHER_PROGRAM; sleep $PUBLISHER_TIMER; done