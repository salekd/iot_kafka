import paho.mqtt.client as mqtt
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import json


# Schema of a plant monitor measurement
schema_str = """
{
   "namespace": "iot_kafka",
   "name": "value",
   "type": "record",
   "fields" : [
     {
       "name" : "device",
       "type" : "string"
     },
     {
       "name" : "timestamp",
       "type" : "string"
     },
     {
       "name" : "moisture",
       "type" : "int"
     },
     {
       "name" : "temperature",
       "type" : "float"
     },
     {
       "name" : "conductivity",
       "type" : "int"
     },
     {
       "name" : "light",
       "type" : "int"
     }
   ]
}
"""

value_schema = avro.loads(schema_str)
#value = {"moisture": 34, "timestamp": "2018-07-17 06:53:06.894367", "temperature": 25.9, "conductivity": 189, "device": "C4:7C:8D:65:BD:76", "light": 1460}

avroProducer = AvroProducer({
    'bootstrap.servers': '127.0.0.1:9092',
    'schema.registry.url': 'http://127.0.0.1:8081'
    }, default_value_schema=value_schema)


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    value = json.loads(str(msg.payload.decode("utf-8")))
    avroProducer.produce(topic='plant_monitor', value=value)
    avroProducer.flush()


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect("test.mosquitto.org", 1883, 60)
mqttc.subscribe("salekd/iot_kafka/plant_monitor", 0)

mqttc.loop_forever()
