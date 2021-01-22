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

try:
    import latency_loss_logging_constants
except ImportError:
    print('Could not import constants!')


def get_devices(dashboard, firewalls=MERAKI['firewalls']):
    """ 
        Identify firewall device types of interest
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

def get_stats(dashboard, devices, target=MERAKI['target'], timespan=MERAKI['timespan'], uplink=MERAKI['uplink']):

    for device in get_devices(dashboard):
        print(device)
        mgmt = dashboard.devices.getDeviceManagementInterface(device['serial'])
        print(mgmt['ddnsHostnames'])
        response = dashboard.devices.getDeviceLossAndLatencyHistory(device['serial'], target, 
                                                                    timespan=timespan, uplink=uplink)
        for item in response:
            print(item)

def main():

    
    if os.getenv('MERAKI_DASHBOARD_API_KEY', None):
        dashboard = meraki.DashboardAPI(output_log=False)     
    else:
        # by default, the API looks for the API key in environment variable MERAKI_DASHBOARD_API_KEY
        print('please create and specify the API key, e.g. "export MERAKI_DASHBOARD_API_KEY=12345"')

    get_stats(dashboard, get_devices(dashboard))

    # `logger --server LOGGING['server'] --port LOGGING['port'] --udp "Hello world"`


if __name__ == '__main__':
    main()