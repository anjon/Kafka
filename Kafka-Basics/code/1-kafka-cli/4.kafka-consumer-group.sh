# documentation for the command 
kafka-consumer-groups 

# list consumer groups
kafka-consumer-groups --bootstrap-server broker1:19092 --list
 
# describe one specific group
kafka-consumer-groups --bootstrap-server broker1:19092 --describe --group my-second-application

# describe another group
kafka-consumer-groups --bootstrap-server broker1:19092 --describe --group my-first-application

# start a consumer
kafka-console-consumer --bootstrap-server broker1:19092 --topic first_topic --group my-first-application

# describe the group now
kafka-consumer-groups --bootstrap-server broker1:19092 --describe --group my-first-application

# describe a console consumer group (change the end number)
kafka-consumer-groups --bootstrap-server broker1:19092 --describe --group console-consumer-10592

# start a console consumer
kafka-console-consumer --bootstrap-server broker1:19092 --topic first_topic --group my-first-application

# describe the group again
kafka-consumer-groups --bootstrap-server broker1:19092 --describe --group my-first-application