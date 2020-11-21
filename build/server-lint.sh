#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell ../build/deps/server-lint.nix
#  shellcheck shell=bash

source "${srcBuildCtxSh}"

function main {
      echo "[INFO] Checking static typing" \
  &&  mypy \
        --strict \
        --pretty \
        server/four_shells \
  &&  echo "[INFO] Linting" \
  &&  prospector \
        --doc-warnings \
        --full-pep8 \
        --strictness veryhigh \
        --test-warnings \
        server/four_shells \

}

main "${@}"
