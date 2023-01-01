
from latency_loss_logging_constants import CONSUMER_CONF
from confluent_kafka import avro, KafkaError

from confluent_kafka import Consumer


CONSUMER_CONF['group.id'] = 'python_example_group_1'
CONSUMER_CONF['auto.offset.reset'] = 'earliest'

consumer = Consumer(CONSUMER_CONF)
consumer.subscribe(['topic_0'])

while True:
    msg = consumer.poll(2.0)
    if msg is None:
        print("Waiting for message or event/error in poll()")
        continue
    elif msg.error():
        print('error: {}'.format(msg.error()))
    else:
                # Check for Kafka message
        record_key = msg.key()
        record_value = msg.value()
        print(f'offset:{msg.offset()} partition:{msg.partition()} {record_key} {record_value}')
        break
        
# consumer.close()