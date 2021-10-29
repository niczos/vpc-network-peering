# "Copyright 2021 by Google. 
# Your use of any copyrighted material and any warranties, if applicable, are subject to your agreement with Google."

provider "google" {
    project = var.project_id
    region = var.region
}

locals {
  project_id = "rational-moon-320316,	my-project-scope-327709"
}

# SA and keys
resource "google_service_account" "service_account" {
  account_id   = "sa-vpc-peering"
  display_name = "Service Account for Cloud Function"
  project = var.project_id
}

resource "google_project_iam_binding" "project" {
  project = var.project_id
  role =  "roles/compute.networkViewer"
  members = [
  format("serviceAccount:%s", google_service_account.service_account.email)]
}


resource "google_project_iam_binding" "project1" {
  project = var.project_id
  role =  "roles/monitoring.metricWriter"
  members = [
  format("serviceAccount:%s", google_service_account.service_account.email)]
}

resource "google_pubsub_topic" "topic" {
  name = "vpc-network-peering-topic"
}

# storage 
data "archive_file" "zip_file" {
  type        = "zip"
  source_dir = "function_files"
  output_path = "metric.zip"
  depends_on = [google_storage_bucket.bucket]
}

resource "google_storage_bucket" "bucket" {
  name = "vpc-network-peering-bucket"
}

resource "google_storage_bucket_object" "archive" {
  name   = "metric.zip"
  bucket = google_storage_bucket.bucket.name
  source = "metric.zip"
}

resource "google_cloudfunctions_function" "function" {
  name        = "vpc-peering-net-function"
  description = "Function which creates metric to show number of peered networks in project."
  runtime     = "python39"

  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  service_account_email = google_service_account.service_account.email
  event_trigger  {
      event_type = "google.pubsub.topic.publish"
      resource = "projects/${var.project_id}/topics/${google_pubsub_topic.topic.name}"
  }
  timeout               = 60
  entry_point           = "peer"

  environment_variables = {
    TF_VAR_PROJECT = local.project_id
  }
}

resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.function.project
  region         = google_cloudfunctions_function.function.region
  cloud_function = google_cloudfunctions_function.function.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}