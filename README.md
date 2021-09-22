# VPC network peering 

The script `vpc-peer-net-count.py` counts VPC peered networks and writes an entry to the Cloud Log and PubSub.
The script `metric-vpc.py` counts VPC peered networks and creates metric to monitoring number of peered networks.


## Requirements

 ### Required: Python3
To install neccesary dependencies run command:
```python
pip install -r requirements.txt
```
## Permissions
Required SA roles for `vpc-peer-net-count.py`: At  least pubsub.publisher, logWriter and  compute.network.viewer.
Required SA roles for `metric-vpc.py`: At  least compute.network.viewer and monitoring.metricWriter.