import time
import requests
import logging
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry.avro import AvroSerializer

# Same mapping as before
COUNTRY_PARTITION_MAP = {
    "AU": 0, "BR": 1, "CA": 2, "DK": 3,
    "FR": 4, "GB": 5, "NZ": 6, "US": 7
}

API_URL = "https://randomuser.me/api/?nat=au,br,ca,dk,fr,gb,nz,us"

logger = logging.getLogger("kafka-producer")


class ProducerService:

    def __init__(self, bootstrap_servers, schema_registry_client, schema_str, topic_name):
        self.topic_name = topic_name
        self.schema_registry_client = schema_registry_client

        # Create Avro serializer
        self.value_serializer = AvroSerializer(
            schema_registry_client=self.schema_registry_client,
            schema_str=schema_str
        )

        # Producer config
        self.producer = SerializingProducer({
            "bootstrap.servers": bootstrap_servers,
            "key.serializer": StringSerializer("utf_8"),
            "value.serializer": self.value_serializer,
            "enable.idempotence": True,
            "acks": "all"
        })

    # -----------------------------
    # Helper: Delivery report
    # -----------------------------
    @staticmethod
    def delivery_report(err, msg):
        if err is not None:
            logger.error(f"Delivery failed: {err}")
        else:
            logger.info(
                f"Message delivered to {msg.topic()} "
                f"[partition={msg.partition()} offset={msg.offset()}] "
                f"key={msg.key().decode('utf-8')}"
            )

    # -----------------------------
    # Helper: Fetch user from API
    # -----------------------------
    @staticmethod
    def fetch_random_user():
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            return response.json()["results"][0]
        except Exception as e:
            logger.error(f"API request failed: {e}")
            return None

    # -----------------------------
    # Helper: Format user data
    # -----------------------------
    @staticmethod
    def format_user(user):
        loc = user["location"]
        return {
            "first_name": user["name"]["first"],
            "last_name": user["name"]["last"],
            "gender": user["gender"],
            "address": f"{loc['street']['number']} {loc['street']['name']}, "
                       f"{loc['city']}, {loc['state']}, {loc['country']}",
            "post_code": str(loc["postcode"]),
            "email": user["email"],
            "username": user["login"]["username"],
            "dob": user["dob"]["date"],
            "registered_date": user["registered"]["date"],
            "phone": user["phone"],
            "picture": user["picture"]["medium"],
            "country": loc["country"],
            "nat": user["nat"]
        }

    # -----------------------------
    # ⭐ PRODUCE ~50 MESSAGES ⭐
    # -----------------------------
    def produce_messages(self, count=50):

        logger.info(f"Starting to produce {count} messages...")

        for i in range(count):
            try:
                raw = self.fetch_random_user()
                if raw is None:
                    continue

                formatted = self.format_user(raw)

                nat_code = formatted["nat"].upper()
                partition = COUNTRY_PARTITION_MAP.get(nat_code, 0)

                key = formatted["country"]

                self.producer.produce(
                    topic=self.topic_name,
                    key=key,
                    value=formatted,
                    partition=partition,
                    on_delivery=self.delivery_report
                )

                self.producer.poll(0)

                if (i + 1) % 10 == 0:
                    logger.info(
                        f"Sent {i + 1}/{count} messages. "
                        f"Last was {nat_code} -> Partition {partition}"
                    )

                time.sleep(0.5)

            except Exception as e:
                logger.error(f"Failed to produce message {i}: {e}")

        self.producer.flush()
        logger.info("Finished producing all messages.")