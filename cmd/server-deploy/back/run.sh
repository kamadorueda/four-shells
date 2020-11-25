#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --keep AWS_ACCESS_KEY_ID_ADMIN
#!   nix-shell --keep AWS_ACCESS_KEY_ID_SERVER
#!   nix-shell --keep AWS_ACCOUNT_ID
#!   nix-shell --keep AWS_CLOUDFRONT_DOMAIN
#!   nix-shell --keep AWS_REGION
#!   nix-shell --keep AWS_SECRET_ACCESS_KEY_ADMIN
#!   nix-shell --keep AWS_SECRET_ACCESS_KEY_SERVER
#!   nix-shell --keep GOOGLE_OAUTH_CLIENT_ID_SERVER
#!   nix-shell --keep GOOGLE_OAUTH_SECRET_SERVER
#!   nix-shell --pure
#!   nix-shell ../../../cmd/server-deploy/back
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
  &&  echo "[INFO] Testing image" \
  &&  docker run \
        --interactive \
        --env "AWS_ACCESS_KEY_ID_SERVER=${AWS_ACCESS_KEY_ID_SERVER}" \
        --env "AWS_CLOUDFRONT_DOMAIN=${AWS_CLOUDFRONT_DOMAIN}" \
        --env "AWS_REGION=${AWS_REGION}" \
        --env "AWS_SECRET_ACCESS_KEY_SERVER=${AWS_SECRET_ACCESS_KEY_SERVER}" \
        --env "GOOGLE_OAUTH_CLIENT_ID_SERVER=${GOOGLE_OAUTH_CLIENT_ID_SERVER}" \
        --env "GOOGLE_OAUTH_SECRET_SERVER=${GOOGLE_OAUTH_SECRET_SERVER}" \
        --env "PRODUCTION=true" \
        --publish 8400:8400 \
        --tty \
        "${target}" \
        four-shells \
  &&  echo \
  &&  read -N 1 -p '[INFO] Press any key to deploy production server' \
  &&  echo \
  &&  echo "[INFO] Authenticating to: ${registry}" \
  &&  aws ecr get-login-password --region "${region}" \
        | docker login --username AWS --password-stdin "${registry}" \
  &&  echo "[INFO] Pushing: ${target}" \
  &&  docker push "${target}"
}

main "${@}"
