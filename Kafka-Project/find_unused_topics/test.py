from confluent_kafka.admin import AdminClient
from confluent_kafka import Consumer
from datetime import datetime, timedelta

kafka_config = {
    'bootstrap.servers': 'localhost:9092',  
    'group.id': 'topic_audit_group',
    'auto.offset.reset': 'earliest'
}

admin_client = AdminClient({'bootstrap.servers': 'localhost:9092'})

consumer = Consumer(kafka_config)

def list_all_topics():
    metadata = consumer.list_topics()
    return list(metadata.topics.keys())

def get_topic_end_offsets(topic):
    partitions = consumer.list_topics().topics[topic].partitions.keys()
    print(f'{topic}----{partitions}')
    #return {partition: consumer.get_watermark_offsets(consumer.assign([(topic, partition)]))[1] for partition in partitions}

def get_last_message_timestamp(topic):
    end_offsets = get_topic_end_offsets(topic)

def find_unused_topics():
    topics = list_all_topics()
    unused_topics = []
    thirty_days_ago = (datetime.now() - timedelta(days=30)).timestamp() * 1000

    for topic in topics:
        if topic.startswith("_"):
            continue
        else:
            last_timestamp = get_last_message_timestamp(topic)
    print(topics)

if __name__ == "__main__":
    unused_topics = find_unused_topics()
    # try:
    #     unused_topics = find_unused_topics()
    #     print("Topics not used in the last 30 days:")
    #     for topic in unused_topics:
    #         print(topic)
    # finally:
    #     consumer.close()