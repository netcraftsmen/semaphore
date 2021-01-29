#!/usr/bin/env python3
#
#     Copyright (c) 2020 World Wide Technology
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

import meraki
import os
import subprocess
import json

try:
    from latency_loss_logging_constants import MERAKI, LOGGING
except ImportError:
    print('Could not import constants!')
    exit()


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
        # Put the public hostname in each record
        for stat in stats:
            stat.update( {"ddnsHostnames": mgmt['ddnsHostnames']})
        
        response.append(stat)

    return response

def logging(records):
    """ 
        Generate (and filter) what is logged and optionally print out.
    """

    for record in records:
        if True:
            msg = record  # TODO filter:: Here we can determine if this record should be logged

        msg = json.dumps(msg)

        cmd =  f'/usr/bin/logger --server {LOGGING["server"]} --port {LOGGING["port"]} --udp {msg}'
        returned_output = subprocess.check_output(cmd)

        """
        OSError: [Errno 36] File name too long: "/usr/bin/logger --server 3.238.50.209 --port 514 --udp 
        {'startTs': '2021-01-29T21:49:00Z', 'endTs': '2021-01-29T21:50:00Z', 'lossPercent': None, 
        'latencyMs': None, 'ddnsHostnames': {'activeDdnsHostname': 'swisswood-cnrtbtvnkm.dynamic-m.com', 
        'ddnsHostnameWan1': 'swisswood-cnrtbtvnkm-1.dynamic-m.com', 'ddnsHostnameWan2': 
        'swisswood-cnrtbtvnkm-2.dynamic-m.com'}}"
        """



        if LOGGING.get('debug'):
            print(f'{cmd} \n {msg}')
            print(f'{returned_output.decode("utf-8")} \n ------')

def main():

    
    if os.getenv('MERAKI_DASHBOARD_API_KEY', None):
        dashboard = meraki.DashboardAPI(output_log=False)     
    else:
        # by default, the API looks for the API key in environment variable MERAKI_DASHBOARD_API_KEY
        print('please create and specify the API key, e.g. "export MERAKI_DASHBOARD_API_KEY=12345"')

    logging(get_stats(dashboard))


if __name__ == '__main__':
    main()