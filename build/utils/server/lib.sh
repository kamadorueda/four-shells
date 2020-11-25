# shellcheck shell=bash

function utils_server_ensure_configuration {
  local required_vars=(
    AWS_ACCESS_KEY_ID_SERVER
    AWS_REGION
    AWS_SECRET_ACCESS_KEY_SERVER
    GOOGLE_OAUTH_CLIENT_ID_SERVER
    GOOGLE_OAUTH_SECRET_SERVER
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
