# Examples

### MQTT

```
/usr/local/sbin/mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf
mosquitto_sub -t sensor/temperature
mosquitto_pub -t sensor/temperature -m 42
```

The example MQTT subscriber is taken from https://github.com/eclipse/paho.mqtt.python/blob/master/examples/client_sub.py



***
### Kafka

```
confluent start
```

The example producers and consumers are taken from
https://www.confluent.io/blog/introduction-to-apache-kafka-for-python-programmers/
and
https://github.com/confluentinc/confluent-kafka-python

The example using the REST Proxy is taken from
https://docs.confluent.io/current/kafka-rest/docs/intro.html



***
### InfluxDB

```
influxd -config /usr/local/etc/influxdb.conf
```

