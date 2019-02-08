import datetime
import time
import subprocess
import json
import re
from google.cloud import pubsub_v1

project_id = "nano-stream"
topic_name = "FILE_UPLOAD"

#Generates unique subscription topics according to the time at which the VM
#started up, accuracy to per minute.
subpref = "minimap_VM+"
ts = datetime.datetime.now().strftime("%Y_%m_%d_%I.%M")
subname = subpref + ts
subscription_name = subname

def create_subscription(project_id, topic_name, subscription_name):
    """Create a new pull subscription on the given topic."""
    # [START pubsub_create_pull_subscription]

    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project_id, topic_name)
    subscription_path = subscriber.subscription_path(
        project_id, subscription_name)

    subscription = subscriber.create_subscription(
        subscription_path, topic_path)

    print('Subscription created: {}'.format(subscription))
    # [END pubsub_create_pull_subscription]

def receive_messages_with_custom_attributes(project_id, subscription_name):
    """Receives messages from a pull subscription."""
    # [START pubsub_subscriber_sync_pull_custom_attributes]
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    def callback(message):
        #print('Received message: {}'.format(message.data))
        if message.attributes:
            #print('Attributes:')
            for key in message.attributes:
                value = message.attributes.get(key);
                #print('{}: {}'.format(key, value))
        message.ack()

        #translates above dictionary from BYTES to unicode and finally string
        payload = json.loads(message.data.decode('utf-8'))
        namepath = payload["name"]
        dirpath = "/nano-stream/"
        fullfastq = dirpath + namepath
        fullfastq = fullfastq.encode("utf-8")
        print("before runid")

        runid = re.search('(?<=runid_).+(?=_.*\.fas)', namepath).group(0)
        runid = runid + ".bam"
        outdir = "/nano-stream/SAM/"
        fullbam = outdir + runid
        fullbam = fullfastq.encode("utf-8")

        subprocess.call(["bash", "align_mm2.sh", "-r", "/nano-stream/NewDatabases/genomeDB.fasta.mmi", "-f", '{}'.format(fullfastq), "-o", '{}'.format(fullbam)])

    subscriber.subscribe(subscription_path, callback=callback)
    # The subscriber is non-blocking, so we must keep the main thread from
    # exiting to allow it to process messages in the background.
    print('Listening for messages on {}'.format(subscription_path))
    while True:
        time.sleep(60)
    # [END pubsub_subscriber_sync_pull_custom_attributes]

create_subscription(project_id, topic_name, subscription_name)
receive_messages_with_custom_attributes(project_id, subscription_name)
