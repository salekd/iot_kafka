#!/bin/bash
# https://docs.confluent.io/current/kafka-rest/docs/intro.html

curl -X POST -H "Content-Type: application/vnd.kafka.avro.v2+json" \
-H "Accept: application/vnd.kafka.v2+json" \
--data '{
   "value_schema": "{\"type\": \"record\", \"name\": \"measurements\", \"fields\": [{\"name\": \"temperature\", \"type\": \"int\"}]}",
   "records": [
     {"value": {"temperature": 42}},
     {"value": {"temperature": 42}}
   ]
}' \
http://localhost:8082/topics/avrotest

curl -X POST -H "Content-Type: application/vnd.kafka.v2+json" \
--data '{"name": "my_consumer_instance", "format": "avro", "auto.offset.reset": "earliest"}' \
http://localhost:8082/consumers/my_avro_consumer

curl -X POST -H "Content-Type: application/vnd.kafka.v2+json" --data '{"topics":["avrotest"]}' \
http://localhost:8082/consumers/my_avro_consumer/instances/my_consumer_instance/subscription

curl -X GET -H "Accept: application/vnd.kafka.avro.v2+json" \
http://localhost:8082/consumers/my_avro_consumer/instances/my_consumer_instance/records

curl -X DELETE -H "Content-Type: application/vnd.kafka.v2+json" \
http://localhost:8082/consumers/my_avro_consumer/instances/my_consumer_instance

#curl http://localhost:8082/topics/avrotest
curl http://localhost:8082/topics/avrotest | jq .

curl http://localhost:8082/topics/avrotest/partitions
