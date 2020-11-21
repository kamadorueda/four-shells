#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --pure
#!   nix-shell ../build/deps/build-lint.nix
#  shellcheck shell=bash

source "${srcBuildCtxSh}"

function main {
      echo "[INFO] Linting" \
  &&  find '.' \
        -name '*.sh' \
        -exec \
          shellcheck \
            --exclude SC1090,SC2154 \
            --external-sources {} + \
  &&  echo '[OK] Shell code is compliant'
}

main "${@}"
