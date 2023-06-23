# To get the kafka cluster version 
kafka-broker-api-versions --bootstrap-server broker1:19092 --version

# To get the cluster id
zookeeper-shell zk1:22181 get /cluster/id

# Create a Partitions
kafka-topics --bootstrap-server broker1:19092 --partitions 3 --replication-factor 3 --topic bcm_test_topic_1 --create

# Describe the details of about the partions
kafka-topics --bootstrap-server broker1:19092 --topic bcm_test_topic_1 --describe

# Modify the partition after the creation 
kafka-topics --bootstrap-server broker1:19092 --alter --topic bcm_test_topic_1 --partitions 6

# Increase the replication factor of the partitions
kafka-topics --bootstrap-server broker1:19092 --partitions 3 --replication-factor 1 --topic bcm_test_topic_1 --create

vim increase-replication-factor.json
{"version":1,
  "partitions":[
     {"topic":"bcm_test_topic_1","partition":0,"replicas":[0,1,2]},
     {"topic":"bcm_test_topic_1","partition":1,"replicas":[0,1,2]},
     {"topic":"bcm_test_topic_1","partition":2,"replicas":[0,1,2]}
]}

kafka-reassign-partitions.sh --bootstrap-server broker1:19092,broker2:29092,broker2:39092 --reassignment-json-file  increase-replication-factor.json --execute