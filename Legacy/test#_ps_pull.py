import datetime
from google.cloud import pubsub_v1

namepref = "minimap_VM+"
timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%I.%M:")
subname = namepref + timestamp

project_id = "nano-stream"
topic_name = "FILE_UPLOAD"
subscription_name = subname

def create_subscription(project_id, topic_name, subscription_name):
    """Create a new pull subscription on the given topic."""
    # [START pubsub_create_pull_subscription]
    from google.cloud import pubsub_v1

    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project_id, topic_name)
    subscription_path = subscriber.subscription_path(
        project_id, subscription_name)

    subscription = subscriber.create_subscription(
        subscription_path, topic_path)

    print('Subscription created: {}'.format(subscription))
    # [END pubsub_create_pull_subscription]

create_subscription(project_id, topic_name, subscription_name)
