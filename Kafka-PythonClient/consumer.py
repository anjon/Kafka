from kafka import KafkaConsumer
import json

if __name__ == "__main__":
    consumer = KafkaConsumer(
        "registered_user",
        bootstrap_servers='broker1:19092',
        auto_offset_reset='earliest',
        group_id="consumer-group-a")
    print("Starting the Consumer")
    for msg in consumer:
        print("Registered User = {}".format(json.loads(msg.value)))