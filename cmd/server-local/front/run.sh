#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --pure
#!   nix-shell ../../../cmd/server-local/front
#  shellcheck shell=bash

source "${srcBuildUtilsCtxLibSh}"

function main {
      echo '[INFO] Launching local front-end server!' \
  &&  echo \
  &&  pushd front \
    &&  npm install \
    &&  npm run-script serve \
  &&  popd \

}

main "${@}"
