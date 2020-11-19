# shellcheck shell=bash

function utils_nix_ipfs_node_ensure_configuration {
  local required_vars=(
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
