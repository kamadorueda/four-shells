#  shellcheck shell=bash

source "${stdenv}/setup"
source "${srcBuildCtxLibSh}"

mkdir "${out}"
mkdir "${out}/bin"
mkdir "${out}/build"
mkdir "${out}/server"

cp --no-target-directory --recursive "${srcBuild}" "${out}/build"
cp --no-target-directory --recursive "${srcBack}" "${out}/back"

{
  # Patch shebang
  echo "${shebang}"
  echo

  # Append required environment variables
  for var in \
    PATH \
    PYTHONPATH \
    srcBuild \
    srcBuildCtxLibSh \
    srcBuildLibCommonSh \
    srcBuildShoptsLibSh \
    srcBack \

  do
    echo "export ${var}='${!var}'"
  done
  echo

  # Append original script
  echo '# Original script starts below'
  echo '#'
  cat "${binary}"
} > "${out}/bin/${pname}"

# Make executable
chmod +x "${out}/bin/${pname}"

# Display result
cat "${out}/bin/${pname}"
