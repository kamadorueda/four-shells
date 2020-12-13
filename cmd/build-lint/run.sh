#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --pure
#!   nix-shell ../../cmd/build-lint
#  shellcheck shell=bash

source "${srcBuildCtxLibSh}"

function main {
      echo "[INFO] Linting" \
  &&  find '.' \
        -name '*.sh' \
        -not -wholename '*/node_modules/*' \
        -exec \
          shellcheck \
            --exclude SC1090,SC2154 \
            --external-sources {} + \
  &&  echo '[OK] Shell code is compliant'
}

main "${@}"
