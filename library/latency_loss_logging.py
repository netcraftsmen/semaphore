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
#
#      references:
#          https://documentation.meraki.com/MX/Monitoring_and_Reporting/Appliance_Status/MX_Uplink_Settings


import os
import subprocess
import json
import sys
from uuid import uuid4
from confluent_kafka import avro, KafkaError, Producer
from confluent_kafka.admin import AdminClient, NewTopic

import certifi

import meraki

try:
    from latency_loss_logging_constants import MERAKI, LOGGING, SCHEMA_CONF, PRODUCER_CONF
except ImportError:
    print('Could not import constants!')
    exit()

                    
def call_back(err, msg):
    """ 
        Call back handler
        p.poll() serves delivery reports (on_delivery) from previous produce() calls
    """
    if err is None:
        print("Produced record to topic {} partition [{}] @ offset {}".format(msg.topic(), msg.partition(), msg.offset()))    
    else:
        print("Failed to deliver message: {}".format(err))

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
        #
        # Get the management interface and dynamic DNS host names for the public addressing
        mgmt = dashboard.devices.getDeviceManagementInterface(device['serial'])
        #
        # The device stats returns a list of stats, determined by the length of timespan
        stats = dashboard.devices.getDeviceLossAndLatencyHistory(device['serial'], target, 
                                                                    timespan=timespan, uplink=uplink)
        #
        # Put the public hostname(s) in each record
        for stat in stats:
            stat.update( mgmt['ddnsHostnames'] )
        
        response.extend(stats)

    return response

def logging(records):
    """ 
        Generate (and filter) what is logged and optionally print out.

        {'startTs': '2021-01-29T21:49:00Z', 'endTs': '2021-01-29T21:50:00Z', 'lossPercent': None, 
        'latencyMs': None, 'activeDdnsHostname': 'swisswood-cnrtbtvnkm.dynamic-m.com', 
        'ddnsHostnameWan1': 'swisswood-cnrtbtvnkm-1.dynamic-m.com', 'ddnsHostnameWan2': 
        'swisswood-cnrtbtvnkm-2.dynamic-m.com'}
    """

    for record in records:

        if True:                                           # TODO ADD TEST to see this record is of interest
            msg = ''
            for key, value in record.items():              # Convert to  a string in the form of: key=value
                msg += f'{str(key)}={str(value)} '

        cmd = ['/usr/bin/logger', '--server', f'{LOGGING["server"]}', '--port',
                f'{LOGGING["port"]}', '--udp', f'"{msg}"']

        returned_output = subprocess.run(cmd, stdout=subprocess.PIPE).stdout

        if LOGGING.get('debug'):
            print(f'CMD:{cmd} \n MSG:{msg}')
            print(f'OUTPUT:{returned_output.decode("utf-8")} \n ------')

def producer(records, topic='topic_0'):
    """
       Topic is defined from GUI
       https://confluent.cloud/environments/env-9vzp0/clusters/lkc-gd35m/topics
       Kafka organizes message feeds into categories called topics.

       A topic is an ordered log of events. When an external system 
       writes an event to Kafka, it is appended to the end of a topic.

       A Topic is a category/feed name to which records are stored and published. 
       All Kafka records are organized into topics. Producer applications write data to topics 
       and consumer applications read from topics. Records published to the cluster 
       stay in the cluster until a configurable retention period has passed by.
       
       Each topic can have multiple partitions, in this example, we have the default value of 6 partitions
       Each partition is a single log file where records are written to it append-only.
    """

    # Create Producer instance
    # A producer is an external application (this program) that writes messages to a Kafka cluster
    producer = Producer(PRODUCER_CONF)

    for record in records:
        # For two records with the same key, the producer will always choose the same partition
        record_key = '2'
        record_value = json.dumps(record)
        producer.produce(topic, key=record_key, value=record_value, on_delivery=call_back)

        producer.poll(0)  # invoke the on_delivery=call_back function

    producer.flush()  # flush() will block until the previously sent messages are delivered
    return


def main():

    
    if os.getenv('MERAKI_DASHBOARD_API_KEY', None):
        dashboard = meraki.DashboardAPI(output_log=False)     
    else:
        # by default, the API looks for the API key in environment variable MERAKI_DASHBOARD_API_KEY
        print('please create and specify the API key, e.g. "export MERAKI_DASHBOARD_API_KEY=12345"')

    logging(get_stats(dashboard))     # Write to syslog
    producer(get_stats(dashboard))    # Write to Kafka


if __name__ == '__main__':
    main()