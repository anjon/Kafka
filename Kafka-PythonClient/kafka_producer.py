import json
import socket
import time
import requests
from confluent_kafka import Producer


def get_user_data():
    user = requests.get('https://randomuser.me/api/').json()['results'][0]
    # print(json.dumps(user, indent=3,ensure_ascii=False))
    return user


def format_data(user):
    data = {}
    location = user['location']
    # data['id'] = uuid.uuid4()
    data['first_name'] = user['name']['first']
    data['last_name'] = user['name']['last']
    data['gender'] = user['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = user['email']
    data['username'] = user['login']['username']
    data['dob'] = user['dob']['date']
    data['registered_date'] = user['registered']['date']
    data['phone'] = user['phone']
    data['picture'] = user['picture']['medium']

    return data


def stream_data():
    conf = {'bootstrap.servers': '',
            'security.protocol': '',
            'sasl.mechanism': '',
            'sasl.username': '',
            'sasl.password': '',
            'client.id': socket.gethostname()}
    producer = Producer(conf)

    for i in range(1,10):
        try:
            # Generating the User data
            user_data = get_user_data()
            time.sleep(1)

            # Formatting User data
            kafka_message = format_data(user_data)
            time.sleep(1)

            producer.produce('test-topic-02', json.dumps(kafka_message).encode('utf-8'))
            print(f"Message {i} produced successfully !")
        except Exception as e:
            print(f"Error producing message: {e}")
        finally:
            producer.flush()


if __name__ == "__main__":
    # Stream messages to kafka topics
    stream_data()
