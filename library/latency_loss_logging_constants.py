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
    
import os
# Define Kafka configuration
PRODUCER_CONF = {
            'bootstrap.servers': os.environ.get('BOOTSTRAP_SERVER'),
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': os.environ.get('CLUSTER_API_KEY'),
            'sasl.password': os.environ.get('CLUSTER_API_SECRET')
}
CONSUMER_CONF = PRODUCER_CONF

# Define Confluent Cloud Schema Registry
SCHEMA_CONF = {
          'schema.registry.url': os.environ.get('SR_URL'),
          'basic.auth.credentials.source': 'USER_INFO',
          'basic.auth.user.info': '{}:{}'.format(os.environ.get('SR_API_KEY'), os.environ.get('SR_API_SECRET'))
}