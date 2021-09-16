# VPC network peering 

The script counts peered networks and writes an entry to the Cloud Log and PubSub.

## Requirements

 ### Required: Python3
To install neccesary dependencies run command:
```python
pip install -r requirements.txt
```
## Permissions
Required roles: At  least pubsub.publisher, logWriter and  compute.network.viewer. 