# create a topic with 3 partitions
kafka-topics --bootstrap-server broker1:19092 --topic third_topic --create --partitions 3

# start one consumer
kafka-console-consumer --bootstrap-server broker1:19092 --topic third_topic --group my-first-application

# start one producer and start producing
kafka-console-producer --bootstrap-server broker1:19092 --producer-property partitioner.class=org.apache.kafka.clients.producer.RoundRobinPartitioner --topic third_topic

# start another consumer part of the same group. See messages being spread
kafka-console-consumer --bootstrap-server broker1:19092 --topic third_topic --group my-first-application

# start another consumer part of a different group from beginning
kafka-console-consumer --bootstrap-server broker1:19092 --topic third_topic --group my-second-application --from-beginning