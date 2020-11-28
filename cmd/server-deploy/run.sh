#! /usr/bin/env bash

function main {
      ./cmd/server-deploy/back/run.sh \
  &&  ./cmd/server-deploy/front/run.sh \

}

main "${@}"
