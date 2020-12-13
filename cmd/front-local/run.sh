#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --pure
#!   nix-shell ../../cmd/front-local
#  shellcheck shell=bash

source "${srcBuildCtxLibSh}"

function main {
      echo '[INFO] Launching local front-end server!' \
  &&  echo \
  &&  pushd front \
    &&  npm install \
    &&  npm run-script serve \
  &&  popd \
  ||  return 1
}

main "${@}"
