# Examples

### MQTT

```
/usr/local/sbin/mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf
mosquitto_sub -t sensor/temperature
mosquitto_pub -t sensor/temperature -m 42
```



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
