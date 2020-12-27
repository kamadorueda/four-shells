# shellcheck shell=bash

function utils_clone_repo {
  local source="${1}"
  local target="${2}"

  if test -e "${target}"
  then
        echo "[INFO] Updating local repository copy at: ${target}" \
    &&  pushd "${target}" \
      &&  git remote set-url origin "${source}" \
      &&  git fetch -a \
      &&  git reset --hard HEAD \
    &&  popd \
    ||  return 1
  else
        echo "[INFO] Creating local repository copy at: ${target}" \
    &&  git clone "${source}" "${target}" \
    &&  pushd "${target}" \
      &&  git fetch -a \
      &&  git reset --hard HEAD \
    &&  popd \
    ||  return 1
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

function utils_ensure_configuration {
      echo 'Configuration:' \
  &&  echo \
  &&  for var in "${@}"
      do
            utils_ensure_variable "${var}" \
        &&  echo "${var} = ${!var}" \
        ||  return 1
      done \
  &&  echo
}

function utils_ensure_variable {
  local var="${1}"

  if test -z "${!var:-}"
  then
        echo "Please export ${var} as environment variable" \
    &&  return 1
  fi
}

function utils_terraform_prepare {
      echo '[INFO] Formatting' \
  &&  terraform fmt -recursive . \
  &&  if ! test -e .terraform/
      then
            echo '[INFO] Initializing' \
        &&  terraform init
      fi \
  &&  echo '[INFO] Linting' \
  &&  tflint --config tflint.hcl \
  &&  echo '[INFO] Generating dependency graph' \
  &&  terraform graph | dot -o ../infra/dependency-graph.svg -T svg /dev/stdin
}
