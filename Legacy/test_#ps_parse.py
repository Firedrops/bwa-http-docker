import argparse
import base64
import json
import re
import socket
import sys
import time

from google.cloud import pubsub_v1

def summarize(message):
    # [START parse_message]
    data = message.data.decode('utf-8')
    attributes = message.attributes

    name = attributes['name']
    time_created = attributes['timeCreated']
    bucket_id = attributes['bucketId']
    object_id = attributes['objectId']
    generation = attributes['objectGeneration']
    description = (
        '\tName: {name}\n'
        '\tTime Created: {time_created}\n'
        '\tBucket ID: {bucket_id}\n'
        '\tObject ID: {object_id}\n'
        '\tGeneration: {generation}\n'
        ).format(
            name=name,
            time_created=time_created,
            bucket_id=bucket_id,
            object_id=object_id,
            generation=generation
            )

    if 'overwroteGeneration' in attributes:
        description += '\tOverwrote generation: %s\n' % (
            attributes['overwroteGeneration'])
    if 'overwrittenByGeneration' in attributes:
        description += '\tOverwritten by generation: %s\n' % (
            attributes['overwrittenByGeneration'])

    payload_format = attributes['payloadFormat']
    if payload_format == 'JSON_API_V1':
        object_metadata = json.loads(data)
        name = object_metadata['name']
        time_created = object_metadata['timeCreated']
        size = object_metadata['size']
        content_type = object_metadata['contentType']
        metageneration = object_metadata['metageneration']
        description += (
            '\tName: {name}\n'
            '\tTime Created: {time_created}\n'
            '\tContent type: {content_type}\n'
            '\tSize: {object_size}\n'
            '\tMetageneration: {metageneration}\n'
            ).format(
                name=name,
                time_created=time_created,
                content_type=content_type,
                object_size=size,
                metageneration=metageneration
                )
    return description
    print('Note for developer: If BucketId and ObjectId listed, utf encoding.')
    print('If not, JSON_V1 encoding. Adjust accordingly.')

    # [END parse_message]
while True:
    print("signpost 1")
    summarize(message)
    print("signpost 2")
    time.sleep(10)
print("signpost 3")

#Below for passing unix commands, ignore for now
#import subprocess
