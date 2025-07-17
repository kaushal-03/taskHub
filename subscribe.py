from google.cloud import pubsub_v1
from celery_init import AutomateDispatch

import json

project_id = "!!!!"
subscription_id = "!!!"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message):
    print(message.data.decode('utf-8'), "data")
    print(message.attributes, "attributes")
    data = json.loads(message.data.decode('utf-8'))
    message.ack()
    AutomateDispatch.delay(data.get('historyId'))





streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
    print("Stopped listening.")

