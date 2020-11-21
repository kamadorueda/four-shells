#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --keep ADMIN_AWS_ACCESS_KEY_ID
#!   nix-shell --keep ADMIN_AWS_SECRET_ACCESS_KEY
#!   nix-shell --pure
#!   nix-shell ./deps/image-deploy.nix
#  shellcheck shell=bash

source "${srcBuildCtxSh}"

function main {
    export AWS_ACCESS_KEY_ID="${ADMIN_AWS_ACCESS_KEY_ID}"
    export AWS_SECRET_ACCESS_KEY="${ADMIN_AWS_SECRET_ACCESS_KEY}"
    local account_id='791877604510'
    local region='us-east-1'
    local registry="${account_id}.dkr.ecr.${region}.amazonaws.com"
    local repository='four_shells'
    local target="${registry}/${repository}:latest"

        echo '[INFO] Building' \
    &&  DOCKER_BUILDKIT=1 \
        docker build --tag "${target}" . \
    &&  echo '[INFO] Authenticating' \
    &&  aws ecr get-login-password --region "${region}" \
          | docker login --username AWS --password-stdin "${registry}" \
    &&  echo '[INFO] Pushing' \
    &&  docker push "${target}"
}

main "${@}"
