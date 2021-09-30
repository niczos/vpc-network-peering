# "Copyright 2021 by Google. 
# Your use of any copyrighted material and any warranties, if applicable, are subject to your agreement with Google."

from google.cloud import scheduler_v1

project_id = '<Project ID for this request.>'
sa_key_file = '<Path to your key file (in json) for service account>'
region =  '<The region of the request.>'

client = scheduler_v1.CloudSchedulerClient.from_service_account_json(sa_key_file)
parent = client.common_location_path(project_id, region)

job = {
    'name': f'projects/{project_id}/locations/{region}/jobs/vpc-peer-net-job',
    'description': 'Scheduler for VPC peering network Cloud function',
    'pubsub_target': {
        'topic_name': f'projects/{project_id}/topics/vpc-network-peer-topic',
        'data': b'run-script'
    },
    'schedule': '*/30 * * * *',  # Job will be executed every minute
    'time_zone': 'US/Central'  # The time zone to be used in interpreting schedule.
}

responce = client.create_job(parent=parent, job=job)
