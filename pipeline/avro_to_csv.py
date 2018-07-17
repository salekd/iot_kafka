from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
import pathlib


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

        # Append to a csv file for the device
        csv_path = pathlib.Path(__file__).parent / 'plant_monitor.csv'
        with csv_path.open('a') as csvfile:
            # Make sure the entries are in the correct order
            csvfile.write("{}, {}, {}, {:.2f}, {}, {}\n".format(measurement["timestamp"], measurement['device'],
                measurement["moisture"], measurement["temperature"], measurement["conductivity"], measurement["light"]))

except KeyboardInterrupt:
    pass

finally:
    c.close()
