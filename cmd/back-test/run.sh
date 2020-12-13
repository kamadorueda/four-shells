#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --keep AWS_ACCESS_KEY_ID_SERVER
#!   nix-shell --keep AWS_ACCOUNT_ID
#!   nix-shell --keep AWS_CLOUDFRONT_DOMAIN
#!   nix-shell --keep AWS_REGION
#!   nix-shell --keep AWS_SECRET_ACCESS_KEY_SERVER
#!   nix-shell --keep GOOGLE_OAUTH_CLIENT_ID_SERVER
#!   nix-shell --keep GOOGLE_OAUTH_SECRET_SERVER
#!   nix-shell --keep SERVER_SESSION_SECRET
#!   nix-shell --pure
#!   nix-shell ../../cmd/back-test
#  shellcheck shell=bash

source "${srcBuildCtxLibSh}"

function main {
  export PYTHONPATH="${srcBack}/src:${PYTHONPATH}"

      pushd back \
  &&  pytest \
        --capture tee-sys \
        --cov-branch \
        --cov-report 'term' \
        --cov-report "html:coverage" \
        --cov 'back' \
        --disable-pytest-warnings \
        --exitfirst \
        --no-cov-on-fail \
        --show-capture no \
        --verbose \
        --verbose \
        --verbose \
  ||  return 1

}

main "${@}"
