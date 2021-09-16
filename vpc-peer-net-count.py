# Copyright 2021 by Google.
# Your use of any copyrighted material and any warranties, if applicable, are subject to your agreement with Google.

import googleapiclient.discovery
from google.oauth2 import service_account
import google.cloud.logging
from google.cloud import pubsub_v1
import os


# SET YOUR OWN VARIABLES
SERVICE_ACCOUNT_FILE = '<Path to your key file (in json) for service account>'
PEERING_NAME         = '<Name of peering connection>'
DIRECTION            = '<The direction of the exchanged routes - INCOMING or OUTGOING>'
NETWORK              = '<Name of the network for this request>'
PROJECT_ID           = '<Project ID for this request>'
REGION               = '<The region of the request>'
TOPIC_PATH           = '<Path to your topic in PubSub>'

# Sets environment variable
try:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE
    os.environ['GOOGLE_TOPIC_PATH'] = TOPIC_PATH
except NameError:
    print('Variable does not exist')

publisher = pubsub_v1.PublisherClient()
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

compute = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

response = compute.networks().listPeeringRoutes(project=f'{PROJECT_ID}', network=f'{NETWORK}',
        direction=f'{DIRECTION}', peeringName=f'{PEERING_NAME}', region=f'{REGION}').execute()

# Instantiates a client
client = google.cloud.logging.Client()
client.setup_logging()

# The name of the log to write to - change if needed
log_name = "vpc-network-peering-logs"
logger = client.logger(log_name)

if 'items' in response:
    length = len(response['items'])
    text = f"Number of {DIRECTION} peered networks: {length}"
    # Writes the log entry
    logger.log_text(text, severity="INFO")
    text = text.encode('utf-8')
    future = publisher.publish(TOPIC_PATH, text)  # message id
    print(f'published message id {future.result()}')

    if length > 50:
        error = "Too many peered networks - max 50."
        logger.log_text(error, severity="ERROR")
        error = error.encode('utf-8')
        future = publisher.publish(TOPIC_PATH, error)  # message id
        print(f'published message id {future.result()}')
        print("Logged: {}".format(error))

else:
    text = "No peered networks."
    logger.log_text(text, severity="INFO")
    text = text.encode('utf-8')
    future = publisher.publish(TOPIC_PATH, text)  # message id
    print(f'published message id {future.result()}')

print("Logged: {}".format(text))
