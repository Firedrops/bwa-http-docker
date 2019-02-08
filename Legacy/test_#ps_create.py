import argparse
import base64
import json
import re
import socket
import sys
import time

from google.cloud import pubsub_v1

project_id = "nano-stream"
topic_name = "FILE_UPLOAD"
subscription_name = "docker_watcher"
endpoint = "https://aligner-watcher-dot-nano-stream.appspot.com/pubsub/push?token=1234abcd"

def create_push_subscription(project_id,
                             topic_name,
                             subscription_name,
                             endpoint):
    """Create a new push subscription on the given topic."""
    # [START pubsub_create_push_subscription]

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

create_push_subscription(project_id, topic_name, subscription_name, endpoint)
