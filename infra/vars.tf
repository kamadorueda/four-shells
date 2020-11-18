data "aws_caller_identity" "current" {}
variable "access_key" {}
variable "region" {
  default = "us-east-1"
}
variable "secret_key" {}
