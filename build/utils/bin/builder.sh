#  shellcheck shell=bash

source "${stdenv}/setup"

mkdir "${out}"
mkdir "${out}/bin"

cp --no-target-directory --recursive "${srcBuild}" "${out}/build"
cp --no-target-directory --recursive "${srcServer}" "${out}/server"

{
  # Patch shebang
  echo "${shebang}"
  echo

  # Append required environment variables
  for var in \
    PATH \
    PYTHONPATH \
    srcBin \
    srcBuild \
    srcBuildUtilsCtxLibSh \
    srcBuildUtilsFourShellsLibSh \
    srcBuildUtilsCommonLibSh \
    srcBuildUtilsShoptsLibSh \
    srcServer \

  do
    echo "export ${var}='${!var}'"
  done
  echo

  # Append original script
  echo '# Original script starts below'
  echo '#'
  cat "${srcBin}/${pname}"
} > "${out}/bin/${pname}"

# Make executable
chmod +x "${out}/bin/${pname}"

# Display result
cat "${out}/bin/${pname}"
