#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --pure
#!   nix-shell ../../cmd/back-sitemap
#  shellcheck shell=bash

source "${srcBuildCtxLibSh}"

function main {
  export DATA_NIXDB="${PWD}/../four-shells-data-nixdb"

      echo '[INFO] Computing sitemaps' \
  &&  rm -rf 'back/sitemap' \
  &&  git checkout -- 'back/sitemap' \
  &&  python3.8 'cmd/back-sitemap/sitemap.py'
}

main "${@}"
