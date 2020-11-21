source "${stdenv}/setup"

mkdir "${out}"

cp --no-target-directory --recursive "${srcBin}" "${out}/bin"
cp --no-target-directory --recursive "${srcBuild}" "${out}/build"
cp --no-target-directory --recursive "${srcServer}" "${out}/server"

chmod +x "${out}/bin/${bin}"
