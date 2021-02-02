#
#
# By default, the API looks for the API key in environment variable MERAKI_DASHBOARD_API_KEY
#
#  You want to export MERAKI_DASHBOARD_API_KEY=12345
#
MERAKI = dict(
    target='8.8.8.8',
    firewalls=('MX64',),
    timespan=119,
    uplink='wan1'
    )

LOGGING = dict(
    server='3.238.50.209',
    port='514',
    debug=True
    )