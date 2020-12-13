#  shellcheck shell=bash

source "${stdenv}/setup"
source "${srcBuildUtilsCtxLibSh}"

mkdir "${out}"
mkdir "${out}/bin"
mkdir "${out}/build"
mkdir "${out}/server"

cp --no-target-directory --recursive "${srcBuild}" "${out}/build"
cp --no-target-directory --recursive "${srcClient}" "${out}/client"
cp --no-target-directory --recursive "${srcServerBack}" "${out}/server/back"
cp --no-target-directory --recursive "${srcServerPublic}" "${out}/server/public"

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
    srcBuildUtilsServerLibSh \
    srcBuildUtilsCommonLibSh \
    srcBuildUtilsShoptsLibSh \
    srcClient \
    srcServerBack \
    srcServerPublic \

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
