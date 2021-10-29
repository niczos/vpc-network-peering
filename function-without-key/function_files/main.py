# Copyright 2021 by Google.
# Your use of any copyrighted material and any warranties, if applicable, are subject to your agreement with Google.

import googleapiclient.discovery
from google.cloud import monitoring_v3
from google.api import metric_pb2 as ga_metric
import time
from flask import escape
import os

def peer(event, context):

    projects = os.environ.get("TF_VAR_PROJECT").split(",")
    PROJECT_ID = projects[0]
    METRIC_NAME = "number-of-peered-networks-metrico"  # change if needed

    compute = googleapiclient.discovery.build('compute', 'v1')

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

    ###############################################

    def write_data(project_id, network, direction, peering_name, region):
        compute = googleapiclient.discovery.build('compute', 'v1')
        response = compute.networks().listPeeringRoutes(project=f'{project_id}', network=f'{network}',
                direction=f'{direction}', peeringName=f'{peering_name}', region=f'{region}').execute()

        if 'items' in response:
            length = len(response['items'])
            if length > 25:
                print(f'Too many peered network in {project_id} - max.25')


        ########### WRITE DATA TO CUSTOM METRIC ##########

        series = monitoring_v3.TimeSeries()
        series.metric.type = f"custom.googleapis.com/{METRIC_NAME}"
        series.resource.type = "global" 
        series.metric.labels["project_id"] = project_id
        series.metric.labels["peering_name"] = peering_name

        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10 ** 9)
        interval = monitoring_v3.TimeInterval({"end_time": {"seconds": seconds, "nanos": nanos}})
        point = monitoring_v3.Point({"interval": interval, "value": {"double_value": length}})
        series.points = [point]
        client.create_time_series(name=project_name, time_series=[series])

        print("Wrote number of vpc peered networks to metric.")

    for p in projects:
        response = compute.networks().list(project=f'{p}').execute()
        for i in response['items']:
            if 'peerings' in i:
                NETWORK = i['name']
                PEERING_NAME = i['peerings'][0]['name']
                DIRECTION            = 'OUTGOING'  # The direction of the exchanged routes - INCOMING or OUTGOING
                REGION               = "europe-west1"  # The region of the request.
                write_data(p,NETWORK, DIRECTION, PEERING_NAME, REGION)
                
    return ('Success')