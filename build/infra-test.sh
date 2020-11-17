#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --keep ROOT_AWS_ACCESS_KEY_ID
#!   nix-shell --keep ROOT_AWS_SECRET_ACCESS_KEY
#!   nix-shell --pure
#!   nix-shell ./deps/infra-test.nix
#  shellcheck shell=bash

source "${srcBuildCtxSh}"

function main {
  export TF_VAR_aws_access_key_id="${ROOT_AWS_ACCESS_KEY_ID}"
  export TF_VAR_aws_secret_access_key="${ROOT_AWS_SECRET_ACCESS_KEY}"

      pushd infra/ \
    &&  echo '[INFO] Initializing' \
    &&  terraform init \
    &&  echo '[INFO] Linting...' \
    &&  tflint --config tflint.hcl \
    &&  echo '[INFO] Planning infrastructure changes...' \
    &&  terraform plan -lock=false -refresh=true \
  &&  popd \
  ||  return 1
}

main "${@}"
