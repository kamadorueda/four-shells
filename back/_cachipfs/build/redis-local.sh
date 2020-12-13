#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --pure
#!   nix-shell ./deps/redis-local.nix
#  shellcheck shell=bash

source "${srcBuildCtxSh}"

function main {
  redis-server
}

main "${@}"
