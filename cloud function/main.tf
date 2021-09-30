# "Copyright 2021 by Google. 
# Your use of any copyrighted material and any warranties, if applicable, are subject to your agreement with Google."
   
provider "google" {
    project = var.project_id
    region = var.region
}

resource "google_pubsub_topic" "topic" {
  name = "vpc-network-peer-topic"
}

resource "google_storage_bucket" "bucket" {
  name = "vpc-peer-network-bucket"
}

resource "google_storage_bucket_object" "archive" {
  name   = "metric.zip"
  bucket = google_storage_bucket.bucket.name
  source = "metric.zip"
}

resource "google_cloudfunctions_function" "function" {
  name        = "vpc-peer-net-function"
  description = "Function which creates metric to show number of peered networks in project."
  runtime     = "python39"

  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  event_trigger  {
      event_type = "google.pubsub.topic.publish"
      resource = "projects/${var.project_id}/topics/${google_pubsub_topic.topic.name}"
  }
  timeout               = 60
  entry_point           = "peer"
}

# IAM entry for all users to invoke the function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.function.project
  region         = google_cloudfunctions_function.function.region
  cloud_function = google_cloudfunctions_function.function.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}