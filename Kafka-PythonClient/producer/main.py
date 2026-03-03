import logging
from topic_manager import TopicManager
from schema_manager import SchemaManager
from producer_service import ProducerService

# ------------------------------------------------
# Logging Setup (same as you requested)
# ------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("producer.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("MainApp")

# ------------------------------------------------
# Main Application
# ------------------------------------------------
def main():
    bootstrap_servers = "localhost:9092"
    schema_registry_url = "http://localhost:8081"
    topic_name = "kafka_users_topic"
    schema_subject = f"{topic_name}-value"
    schema_file = "user.avsc"

    logger.info("Starting Kafka Producer Application...")

    # 1. Create topic
    topic_manager = TopicManager(bootstrap_servers)
    topic_manager.create_topic(topic_name, num_partitions=8, replication_factor=1)

    # 2. Register schema
    schema_manager = SchemaManager(schema_registry_url)
    schema_str = schema_manager.register_avro_schema(schema_subject, schema_file)

    # 3. Create producer
    producer_service = ProducerService(
        bootstrap_servers=bootstrap_servers,
        schema_registry_client=schema_manager.client,
        schema_str=schema_str,
        topic_name=topic_name
    )

    producer_service.produce_messages(100)


if __name__ == "__main__":
    main()