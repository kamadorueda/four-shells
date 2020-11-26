provider "acme" {
  server_url = "https://acme-v02.api.letsencrypt.org/directory"
}

provider "aws" {
  access_key = var.AWS_ACCESS_KEY_ID_TF
  secret_key = var.AWS_SECRET_ACCESS_KEY_TF
  region     = var.AWS_REGION
}

provider "tls" {}
