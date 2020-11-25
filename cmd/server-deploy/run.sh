#! /usr/bin/env bash

function main {
      ./cmd/server-deploy/build/run.sh \
  &&  ./cmd/server-deploy/deploy/run.sh \

}

main "${@}"
