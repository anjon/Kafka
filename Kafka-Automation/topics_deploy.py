#!/usr/bin/env python3

import sys

def topic_exists(name):
    
    pass

def create_topics(name,partition,rf,rp):
    print(f"Topic Name: {name}, Partition: {partition}, Replication Factor: {rf}, Retention Period: {rp}")

def delete_topic(name):
    print(f"Topic Name: {name}")

if __name__ == "__main__":

    with open('topics.config','r') as topics_file:
        for topic in topics_file:
            if topic.startswith("[+]"):
                ingrediants = topic.split(':')
                if topic_exists(ingrediants[1]):
                    raise Exception (f"Topic {ingrediants[1]} Already Exists")
                else:    
                    create_topics(ingrediants[1],ingrediants[2],ingrediants[3],ingrediants[4]) 
            if topic.startswith("[-]"):
                ingrediants = topic.split(':')
                delete_topic(ingrediants[1])
