#!/usr/bin/env python3
#
#     Copyright (c) 2022
#     All rights reserved.
#
#     author: Joel W. King  @joelwking
#
#     usage: python3 ./latency_loss_logging.py
#
#     linter: flake8
#         [flake8]
#         max-line-length = 160
#         ignore = E402
#
#      references:
#          https://documentation.meraki.com/MX/Monitoring_and_Reporting/Appliance_Status/MX_Uplink_Settings

import os
import subprocess
import json
import argparse
# from uuid import uuid4
from confluent_kafka import avro, KafkaError, Producer
# from confluent_kafka.admin import AdminClient, NewTopic

import certifi

import meraki

try:
    from latency_loss_logging_constants import MERAKI, LOGGING, SCHEMA_CONF, PRODUCER_CONF, PRODUCER_ARGS
except ImportError:
    print('Could not import constants!')
    exit(1)


def call_back(err, msg):
    """
        Kafka call back handler
    """
    if err is None:
        print(f"Produced record to topic {msg.topic()} partition [{msg.partition()}] @ offset {msg.offset()}")
    else:
        print(f"Failed to deliver message: {err}")


def get_devices(dashboard, firewalls=MERAKI['firewalls']):
    """
        Get all the organizations, the networks in each org, and the devices in each network

        Identify firewall device types of interest, we return a list of firewall devices
        In the Meraki topology, the firewall devices manage the uplink(s) for a network.
    """
    response = []

    try:
        orgs = dashboard.organizations.getOrganizations()
    except meraki.exceptions.APIError as e:
        print(f'ERROR: {e}')
        return response

    for org in orgs:
        for network in dashboard.organizations.getOrganizationNetworks(org['id']):
            devices = dashboard.networks.getNetworkDevices(network['id'])

            for device in devices:
                if device.get('model') in firewalls:
                    response.append(device)
    return response


def get_stats(dashboard, target=MERAKI['target'], timespan=MERAKI['timespan'], uplink=MERAKI['uplink']):
    """
        Get the Loss and Latency History from the firewall device uplink.
    """
    response = []

    for device in get_devices(dashboard):

        # Get the management interface and dynamic DNS host names for the public addressing
        mgmt = dashboard.devices.getDeviceManagementInterface(device['serial'])

        # The device stats returns a list of stats, determined by the length of timespan
        stats = dashboard.devices.getDeviceLossAndLatencyHistory(device['serial'], target,
                                                                 timespan=timespan, uplink=uplink)

        # Put the public hostname(s) in each record
        for stat in stats:
            stat.update(mgmt['ddnsHostnames'])

        response.extend(stats)

    return response


def syslog(records):
    """
        Generate (and filter) what is logged and optionally print out.

        Sample input record
        {'startTs': '2021-01-29T21:49:00Z', 'endTs': '2021-01-29T21:50:00Z', 'lossPercent': None,
        'latencyMs': None, 'activeDdnsHostname': 'swisswood-cnrtbtvnkm.dynamic-m.com',
        'ddnsHostnameWan1': 'swisswood-cnrtbtvnkm-1.dynamic-m.com', 'ddnsHostnameWan2':
        'swisswood-cnrtbtvnkm-2.dynamic-m.com'}
    """

    for record in records:

        if True:                                   # TODO ADD TEST to see this record is of interest
            msg = ''
            for key, value in record.items():      # Convert to a string in the form of: key=value
                msg += f'{str(key)}={str(value)} '

        cmd = ['/usr/bin/logger', '--server', f'{LOGGING["server"]}', 
                                  '--port', f'{LOGGING["port"]}', 
                                  '--udp', f'"{msg}"']

        returned_output = subprocess.run(cmd, stdout=subprocess.PIPE).stdout

        if LOGGING.get('debug'):
            print(f'CMD:{cmd} \n MSG:{msg}')
            print(f'OUTPUT:{returned_output.decode("utf-8")} \n ------')


def kafka(records, topic=PRODUCER_ARGS['topic'], key=PRODUCER_ARGS['key']):
    """
        Publish messages to a topic, an ordered log of events. Each topic can have multiple partitions.
        For two records with the same key, the producer will always choose the same partition. If the
        key is not specified, message are written round-robin across all partititons.
    """

    producer = Producer(PRODUCER_CONF)    #  Producers write messages to a Kafka cluster

    args = dict(on_delivery=call_back)    # Refer to Kafka call back handler function (call_back) defined above

    if key is not None:
        args['key'] = str(key)

    for record in records:
        producer.produce(topic, value=json.dumps(record), **args)
        producer.poll(0)        # invoke the on_delivery=call_back function

    producer.flush()            # flush() will block until the previously sent messages are delivered
    return


def main():
    """
        Check for the Meraki API key, determine if we are logging to Syslog or publishing to Kafka
    """
    if os.getenv('MERAKI_DASHBOARD_API_KEY', None):
        dashboard = meraki.DashboardAPI(output_log=False, print_console=MERAKI['print_console'])
    else:
        # by default, the API looks for the API key in environment variable MERAKI_DASHBOARD_API_KEY
        print('please create and specify the API key, e.g. "export MERAKI_DASHBOARD_API_KEY=12345"')

    parser = argparse.ArgumentParser(prog='latency_loss_logging.py', description='Demonstration of telemetry logging and publishing')
    parser.add_argument('-a', '--action', dest='action', choices=['syslog', 'kafka', 'both'], help='action', default='both', required=False)
    args = parser.parse_args()

    if args.action in ('syslog', 'both'):
        syslog(get_stats(dashboard))       # Write to syslog

    if args.action in ('kafka', 'both'):
        kafka(get_stats(dashboard))        # Publish to Kafka


if __name__ == '__main__':
    main()
