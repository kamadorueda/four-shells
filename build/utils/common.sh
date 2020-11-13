# shellcheck shell=bash

function utils_ensure_variable {
  local var="${1}"

  if test -z "${!var:-}"
  then
        echo "Please export ${var} as environment variable" \
    &&  return 1
  fi
}

function utils_configure_proxy {
  local port="${1}"

  if test -n "${port}"
  then
        echo "Using BURP proxy: http://127.0.0.1:${port}" \
    &&  export HTTP_PROXY="http://127.0.0.1:${port}" \
    &&  export HTTPS_PROXY="http://127.0.0.1:${port}"
  fi
}
