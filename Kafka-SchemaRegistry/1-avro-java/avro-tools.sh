# put this in any directory you like
wget https://repo1.maven.org/maven2/org/apache/avro/avro-tools/1.11.4/avro-tools-1.11.4.jar

# run this from our project folder. Make sure ~/avro-tools-1.8.2.jar is your actual avro tools location
java -jar ~/avro-tools-1.8.2.jar tojson --pretty customer-generic.avro 
java -jar ~/avro-tools-1.8.2.jar tojson --pretty customer-specific.avro 

# getting the schema
java -jar ~/avro-tools-1.8.2.jar getschema customer-specific.avro 
