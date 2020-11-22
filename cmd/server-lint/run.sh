#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --option sandbox false
#!   nix-shell --pure
#!   nix-shell ../../cmd/server-lint
#  shellcheck shell=bash

source "${srcBuildUtilsCtxLibSh}"

function main {
  export PYTHONPATH="${srcServer}/pkgs/cachipfs:${PYTHONPATH}"
  export PYTHONPATH="${srcServer}/pkgs/four_shells:${PYTHONPATH}"

  for pkg in \
    server/pkgs/cachipfs \
    server/pkgs/four_shells \

  do
        echo "[INFO] Checking static typing: ${pkg}" \
    &&  mypy \
          --ignore-missing-imports \
          --strict \
          --pretty \
          "${pkg}" \
    &&  echo "[INFO] Linting: ${pkg}" \
    &&  prospector \
          --full-pep8 \
          --strictness veryhigh \
          --test-warnings \
          "${pkg}" \
    ||  return 1
  done
}

main "${@}"
