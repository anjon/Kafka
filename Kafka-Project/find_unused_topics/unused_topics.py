from confluent_kafka import Consumer, KafkaException, KafkaError, AdminClient
import time
from datetime import datetime, timedelta

# Kafka broker configuration
conf = {
    'bootstrap.servers': 'localhost:9092',  
    'group.id': 'topic_audit_group',
    'auto.offset.reset': 'earliest'
}

# Create AdminClient
admin_client = AdminClient(conf)

# Create Consumer
consumer = Consumer(conf)

def list_all_topics():
    """List all topics in the Kafka cluster."""
    metadata = consumer.list_topics()
    return metadata.topics.keys()

def get_topic_end_offsets(topic):
    """Get the end offsets for all partitions of a topic."""
    partitions = consumer.list_topics().topics[topic].partitions.keys()
    return {partition: consumer.get_watermark_offsets(consumer.assign([(topic, partition)]))[1] for partition in partitions}

def get_last_message_timestamp(topic):
    """Get the timestamp of the last message in a topic."""
    end_offsets = get_topic_end_offsets(topic)
    last_timestamp = 0

    for partition, offset in end_offsets.items():
        if offset == 0:
            continue  # Skip partitions with no messages

        # Seek to the last message in the partition
        consumer.assign([(topic, partition)])
        consumer.seek((topic, partition, offset - 1))

        msg = consumer.poll(timeout=10.0)
        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                raise KafkaException(msg.error())

        last_timestamp = max(last_timestamp, msg.timestamp()[1])

    return last_timestamp

def find_unused_topics():
    """Find topics that have not been used in the last 30 days."""
    topics = list_all_topics()
    unused_topics = []
    thirty_days_ago = (datetime.now() - timedelta(days=30)).timestamp() * 1000

    for topic in topics:
        last_timestamp = get_last_message_timestamp(topic)
        if last_timestamp < thirty_days_ago:
            unused_topics.append(topic)

    return unused_topics

if __name__ == "__main__":
    try:
        unused_topics = find_unused_topics()
        print("Topics not used in the last 30 days:")
        for topic in unused_topics:
            print(topic)
    finally:
        consumer.close()