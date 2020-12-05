terraform {
  backend "s3" {
    bucket  = "4shells-infra-states"
    encrypt = true
    key     = "infra.tfstate"
    region  = "us-east-1"
  }
  required_providers {
    acme = {
      source  = "vancluever/acme"
      version = "1.6.3"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "3.15.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "3.0.0"
    }
  }
  required_version = "0.13.5"
}
