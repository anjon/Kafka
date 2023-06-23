# look at the documentation again
kafka-consumer-groups

# describe the consumer group
kafka-consumer-groups --bootstrap-server broker1:19092 --describe --group my-first-application

# Dry Run: reset the offsets to the beginning of each partition
kafka-consumer-groups --bootstrap-server broker1:19092 --group my-first-application --reset-offsets --to-earliest --topic third_topic --dry-run

# execute flag is needed
kafka-consumer-groups --bootstrap-server broker1:19092 --group my-first-application --reset-offsets --to-earliest --topic third_topic --execute

# describe the consumer group again
kafka-consumer-groups --bootstrap-server broker1:19092 --describe --group my-first-application

# consume from where the offsets have been reset
kafka-console-consumer --bootstrap-server broker1:19092 --topic third_topic --group my-first-application

# describe the group again
kafka-consumer-groups --bootstrap-server broker1:19092 --describe --group my-first-application