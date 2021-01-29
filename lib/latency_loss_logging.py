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
import os, subprocess

try:
    import latency_loss_logging_constants
except ImportError:
    print('Could not import constants!')


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

    """
    response = []

    for device in get_devices(dashboard):
        mgmt = dashboard.devices.getDeviceManagementInterface(device['serial'])
        print(mgmt['ddnsHostnames'])

        response = dashboard.devices.getDeviceLossAndLatencyHistory(device['serial'], target, 
                                                                    timespan=timespan, uplink=uplink)
        """
        for item in response:
            item.update( {"ddnsHostnames":mgmt['ddnsHostnames']})
        """


    return response

def logging(records):
    """ 
        Generate (and filter) what is logged and optionally print out.
    """

    for record in records:
        if True:
            msg = record                                   # TODO filter:: Here we can determine if this record should be logged

        cmd =  f'/usr/bin/logger --server {LOGGING['server']} --port {LOGGING['port']} --udp {msg}'
        returned_output = subprocess.check_output(cmd)

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