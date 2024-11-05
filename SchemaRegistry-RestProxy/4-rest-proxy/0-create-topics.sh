kafka-topics --create --zookeeper localhost:2181 --topic rest-binary --replication-factor 1 --partitions 1
kafka-topics --create --zookeeper localhost:2181 --topic rest-json --replication-factor 1 --partitions 1
kafka-topics --create --zookeeper localhost:2181 --topic rest-avro --replication-factor 1 --partitions 1

# List topics using rest proxy
http://localhost:8082/topics/
Accept: application/vnd.kafka.v2+json

http://localhost:8082/topics/_schemas
Accept: application/vnd.kafka.v2+json

# Producer : Binary Posting to a topics (POST Request)
http://localhost:8082/topics/rest-binary

Content-Type : application/vnd.kafka.binary.v2+json
Accept       : application/vnd.kafka.v2+json, application/vnd.kafka+json, application/json
{
  "records": [
    {
      "key": "a2V5",
      "value": "SGVsbG8gV29ybGQ="
    },
    {
      "value": "a2Fma2E=",
      "partition": 0
    },
    {
      "value": "UmVzdC1Qcm94eQ=="
    }
  ]
}

# Consume data using rest proxy
Steps:
  - Create a consumer group
  - Subscribe to a topic(or topic list)
  - Get records
  - Process records(your app)
  - Commit offsets (Once in a while)


# Step-01: Consume topics data using kafka rest proxy (POST Request)
http://localhost:8082/consumers/my-consumer-group
Content-Type : application/vnd.kafka.v2+json
{
    "name": "my_consumer_binary",
    "format": "binary",
    "auto.offset.reset": "earliest",
    "auto.commit.enable": "false"
}
# and got the return value
{
    "instance_id": "my_consumer_binary",
    "base_uri": "http://localhost:8082/consumers/my-consumer-group/instances/my_consumer_binary"
}

# Step-02: Subscibe consumer group to the topics  (POST Request)
http://localhost:8082/consumers/my-consumer-group/instances/my_consumer_binary/subscription
Content-Type: application/vnd.kafka.v2+json
{
  "topics": [
    "rest-binary"
  ]
}

# Step-03: Get records (GET Request)
http://localhost:8082/consumers/my_consumer_binary/instances/my_consumer_binary/records?timeout=3000&max_bytes=300000
Accept: application/vnd.kafka.binary.v2+json
[
    {
        "topic": "rest-binary",
        "key": "a2V5",
        "value": "SGVsbG8gV29ybGQ=",
        "partition": 0,
        "offset": 0
    },
    {
        "topic": "rest-binary",
        "key": null,
        "value": "a2Fma2E=",
        "partition": 0,
        "offset": 1
    },
    {
        "topic": "rest-binary",
        "key": null,
        "value": "UmVzdC1Qcm94eQ==",
        "partition": 0,
        "offset": 2
    }
]
# Step-04: Commiting offsets (POST)
http://localhost:8082/consumers/my-consumer-group/instances/my_consumer_binary/offsets
Content-Type: application/vnd.kafka.v2+json
{
    "offsets": [
        {
            "topic": "rest-binary",
            "partition": 0,
            "offset": 2
        }
    ]
}
