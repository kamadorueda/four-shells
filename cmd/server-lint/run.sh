#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --option sandbox false
#!   nix-shell --pure
#!   nix-shell ../../cmd/server-lint
#  shellcheck shell=bash

source "${srcBuildUtilsCtxLibSh}"

function main {
  export PYTHONPATH="${srcServerPkgs}/four_shells:${PYTHONPATH}"
  export SERVER_PATH_PUBLIC="${srcServerPublic}"
  local pkgs=(
    server/pkgs/four_shells/four_shells
  )

  for pkg in "${pkgs[@]}"
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
