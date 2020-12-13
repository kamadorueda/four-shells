#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --option sandbox false
#!   nix-shell --pure
#!   nix-shell ../../cmd/back-lint
#  shellcheck shell=bash

source "${srcBuildCtxLibSh}"

function main {
  export PYTHONPATH="${srcBack}:${PYTHONPATH}"
  local pkgs=( back/src/* )

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
