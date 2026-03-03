# Kafka Python Producer with Avro & Schema Registry

This project demonstrates a complete end-to-end Kafka producer workflow using Python.  
It includes:

- Automated Kafka topic creation
- Avro schema management and Schema Registry integration
- A Python producer using Avro serialization
- Deterministic partition routing using country-based message keys
- Fetching and transforming real user data from an external API
---

## Features
- Create Kafka topics programmatically  
- Automatically register Avro schemas  
- Serialize messages using Avro  
- Route messages to partitions based on keys  
- Use real-world random user API data  
---

## Project Structure
```
producer/
│── main.py                # Entry point for the full workflow
│── topic_manager.py       # Kafka topic creation logic
│── schema_manager.py      # Avro schema registration logic
│── producer_service.py    # Kafka producer logic & message serialization
│── user.avsc              # Avro schema definition for user messages
```
---

## Prerequisites
- Python 3.13.X+
- Kafka Cluster
- Schema Registry
---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/anjon/Kafka.git
cd Kafka/Kafka-PythonClient/producer
```

### 2. Install dependencies
```bash
pip install confluent-kafka[avro,schemaregistry] requests fastavro
```

### 3. Create a virtual environment (Optional)
```bash
python -m venv venv
source venv/bin/activate
```
---

## How the System Works

### Step 1 — Topic Creation

`topic_manager.py` ensures the Kafka topic exists.  
If it doesn't, the script creates it with the required number of partitions.

### Step 2 — Schema Registration

`schema_manager.py` loads the Avro schema from `user.avsc` and registers it with the Schema Registry.  
The returned schema ID is used by the producer.

### Step 3 — Message Production

`producer_service.py`:
1. Fetches random user data from an API  
2. Converts it to match the Avro schema  
3. Selects a partition based on the country key  
4. Sends the Avro-serialized message to Kafka  
5. Logs the delivery result  
---

## Avro Schema
The `user.avsc` file describes the structure of messages produced.  
It includes fields such as name, address, gender, email, phone, and country.

---

## Partition Strategy

### Default Kafka Behavior (Without Custom Routing)

If you assign a **key** but do **not** specify a partition:

- Kafka hashes the key  
- Uses: `hash(key) % number_of_partitions`
- Same key always goes to the same partition
- Ensures ordering per key  
- But you do NOT control which partition it lands in  
  (only that it stays consistent)

### Custom Routing Logic (Your Implementation)

Your code maps specific countries to predefined partitions:

```
COUNTRY_PARTITION_MAP = {
    "AU": 0, "BR": 1, "CA": 2, "DK": 3,
    "FR": 4, "GB": 5, "NZ": 6, "US": 7
}
```
This gives:

- Complete control over partition assignment  
- Predictable, non-hash-based routing  
- Stability even if partition count changes  
- Ability to meet business or geographic routing needs  

### Why Custom Routing May Be Useful

- Ensures balanced load  
- Enforces geographic partitioning  
- Prevents rebalancing issues when partitions are added  
- Supports compliance or data locality requirements  
---

## Running the Application
Start Kafka, Zookeeper, and Schema Registry.  
Then run:

```bash
python main.py
```

Expected output:
```
Created topic 'kafka_users_topic'
Registered schema under subject kafka_users_topic-value
Producing 100 user records...
Delivered record to topic 'kafka_users_topic' partition 3 offset 42 (key=US)
```
---

## Useful Kafka Commands

### List Topics

```bash
kafka-topics.sh --list --bootstrap-server localhost:9092
```

### Consume Messages
```bash
kafka-console-consumer.sh   --bootstrap-server localhost:9092   --topic kafka_users_topic   --from-beginning   --property print.key=true   --property print.partition=true
```
---