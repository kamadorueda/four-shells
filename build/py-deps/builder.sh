#  shellcheck shell=bash

source "${stdenv}/setup"
source "${srcBuildCtxLibSh}"

function main {
      mkdir "${out}" \
  &&  echo '[INFO] Creating virtualenv' \
  &&  python -m venv "${out}" \
  &&  echo '[INFO] Activating virtualenv' \
  &&  source "${out}/bin/activate" \
  &&  echo '[INFO] Installing' \
  &&  python -m pip install --requirement "${reqsFile}" \
  &&  echo '[INFO] Freezing' \
  &&  python -m pip freeze > "${out}/reqs" \
  &&  if test "$(cat "${out}/reqs")" = "$(cat "${reqsFile}")"
      then
        echo '[INFO] Integrity check passed'
      else
            echo '[ERROR] Integrity check failed' \
        &&  echo '[INFO] You need to pin all dependencies:' \
        &&  while read -r req
            do
              echo "\"${req}\""
            done < "${out}/reqs" \
        &&  return 1
      fi \
  &&  rm -f "${out}/reqs" \

}

main
