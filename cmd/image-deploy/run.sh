#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --keep AWS_ACCESS_KEY_ID_ADMIN
#!   nix-shell --keep AWS_ACCOUNT_ID
#!   nix-shell --keep AWS_SECRET_ACCESS_KEY_ADMIN
#!   nix-shell --pure
#!   nix-shell ../../cmd/image-deploy
#  shellcheck shell=bash

source "${srcBuildUtilsCtxLibSh}"

function main {
  export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID_ADMIN}"
  export AWS_ACCOUNT_ID
  export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY_ADMIN}"
  local region='us-east-1'
  local registry="${AWS_ACCOUNT_ID}.dkr.ecr.${region}.amazonaws.com"
  local target="${registry}/four_shells:latest"

      echo "[INFO] Loading: ${oci}" \
  &&  docker load --input "${oci}" \
  &&  echo "[INFO] Tagging: ${target}" \
  &&  docker tag 'oci' "${target}" \
  &&  echo "[INFO] Authenticating to: ${registry}" \
  &&  aws ecr get-login-password --region "${region}" \
        | docker login --username AWS --password-stdin "${registry}" \
  &&  echo "[INFO] Pushing: ${target}" \
  &&  docker push "${target}"
}

main "${@}"
