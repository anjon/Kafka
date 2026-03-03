import logging
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.schema_registry_client import Schema

class SchemaManager:
    def __init__(self, schema_registry_url: str):
        self.schema_registry_url = schema_registry_url
        self.client = SchemaRegistryClient({"url": schema_registry_url})
        self.logger = logging.getLogger("SchemaManager")

    def register_avro_schema(self, subject_name: str, schema_file_path: str):
        self.logger.info(f"Reading schema from {schema_file_path}")

        with open(schema_file_path, "r") as f:
            schema_str = f.read()

        schema = Schema(schema_str, schema_type="AVRO")

        self.logger.info(f"Registering schema for subject '{subject_name}'...")

        try:
            schema_id = self.client.register_schema(subject_name, schema)
            self.logger.info(f"Schema registered successfully with ID: {schema_id}")
            return schema_str
        except Exception as e:
            self.logger.error(f"Failed to register schema: {e}")
            raise