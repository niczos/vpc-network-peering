### Cloud Function 
The script counts VPC peered networks ever 30 minutes and creates metric to monitoring number of theese peered networks.

## Requirements:
Required: Python3
Required SA roles for the script: At least `compute.network.viewer` and `monitoring.metricWriter`.

In the file `variables.tf` change project_id and region to own variables.
Copy your key-file.json to folder `metric.zip`. 
To start using terraform run `terraform init` in command line. After that run `terraform apply`. This command will create PubSub topic from which Cloud Function will be triggered, Storage Bucket where function will be storage and Cloud Function that will count VPC peered networks and will create metric to monitoring number of peered networks.

To get neccesarry libraries to use `scheduler.py` run this command in command line:
```python
pip3 install google-cloud-scheduler
```
To deploy Cloud function in the command line run:
```python
python3 scheduler.py
```
This command will create a scheduler job that deploys function every 30 minutes.
