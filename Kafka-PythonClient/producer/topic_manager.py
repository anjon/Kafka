import logging
from confluent_kafka.admin import AdminClient, NewTopic


class TopicManager:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.admin_client = AdminClient({"bootstrap.servers": bootstrap_servers})
        self.logger = logging.getLogger("TopicManager")

    def create_topic(self, topic_name: str, num_partitions: int = 1, replication_factor: int = 1):
        self.logger.info(f"Checking if topic '{topic_name}' exists...")

        md = self.admin_client.list_topics(timeout=5)

        if topic_name in md.topics:
            self.logger.info(f"Topic '{topic_name}' already exists.")
            return

        new_topic = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
        fs = self.admin_client.create_topics([new_topic])

        for topic, future in fs.items():
            try:
                future.result()
                self.logger.info(f"Topic '{topic}' successfully created.")
            except Exception as e:
                self.logger.error(f"Failed to create topic '{topic}': {e}")