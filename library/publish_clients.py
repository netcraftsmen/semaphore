#!/usr/bin/env python3
#
#     Copyright (c) 2023
#     All rights reserved.
#
#     author: Joel W. King  @joelwking
#
#     usage: python3 ./publish_clients.py
#
#     linter: flake8
#         [flake8]
#         max-line-length = 160
#         ignore = E402
#

import os
import argparse
from confluent_kafka import avro, KafkaError, Producer
# from confluent_kafka.admin import AdminClient, NewTopic

import meraki

try:
    from latency_loss_logging_constants import MERAKI, LOGGING, SCHEMA_CONF, PRODUCER_CONF, PRODUCER_ARGS
    from latency_loss_logging import call_back, kafka
    from filter import filters
except ImportError:
    print('import error!')
    exit(1)

CAMERA = 'camera'
FUZZY = 'fuzzy'

def get_clients(dashboard, filter_config=None):
    """
    Retrieve all the clients by network and publish to Kafka
    Get all the organizations, the networks in each org, and clients in each network
    Update the client with the organization ID and network name.

    Call the `kafka` method (from latency_loss_logging) to publish.
    """
    try:
        orgs = dashboard.organizations.getOrganizations()
    except meraki.exceptions.APIError as e:
        print(f'ERROR: {e}')
        return

    for org in orgs:
        for network in dashboard.organizations.getOrganizationNetworks(org['id']):
            if CAMERA in network.get('productTypes', []):
                continue  # Camera networks have no clients
            try:
                clients = dashboard.networks.getNetworkClients(network['id'], timespan=MERAKI['timespan'], perPage=MERAKI['per_page'], total_pages='all')
            except meraki.exceptions.APIError as e:
                if e.status in ("404",):
                    print(f'No clients for {network["id"]}, status= {e.status}, reason= {e.reason}, error= {e.message}')
                    continue
                else:
                    raise ValueError(f'ERROR: {e}')
            
            records = []
            for client in clients:
                selected = select_client_records(filter_config, client)
                if selected:
                    selected.update(dict(organizationId=network['organizationId'], networkName=network['name']))
                    records.append(selected)

            # call the Kafka publisher, sending a list with one entry, a dictionary with the key
            # 'payload' where the value is the the list of clients
            if records:
                kafka([dict(payload=records, network=network['id'], networkName=network['name'])], key=network['id'])

    return

def select_client_records(filter_config, client):
    """
        Return an updated client record if it meets the selection criteria
    """
    client.update(dict(filter_config=filter_config))
    client.update(dict(conditional_match=filters.Conditional(filter_config, client).compare()))

    # If the user asks for a fuzzy match, we always return the record
    if filter_config.get(FUZZY):
        result = filters.Fuzzy(filter_config[FUZZY]['value'], client.get(filter_config[FUZZY]['key'])).compare()
        client.update(result)
        return client
    
    if client['conditional_match']:
        return client
    
    return False
    

def main():
    """
        Check for the Meraki API key and parse any arguments
    """
    if os.getenv('MERAKI_DASHBOARD_API_KEY', None):
        dashboard = meraki.DashboardAPI(output_log=False, print_console=MERAKI['print_console'])
    else:
        # by default, the API looks for the API key in environment variable MERAKI_DASHBOARD_API_KEY
        print('please create and specify the API key, e.g. "export MERAKI_DASHBOARD_API_KEY=12345"')

    parser = argparse.ArgumentParser(prog='publish_clients.py', description='Publish clients')
    parser.add_argument('-f', '--filter', dest='filterfname', help='filter filename', required=False)
    args = parser.parse_args()
    
    valid = False
    valid = filters.Conditional(filters.read_filter_configuration(args.filterfname), dict())
    if not valid:
        print(f'Filter filename not valid or invalid JSON {args.filterfname}')
        exit(1)

    get_clients(dashboard, filter_config=filters.read_filter_configuration(args.filterfname))


if __name__ == '__main__':
    main()
