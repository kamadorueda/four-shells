# shellcheck shell=bash

function ensure_variable {
  local var="${1}"

  if test -z "${!var:-}"
  then
        echo "Please export ${var} as environment variable" \
    &&  return 1
  fi
}

function ensure_configuration {
      echo 'Configuration:' \
  &&  echo \
  &&  for var in \
        NIX_IPFS_NODE_PORT \
        NIX_IPFS_NODE_SUBSTITUTER \

      do
            ensure_variable "${var}" \
        &&  echo "${var} = ${!var}" \
        ||  return 1
      done \
  &&  echo
}
