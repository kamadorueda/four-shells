#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --pure
#!   nix-shell --keep AWS_ACCESS_KEY_ID_ADMIN
#!   nix-shell --keep AWS_CLOUDFRONT_DOMAIN
#!   nix-shell --keep AWS_SECRET_ACCESS_KEY_ADMIN
#!   nix-shell ../../cmd/front-deploy
#  shellcheck shell=bash

source "${srcBuildCtxLibSh}"

function main {
  local root="${PWD}/.."
  export DATA_NIXDB="${root}/four-shells-data-nixdb"
  export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID_ADMIN}"
  export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY_ADMIN}"

      echo '[INFO] Cleaning paths' \
  &&  rm -rf 'public/front' \
  &&  rm -rf 'public/sitemap' \
  &&  mkdir 'public/sitemap' \
  &&  echo '[INFO] Computing sitemaps' \
  &&  python3.8 'cmd/front-deploy/sitemap.py' \
  &&  echo '[INFO] Building front' \
  &&  pushd front \
    &&  npm install \
    &&  npm run-script build \
  &&  popd \
  &&  echo \
  &&  read -N 1 -p '[INFO] Press any key to deploy public content and front-end' -r \
  &&  echo \
  &&  echo '[INFO] Syncing public content' \
  &&  aws s3 sync --delete 'public' 's3://four-shells-public-content' \

}

main "${@}"
