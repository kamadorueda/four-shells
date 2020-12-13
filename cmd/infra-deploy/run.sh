#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --keep ACME_EMAIL_ADDRESS
#!   nix-shell --keep AWS_ACCESS_KEY_ID_TF
#!   nix-shell --keep AWS_CLOUDFRONT_DOMAIN
#!   nix-shell --keep AWS_REGION
#!   nix-shell --keep AWS_SECRET_ACCESS_KEY_TF
#!   nix-shell --keep CF_DNS_API_TOKEN
#!   nix-shell --keep GOOGLE_OAUTH_CLIENT_ID_SERVER
#!   nix-shell --keep GOOGLE_OAUTH_SECRET_SERVER
#!   nix-shell --keep SERVER_SESSION_SECRET
#!   nix-shell --pure
#!   nix-shell ../../cmd/infra-deploy
#  shellcheck shell=bash

source "${srcBuildCtxLibSh}"

function main {
  export TF_VAR_ACME_EMAIL_ADDRESS="${ACME_EMAIL_ADDRESS}"
  export TF_VAR_AWS_ACCESS_KEY_ID_TF="${AWS_ACCESS_KEY_ID_TF}"
  export TF_VAR_AWS_REGION="${AWS_REGION}"
  export TF_VAR_AWS_SECRET_ACCESS_KEY_TF="${AWS_SECRET_ACCESS_KEY_TF}"
  export TF_VAR_CF_DNS_API_TOKEN="${CF_DNS_API_TOKEN}"
  export TF_VAR_GOOGLE_OAUTH_CLIENT_ID_SERVER="${GOOGLE_OAUTH_CLIENT_ID_SERVER}"
  export TF_VAR_GOOGLE_OAUTH_SECRET_SERVER="${GOOGLE_OAUTH_SECRET_SERVER}"
  export TF_VAR_SERVER_SESSION_SECRET="${SERVER_SESSION_SECRET}"
  export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID_TF}"
  export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY_TF}"

      pushd infra/ \
    &&  utils_terraform_prepare \
    &&  echo '[INFO] Deploying infrastructure changes...' \
    &&  terraform apply -auto-approve -refresh=true \
  &&  popd \
  ||  return 1
}

main "${@}"
