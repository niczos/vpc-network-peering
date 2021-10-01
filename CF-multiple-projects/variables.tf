variable "project_id" {
  type = string
  description = "The ID of the project in which we would like to have Cloud Function."
  default = "<Project ID for this request.>"
}

variable "region" {
    description = "The region of Cloud Function."
    default = "<The region of the request.>"
}