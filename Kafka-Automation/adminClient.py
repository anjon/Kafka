#!/usr/bin/env python3

from confluent_kafka.admin import AdminClient, NewTopic

def create_topics_if_not_exist(bootstrap_servers, topics):
    admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})

    # Fetch the cluster metadata to get the list of existing topics
    metadata = admin_client.list_topics(timeout=10)
    existing_topics = metadata.topics

    # List of new topics to be created
    new_topics = []

    for topic_name, num_partitions, replication_factor in topics:
        if topic_name in existing_topics:
            print(f"Topic '{topic_name}' already exists.")
        else:
            new_topic = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
            new_topics.append(new_topic)
    
    if new_topics:
        # Try to create the new topics
        fs = admin_client.create_topics(new_topics)
        
        # Wait for operation to finish
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                print(f"Topic '{topic}' created successfully.")
            except Exception as e:
                print(f"Failed to create topic '{topic}': {e}")
    else:
        print("No new topics to create.")

if __name__ == "__main__":
    bootstrap_servers = 'localhost:9092'
    topics_to_create = [
        ('topic1', 3, 1),
        ('topic2', 2, 1),
        ('topic3', 1, 1)
    ]

    create_topics_if_not_exist(bootstrap_servers, topics_to_create)
