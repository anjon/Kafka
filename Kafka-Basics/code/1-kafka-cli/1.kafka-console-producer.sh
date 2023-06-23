# Creating topics for producing
kafka-topics --bootstrap-server broker1:19092 --topic first_topic --create --partitions 1

# Producing
kafka-console-producer --bootstrap-server broker1:19092 --topic first_topic 

# Producing with properties
kafka-console-producer --bootstrap-server broker1:19092 --topic first_topic --producer-property acks=all

# producing to a non existing topic
kafka-console-producer --bootstrap-server broker1:19092 --topic new_topic

# our new topic only has 1 partition
kafka-topics --bootstrap-server broker1:19092 --list
kafka-topics --bootstrap-server broker1:19092 --topic new_topic --describe


# edit config/server.properties or config/kraft/server.properties
# num.partitions=3

# produce against a non existing topic again
kafka-console-producer --bootstrap-server broker1:19092 --topic new_topic_2
hello again!

# this time our topic has 3 partitions
kafka-topics --bootstrap-server broker1:19092 --list
kafka-topics --bootstrap-server broker1:19092 --topic new_topic_2 --describe

# overall, please create topics with the appropriate number of partitions before producing to them!


# produce with keys
kafka-console-producer --bootstrap-server broker1:19092 --topic first_topic --property parse.key=true --property key.separator=:
>example key:example value
>name:Stephane