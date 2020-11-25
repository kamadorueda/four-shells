
variable "acme_email_address" {}

variable "aws_access_key_id" {}

variable "aws_ecs_cluster_name" {
  default = "four_shells"
}

variable "aws_secret_access_key" {}

variable "cf_dns_api_token" {}

variable "google_oauth_secret_server" {}

variable "google_oauth_client_id_server" {}

variable "region" {
  default = "us-east-1"
}

variable "service_deploy_on_each_apply" {
  default = false
}

variable "service_replicas" {
  default = 1
}
