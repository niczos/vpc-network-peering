from google.cloud import monitoring_v3

client = monitoring_v3.MetricServiceClient()
client.delete_metric_descriptor(name="projects/rational-moon-320316/metricDescriptors/custom.googleapis.com/number-of-peered-networks-metric")
print("Deleted metric descriptor {}.".format("projects/rational-moon-320316/metricDescriptors/custom.googleapis.com/number-of-peered-networks-metric"))