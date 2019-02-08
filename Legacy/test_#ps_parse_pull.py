#Hi, Larry here. This script has quite a bit of history, see
#https://stackoverflow.com/questions/54283001/how-do-i-create-assign-a-logging-handler-for-google-cloud-pubsub
#if you're interested in how it came to be.
#
#Anyway, most of the 'print's have been suppressed to not clog up the console.
#
#We only really need the subprocess.call to pass instructions to minimap2.
#Pubsub messages can be watched at
#http://aligner-watcher-dot-nano-stream.appspot.com
#for diagnostics. If the messages are appearing there but not here, the fault lies in this script somewhere.
#If messages aren't even appearing there, something's broken in the pubsub chain.

import time
import subprocess
import json
import re

from google.cloud import pubsub_v1

project_id = "nano-stream"
subscription_name = "docker_watcher_pull"

def receive_messages_with_custom_attributes(project_id, subscription_name):
    """Receives messages from a pull subscription."""
    # [START pubsub_subscriber_sync_pull_custom_attributes]
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project_id, subscription_name)

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
        fullpath = dirpath + namepath
        fullpath = fullpath.encode("utf-8")

        runid =  re.search('(?<=runid_).+(?=_.*\.fas)', text).group(0)
        runid = runid + ".bam"

        subprocess.call(["echo", "align_mm2.sh", "-r", "/nano-stream/NewDatabases/genomeDB.fasta.mmi", "-f", '{0}'.format(fullpath), "-o", '{0}'.format(runid)"])

    subscriber.subscribe(subscription_path, callback=callback)
    # The subscriber is non-blocking, so we must keep the main thread from
    # exiting to allow it to process messages in the background.
    print('Listening for messages on {}'.format(subscription_path))
    while True:
        time.sleep(60)
    # [END pubsub_subscriber_sync_pull_custom_attributes]

receive_messages_with_custom_attributes(project_id, subscription_name)
