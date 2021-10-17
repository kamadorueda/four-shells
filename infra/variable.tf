
variable "ACME_EMAIL_ADDRESS" {}

variable "AWS_ACCESS_KEY_ID_TF" {}

variable "AWS_ECS_CLUSTER_NAME" {
  default = "four_shells"
}

variable "AWS_REGION" {}

variable "AWS_SECRET_ACCESS_KEY_TF" {}

variable "CF_DNS_API_TOKEN" {}

variable "SERVER_SESSION_SECRET" {}

variable "service_replicas" {
  default = 1
}
