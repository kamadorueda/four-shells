#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --keep TF_AWS_ACCESS_KEY_ID
#!   nix-shell --keep TF_AWS_SECRET_ACCESS_KEY
#!   nix-shell --pure
#!   nix-shell ./deps/infra-test.nix
#  shellcheck shell=bash

source "${srcBuildCtxSh}"

function main {
  export TF_VAR_access_key="${TF_AWS_ACCESS_KEY_ID}"
  export TF_VAR_secret_key="${TF_AWS_SECRET_ACCESS_KEY}"
  export AWS_ACCESS_KEY_ID="${TF_AWS_ACCESS_KEY_ID}"
  export AWS_SECRET_ACCESS_KEY="${TF_AWS_SECRET_ACCESS_KEY}"

      pushd infra/ \
    &&  utils_terraform_prepare \
    &&  echo '[INFO] Planning infrastructure changes' \
    &&  terraform plan -lock=false -refresh=true \
  &&  popd \
  ||  return 1
}

main "${@}"
