import argparse
import base64
import json
import re
import socket
import sys
import time

from google.cloud import pubsub_v1

def create_push_subscription(project_id,
                             topic_name,
                             subscription_name,
                             endpoint):
    """Create a new push subscription on the given topic."""
    # [START pubsub_create_push_subscription]
    from google.cloud import pubsub_v1

    project_id = "nano-stream"
    topic_name = "FILE_UPLOAD"
    subscription_name = "docker_watcher"
    endpoint = "https://aligner-watcher-dot-nano-stream.appspot.com/pubsub/push?token=1234abcd"

    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project_id, topic_name)
    subscription_path = subscriber.subscription_path(
        project_id, subscription_name)

    push_config = pubsub_v1.types.PushConfig(
        push_endpoint=endpoint)

    subscription = subscriber.create_subscription(
        subscription_path, topic_path, push_config)

    print('Push subscription created: {}'.format(subscription))
    print('Endpoint for subscription is: {}'.format(endpoint))
    # [END pubsub_create_push_subscription]

# def receive_messages_with_custom_attributes(project_id, subscription_name):
#     """Receives messages from a pull subscription."""
#     # [START pubsub_subscriber_sync_pull_custom_attributes]
#     import time
#
#     from google.cloud import pubsub_v1
#
#     project_id = "nano-stream"
#     subscription_name = "aligner_watcher"
#
#     subscriber = pubsub_v1.SubscriberClient()
#     subscription_path = subscriber.subscription_path(
#         project_id, subscription_name)
#
#     def callback(message):
#         print('Received message: {}'.format(message.data))
#         if message.attributes:
#             print('Attributes:')
#             for key in message.attributes:
#                 value = message.attributes.get(key)
#                 print('{}: {}'.format(key, value))
#         message.ack()
#
#     subscriber.subscribe(subscription_path, callback=callback)
#
#     # The subscriber is non-blocking, so we must keep the main thread from
#     # exiting to allow it to process messages in the background.
#     print('Listening for messages on {}'.format(subscription_path))
#     while True:
#         time.sleep(60)
#     # [END pubsub_subscriber_sync_pull_custom_attributes]

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
    print('Note for developer: If BucketId and ObjectId listed, utf encoding.\n
    If not, JSON_V1 encoding. Adjust accordingly.',
    )
    # [END parse_message]
###############################################################################
import subprocess
