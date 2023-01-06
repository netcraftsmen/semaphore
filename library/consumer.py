#!/usr/bin/env python3
#
#     Copyright (c) 2022
#     All rights reserved.
#
#     author: Joel W. King  @joelwking
#
#     usage: python3 ./consumer.py
#
#     linter: flake8
#         [flake8]
#         max-line-length = 160
#         ignore = E402
#
#     Reference:
#       - https://medium.com/fintechexplained/12-best-practices-for-using-kafka-in-your-architecture-a9d215e222e3
#
from latency_loss_logging_constants import CONSUMER_CONF, PRODUCER_ARGS
# from confluent_kafka import avro, KafkaError
from confluent_kafka import Consumer

import argparse
import json

parser = argparse.ArgumentParser(prog='consumer.py', description='Kafka consumer')
parser.add_argument('-g', '--group', dest='group', help='group ID', default='group_1', required=False)
parser.add_argument('-o', '--offset', dest='offset', choices=['latest', 'earliest'], help='auto.offset.reset', default='earliest', required=False)
parser.add_argument('-t', '--timeout', dest='timeout', help='poll timeout (sec)', default=5.0, required=False)
parser.add_argument('-r', '--range', dest='range', help='number of polling iterations', default=65536, required=False)
args = parser.parse_args()

CONSUMER_CONF['group.id'] = args.group            # only one consumer within a consumer group gets a message from a partition.
CONSUMER_CONF['auto.offset.reset'] = args.offset  # Consume from the beginning of the topic, vs. latest, consume from the end

consumer = Consumer(CONSUMER_CONF)
consumer.subscribe([PRODUCER_ARGS['topic']])      # for demo, consume the topic we produced


def main():
    """
        Consume messages from Kafka
    """

    for n in range(1, args.range):

        msg = consumer.poll(args.timeout)
        if msg is None:
            print(f'Waiting for message or event/error in poll() {n} of {args.range} iterations')
            continue
        elif msg.error():
            print(f'error: {msg.error()}')
        else:
            # Received a message
            
            print(f'offset:{msg.offset()} partition:{msg.partition()} key:{msg.key()} ')
            print(json.dumps(json.loads(msg.value()), sort_keys=False, indent=4))

    # consumer.close()    TODO causing exceptions


if __name__ == '__main__':
    main()
