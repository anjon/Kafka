# create a topic with 3 partitions
kafka-topics --bootstrap-server broker1:19092 --topic second_topic --create --partitions 3

# consuming
kafka-console-consumer --bootstrap-server broker1:19092 --topic second_topic

# other terminal
kafka-console-producer --bootstrap-server broker1:19092 --producer-property partitioner.class=org.apache.kafka.clients.producer.RoundRobinPartitioner --topic second_topic

# Consume from Beginning
kafka-console-consumer --bootstrap-server broker1:19092 --topic second_topic --from-beginning

# Display key, values and timestamp in consumer
kafka-console-consumer --bootstrap-server broker1:19092 --topic second_topic --formatter kafka.tools.DefaultMessageFormatter --property print.timestamp=true --property print.key=true --property print.value=true --property print.partition=true --from-beginning