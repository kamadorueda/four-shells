#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --keep GITHUB_USER
#!   nix-shell --keep GITHUB_PERSONAL_ACCESS_TOKEN
#!   nix-shell --pure
#!   nix-shell ./deps/image-deploy.nix
#  shellcheck shell=bash

source "${srcBuildCtxSh}"

function main {
    local registry='docker.pkg.github.com'
    local target="${registry}/kamadorueda/4shells.com/4shells.com:latest"

        echo '[INFO] Building' \
    &&  DOCKER_BUILDKIT=1 docker build --tag "${target}" . \
    &&  echo '[INFO] Authenticating' \
    &&  echo "${GITHUB_PERSONAL_ACCESS_TOKEN}" \
          | docker login -u "${GITHUB_USER}" --password-stdin "${registry}" \
    &&  echo '[INFO] Pushing' \
    &&  docker push "${target}"
}

main "${@}"
