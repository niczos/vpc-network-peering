# Copyright 2021 by Google.
# Your use of any copyrighted material and any warranties, if applicable, are subject to your agreement with Google.

import googleapiclient.discovery
from google.oauth2 import service_account
from google.cloud import monitoring_v3
from google.api import metric_pb2 as ga_metric
import time
import os

# SET YOUR OWN VARIABLES.
SERVICE_ACCOUNT_FILE = '<Path to your key file (in json) for service account>'
PEERING_NAME         = '<Name of peering connection>'
DIRECTION            = '<The direction of the exchanged routes - INCOMING or OUTGOING>'
NETWORK              = '<Name of the network for this request>'
PROJECT_ID           = '<Project ID for this request>'
REGION               = '<The region of the request>'
METRIC_NAME          = "number-of-peered-networks-metric" # change if needed

# Sets environment variable
try:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE
except NameError:
    print('Variable does not exist')

SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

compute = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

response = compute.networks().listPeeringRoutes(project=f'{PROJECT_ID}', network=f'{NETWORK}',
        direction=f'{DIRECTION}', peeringName=f'{PEERING_NAME}', region=f'{REGION}').execute()

if 'items' in response:
    length = len(response['items'])

########## CREATE CUSTOM METRIC ##########

client = monitoring_v3.MetricServiceClient()
project_name = f"projects/{PROJECT_ID}"
descriptor = ga_metric.MetricDescriptor()
descriptor.type = f"custom.googleapis.com/{METRIC_NAME}"
descriptor.metric_kind = ga_metric.MetricDescriptor.MetricKind.GAUGE
descriptor.value_type = ga_metric.MetricDescriptor.ValueType.DOUBLE
descriptor.description = "VPC peering network metric."

descriptor = client.create_metric_descriptor(name=project_name, metric_descriptor=descriptor)
print("Created {}.".format(descriptor.name))

########### WRITE DATA TO CUTOM METRIC ##########

series = monitoring_v3.TimeSeries()
series.metric.type = f"custom.googleapis.com/{METRIC_NAME}"
series.resource.type = "global"  # https://cloud.google.com/monitoring/custom-metrics/creating-metrics#custom-metric-resources
series.resource.labels["project_id"] = PROJECT_ID

now = time.time()
seconds = int(now)
nanos = int((now - seconds) * 10 ** 9)
interval = monitoring_v3.TimeInterval({"end_time": {"seconds": seconds, "nanos": nanos}})
point = monitoring_v3.Point({"interval": interval, "value": {"double_value": length}})
series.points = [point]
client.create_time_series(name=project_name, time_series=[series])

print("Wrote number of vpc peered networks to metric.")
