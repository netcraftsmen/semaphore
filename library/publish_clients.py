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
    from latency_loss_logging import call_back, kafka
except ImportError:
    print('Could not import constants!')
    exit(1)

def clients(dashboard):
    """
    Retrieve all the clients by network and publish to Kafka
    Get all the organizations, the networks in each org, and the devices in each network
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
                #### Get Clients and append to the list of clients
                    response.append(clients)
    return response

def main():
    """
        Check for the Meraki API key ....
    """
    if os.getenv('MERAKI_DASHBOARD_API_KEY', None):
        dashboard = meraki.DashboardAPI(output_log=False, print_console=MERAKI['print_console'])
    else:
        # by default, the API looks for the API key in environment variable MERAKI_DASHBOARD_API_KEY
        print('please create and specify the API key, e.g. "export MERAKI_DASHBOARD_API_KEY=12345"')

    parser = argparse.ArgumentParser(prog='publish_clients.py', description='Publish clients')
    parser.add_argument('-d', '--debug', dest='debug', help='debug', required=False)
    args = parser.parse_args()

    kafka(clients(dashboard))        # Publish to Kafka

if __name__ == '__main__':
    main()
