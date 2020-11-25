#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --keep ACME_EMAIL_ADDRESS
#!   nix-shell --keep AWS_ACCESS_KEY_ID_TF
#!   nix-shell --keep AWS_CLOUDFRONT_DOMAIN
#!   nix-shell --keep AWS_SECRET_ACCESS_KEY_TF
#!   nix-shell --keep CF_DNS_API_TOKEN
#!   nix-shell --keep GOOGLE_OAUTH_CLIENT_ID_SERVER
#!   nix-shell --keep GOOGLE_OAUTH_SECRET_SERVER
#!   nix-shell --pure
#!   nix-shell ../../cmd/infra-test
#  shellcheck shell=bash

source "${srcBuildUtilsCtxLibSh}"

function main {
  export TF_VAR_acme_email_address="${ACME_EMAIL_ADDRESS}"
  export TF_VAR_aws_access_key_id="${AWS_ACCESS_KEY_ID_TF}"
  export TF_VAR_aws_secret_access_key="${AWS_SECRET_ACCESS_KEY_TF}"
  export TF_VAR_cf_dns_api_token="${CF_DNS_API_TOKEN}"
  export TF_VAR_google_oauth_secret_server="${GOOGLE_OAUTH_CLIENT_ID_SERVER}"
  export TF_VAR_google_oauth_client_id_server="${GOOGLE_OAUTH_SECRET_SERVER}"
  export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID_TF}"
  export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY_TF}"

      pushd infra/ \
    &&  utils_terraform_prepare \
    &&  echo '[INFO] Planning infrastructure changes' \
    &&  terraform plan -lock=false -refresh=true \
  &&  popd \
  ||  return 1
}

main "${@}"
