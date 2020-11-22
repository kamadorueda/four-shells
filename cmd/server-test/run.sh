#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --keep AWS_ACCESS_KEY_ID_SERVER
#!   nix-shell --keep AWS_REGION
#!   nix-shell --keep AWS_SECRET_ACCESS_KEY_SERVER
#!   nix-shell --pure
#!   nix-shell ../../cmd/server-test
#  shellcheck shell=bash

source "${srcBuildUtilsCtxLibSh}"

function main {
  export PYTHONPATH="${srcServer}/pkgs/cachipfs:${PYTHONPATH}"
  export PYTHONPATH="${srcServer}/pkgs/four_shells:${PYTHONPATH}"
  local pkgs=(
    server/pkgs/cachipfs/cachipfs
    server/pkgs/four_shells/four_shells
  )

  for pkg in "${pkgs[@]}"
  do
        echo "[INFO] Testing: ${pkg}" \
    &&  pytest \
          --capture tee-sys \
          --cov-branch \
          --cov-report 'term' \
          --cov-report "html:${pkg}/coverage" \
          --cov "${pkg}" \
          --disable-pytest-warnings \
          --exitfirst \
          --no-cov-on-fail \
          --show-capture no \
          --verbose \
          "${pkg}_test" \
    ||  return 1
  done
}

main "${@}"
