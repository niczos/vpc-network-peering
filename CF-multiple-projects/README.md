## Cloud Function for multiple projects
The script counts VPC peered networks from multiple projects every 30 minutes and creates metric to monitoring number of theese peered networks.

#### Requirements:
Required: Python3  
Required roles for every SA: At least `compute.network.viewer` and `monitoring.metricWriter`.  

In the file `variables.tf` change **project_id** and **region** to own variables.  
Copy your all **key-files.json** to folder `metric.zip`.  
In the file `main.py` in folder `metric.zip` change variables to yours. Add as many projects from which number of peered networks will be received as you need. Call function `write_data` as many times depending on the number of projects with their parameters.  
To start using terraform run `terraform init` in command line. After that run `terraform apply`. This command will create PubSub topic from which Cloud Function will be triggered, Storage Bucket where function will be storage and Cloud Function that will count VPC peered networks and will create metric to monitoring number of peered networks.  

To get neccesarry packages to use `scheduler.py` run this command in the command line:
```python
pip3 install google-cloud-scheduler
```
To deploy Cloud function in the command line run:
```python
python3 scheduler.py
```
This command will create a scheduler job that deploys function every 30 minutes.  

To see this metric, open Metric Explorer in the Console GCP. Set *Resource type:* Global, *Metric:* custom/number-of-peered-networks-metric, *Group by:* project_id (metric label) and *Aligner:* mean.