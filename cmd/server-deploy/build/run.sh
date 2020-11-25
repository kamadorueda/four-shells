#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --pure
#!   nix-shell ../../../cmd/server-deploy/build
#  shellcheck shell=bash

source "${srcBuildUtilsCtxLibSh}"

function main {
      echo '[INFO] Building front' \
  &&  pushd server/front \
    &&  npm install \
    &&  npm run-script build \
  &&  popd
}

main "${@}"
