# List & Create Topics 
kafka-topics --bootstrap-server broker1:19092 --list 
kafka-topics --bootstrap-server broker1:19092 --topic first_topic --create
kafka-topics --bootstrap-server broker1:19092 --topic second_topic --create --partitions 3
kafka-topics --bootstrap-server broker1:19092 --topic third_topic --create --partitions 3 --replication-factor 2

# Create a topic (working)
kafka-topics --bootstrap-server broker1:19092 --topic third_topic --create --partitions 3 --replication-factor 1

# List topics
kafka-topics --bootstrap-server broker1:19092 --list 

# Describe a topic
kafka-topics --bootstrap-server broker1:19092 --topic first_topic --describe

# Delete a topic 
kafka-topics --bootstrap-server broker1:19092 --topic first_topic --delete
# (only works if delete.topic.enable=true)