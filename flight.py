
from pykafka import KafkaClient
client = KafkaClient(hosts="localhost:9092")
for i in client.topics['flightdata'].get_simple_consumer():
    print('data:{0}\n\n'.format(i.value.decode()))