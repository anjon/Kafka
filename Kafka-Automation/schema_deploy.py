#!/usr/bin/env python3

import os
import json
import requests


def load_avro_data(schemadata):
    schema_file_path = os.path.join("Data", schemadata)
    with open(schema_file_path, 'r') as read_schema:
        schemafile = json.loads(read_schema.read())
        print(schemafile) 
    return schemafile

def register_schema(schemafile):
    base_uri = "http://localhost:8081"

    register_request = requests.post(url=f'{base_uri}/subjects/sensor-value/versions',
                data=json.dumps({'schema': json.dumps(schemafile)}),
                headers={'Content-Type': 'application/vnd.schemaregistry.v1+json'}).json()
    return register_request

def schema_comatibility():
    pass

def delete_schema():
    pass

if __name__ == "__main__":
    with open('Schema.config') as all_schemas:
        for schema in all_schemas:
            singleSchema = schema.split(":")
            print(singleSchema)
            print(f"Operation : {singleSchema[0]}, Avro File: {singleSchema[1]}, Schema Subject: {singleSchema[2]}, Compatibility: {singleSchema[3]}")
            if singleSchema[0] == "[+]":
                print("Schema load, register, compatibility operation")
                load_avro_data(singleSchema[1])
            if singleSchema[0] == "[-]":
                print("Schema delete operation")
                load_avro_data(singleSchema[1])
            