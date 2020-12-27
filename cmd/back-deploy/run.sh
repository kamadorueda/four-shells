#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --keep AWS_ACCESS_KEY_ID_ADMIN
#!   nix-shell --keep AWS_ACCESS_KEY_ID_SERVER
#!   nix-shell --keep AWS_ACCOUNT_ID
#!   nix-shell --keep AWS_CLOUDFRONT_DOMAIN
#!   nix-shell --keep AWS_REGION
#!   nix-shell --keep AWS_SECRET_ACCESS_KEY_ADMIN
#!   nix-shell --keep AWS_SECRET_ACCESS_KEY_SERVER
#!   nix-shell --keep GOOGLE_OAUTH_CLIENT_ID_SERVER
#!   nix-shell --keep GOOGLE_OAUTH_SECRET_SERVER
#!   nix-shell --keep SERVER_SESSION_SECRET
#!   nix-shell --pure
#!   nix-shell ../../cmd/back-deploy
#  shellcheck shell=bash

source "${srcBuildCtxLibSh}"

function main {
  export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID_ADMIN}"
  export AWS_ACCOUNT_ID
  export AWS_REGION
  export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY_ADMIN}"
  local registry="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
  local target="${registry}/four_shells:latest"

      echo "[INFO] Loading: ${oci}" \
  &&  docker load --input "${oci}" \
  &&  echo "[INFO] Tagging: ${target}" \
  &&  docker tag 'oci' "${target}" \
  &&  echo "[INFO] Testing image" \
  &&  docker run \
        --interactive \
        --publish 8400:8400 \
        --tty \
        "${target}" \
        4s \
        server \
        --aws-access-key-id "${AWS_ACCESS_KEY_ID_SERVER}" \
        --aws-cloudfront-domain "${AWS_CLOUDFRONT_DOMAIN}" \
        --aws-region "${AWS_REGION}" \
        --aws-secret-access-key "${AWS_SECRET_ACCESS_KEY_SERVER}" \
        --google-oauth-client-id "${GOOGLE_OAUTH_CLIENT_ID_SERVER}" \
        --google-oauth-secret "${GOOGLE_OAUTH_SECRET_SERVER}" \
        --host '0.0.0.0' \
        --port '8400' \
        --production \
        --session-secret "${SERVER_SESSION_SECRET}" \
  &&  echo \
  &&  read -N 1 -p '[INFO] Press any key to deploy oci image' -r \
  &&  echo \
  &&  echo "[INFO] Authenticating to: ${registry}" \
  &&  aws ecr get-login-password --region "${AWS_REGION}" \
        | docker login --username AWS --password-stdin "${registry}" \
  &&  echo "[INFO] Pushing: ${target}" \
  &&  docker push "${target}" \
  &&  echo \
  &&  read -N 1 -p '[INFO] Press any key to rollout deployment' -r \
  &&  echo \
  &&  echo "[INFO] Rolling out to production" \
  &&  aws ecs update-service \
        --cluster four_shells \
        --force-new-deployment \
        --service four_shells \
      | cat \

}

main "${@}"
