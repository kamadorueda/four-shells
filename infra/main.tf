provider "aws" {
  access_key = var.access_key
  secret_key = var.secret_key
  region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket  = "4shells-infra-states"
    encrypt = true
    key     = "infra.tfstate"
    region  = "us-east-1"
  }
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "3.15.0"
    }
  }
  required_version = "0.13.5"
}
