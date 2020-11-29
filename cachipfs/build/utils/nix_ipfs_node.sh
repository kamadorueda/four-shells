# shellcheck shell=bash

function utils_nix_ipfs_node_ensure_configuration {
  local required_vars=(
    NIX_IPFS_NODE_COORDINATOR_URL
    NIX_IPFS_NODE_DATA_DIR
    NIX_IPFS_NODE_IPFS_API_PORT
    NIX_IPFS_NODE_IPFS_GATEWAY_PORT
    NIX_IPFS_NODE_IPFS_SWARM_PORT
    NIX_IPFS_NODE_PORT
    NIX_IPFS_NODE_SUBSTITUTER
  )

      echo 'Configuration:' \
  &&  echo \
  &&  for var in "${required_vars[@]}"
      do
            utils_ensure_variable "${var}" \
        &&  echo "${var} = ${!var}" \
        ||  return 1
      done \
  &&  echo
}
