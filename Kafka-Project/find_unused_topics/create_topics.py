import json, csv, random, uuid, time
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer
from faker import Faker

# Kafka broker configuration
bootstrap_servers = "localhost:29092, localhost:39092, localhost:49092"

# Initialize Kafka Producer
producer = Producer({'bootstrap.servers': bootstrap_servers})

# Initialize Kafka AdminClient
admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})

# Callback function to check message delivery status
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def check_topic_exists(topic_name):
    """Check if a Kafka topic already exists."""
    # Fetch metadata for all topics
    cluster_metadata = admin_client.list_topics(timeout=10)
    return topic_name in cluster_metadata.topics

def create_topics_from_csv(csv_file):
    """Create Kafka topics from a CSV file if they don't already exist."""
    # Read topics from CSV file
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            topics = [
                NewTopic(
                    topic=row['topic_name'],
                    num_partitions=int(row['partitions']),
                    replication_factor=int(row['replication_factor'])
                )
                for row in reader
            ]
    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found.")
        exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        exit(1)

    # Create topics if they don't already exist
    if topics:
        for topic in topics:
            if check_topic_exists(topic.topic):
                print(f"Topic {topic.topic} already exists. Skipping creation.")
            else:
                # Create the topic
                fs = admin_client.create_topics([topic])
                for topic_name, future in fs.items():
                    try:
                        future.result()  # Wait for the topic to be created
                        print(f"Topic {topic_name} created successfully.")
                    except Exception as e:
                        print(f"Failed to create topic {topic_name}: {e}")
    else:
        print("No topics found in the CSV file.")

def generate_transaction():
    return dict(
        transactionId = str(uuid.uuid4()),
        userId = f"user_{random.randint(1, 100)}",
        amount = round(random.uniform(50000, 150000), 2),
        transactionTime = int(time.time()),
        merchantId = random.choice(['merchant_1', 'merchant_2', 'merchant_3']),
        transactionType = random.choice(['purchase', 'refund']),
        location = f"Location {random.randint(1, 50)}",
        paymentMethod = random.choice(['credit_card', 'paypal', 'bank_transfer', 'blik']),
        isInternational = random.choice(['True', 'False']),
        currency = random.choice(['USD', 'EURO', 'PLN'])
    )

def produce_random_messages(csv_file):
    """Produce 100 random messages to each topic listed in the CSV file."""
    # Read topics from CSV file
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            topics = [row['topic_name'] for row in reader]
    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found.")
        exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        exit(1)

    # Produce 100 random messages to each topic
    for topic in topics:
        print(f"Producing messages to topic: {topic}")
        for _ in range(100):
            # Generate a random message using Faker
            message = generate_transaction()
            
            # Produce the message to the Kafka topic
            try:
                producer.produce(
                    topic=topic,
                    key=message['userId'],
                    value=json.dumps(message).encode('utf-8'),
                    on_delivery=delivery_report
                )
                print(f"Produce message - {message} to the topic {topic}")
                time.sleep(0.1)
            except Exception as e:
                print(f"Error sending transaction: {e}")
            
            # Poll for events to trigger the callback
            producer.poll(0)

        # Wait for all messages to be delivered
        producer.flush()
        print(f"Finished producing messages to topic: {topic}")

    print("All messages produced successfully.")

if __name__ == "__main__":
    # Path to the CSV file containing topic configurations
    csv_file = 'topics.csv'  # Replace with your CSV file path

    # Step 1: Create topics from the CSV file (if they don't already exist)
    print("Creating topics...")
    create_topics_from_csv(csv_file)

    # Step 2: Produce random messages to the topics
    print("Producing messages...")
    produce_random_messages(csv_file)