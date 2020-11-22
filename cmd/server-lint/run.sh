#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --pure
#!   nix-shell ../../cmd/server-lint
#  shellcheck shell=bash

source "${srcBuildUtilsCtxLibSh}"

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
