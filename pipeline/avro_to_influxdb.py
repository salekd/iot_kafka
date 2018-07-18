from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from influxdb import InfluxDBClient


client = InfluxDBClient("localhost", 8086, "admin", "admin")

client.create_database("plant_monitor")
client.switch_database("plant_monitor")

c = AvroConsumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'groupid',
    'schema.registry.url': 'http://localhost:8081'})

c.subscribe(['plant_monitor'])

try:
    while True:
        try:
            msg = c.poll(10)

        except SerializerError as e:
            print("Message deserialization failed for {}: {}".format(msg, e))
            break

        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        print(msg.value())
        measurement = msg.value()
        json_body =\
            [
                {
                    "measurement": "miflora",
                    "tags": {
                        "device": measurement["device"]
                    },
                    "fields": {
                        "mositure": measurement["moisture"],
                        "temperature": measurement["temperature"],
                        "conductivity": measurement["conductivity"],
                        "light": measurement["light"],
                        "timestamp": measurement["timestamp"]
                    }
                }
            ]

        client.write_points(json_body)

except KeyboardInterrupt:
    pass

finally:
    c.close()
