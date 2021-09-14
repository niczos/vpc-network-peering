# Copyright 2021 by Google.
# Your use of any copyrighted material and any warranties, if applicable, are subject to your agreement with Google.

import googleapiclient.discovery
from google.oauth2 import service_account
import google.cloud.logging
import os

SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

# SET YOUR OWN VARIABLES
SERVICE_ACCOUNT_FILE = '<Path to your key file (in json) for service account>'
PEERING_NAME         = '<Name of peering connection>'
DIRECTION            = '<The direction of the exchanged routes - INCOMING or OUTGOING>'
NETWORK              = '<Name of the network for this request>'
PROJECT_ID           = '<Project ID for this request>'
REGION               = '<The region of the request>'

# Sets environment variable
try:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE
except NameError:
    print('Variable does not exist')

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
        text = f"Number of {DIRECTION} peered networks: {len(response['items'])}"
        # Writes the log entry
        logger.log_text(text, severity="INFO")
else:
        text = "No peered networks."
        logger.log_text(text, severity="INFO")

print("Logged: {}".format(text))
