
from latency_loss_logging_constants import CLIENT_CONF
from confluent_kafka import avro, KafkaError

from confluent_kafka import Consumer


CLIENT_CONF['group.id'] = 'python_example_group_1'
CLIENT_CONF['auto.offset.reset'] = 'earliest'

consumer = Consumer(CLIENT_CONF)
consumer.subscribe(['topic_0'])

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        print("Waiting for message or event/error in poll()")
        continue
    elif msg.error():
        print('error: {}'.format(msg.error()))
    else:
                # Check for Kafka message
        record_key = msg.key()
        record_value = msg.value()
        
consumer.close()