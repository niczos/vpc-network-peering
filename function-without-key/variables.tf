variable "project_id" {
  type = string
  description = "The ID of the project in which we would like to have Cloud Function."
  default = "rational-moon-320316"
}

variable "region" {
    description = "The region of Cloud Function."
    default = "europe-west1"
}