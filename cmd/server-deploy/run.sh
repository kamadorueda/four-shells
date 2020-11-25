#! /usr/bin/env bash

function main {
      ./cmd/server-deploy/front/run.sh \
  &&  ./cmd/server-deploy/back/run.sh \

}

main "${@}"
