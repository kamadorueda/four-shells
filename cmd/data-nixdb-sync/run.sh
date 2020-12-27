#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --pure
#!   nix-shell ../../cmd/data-nixdb-sync
#  shellcheck shell=bash

source "${srcBuildCtxLibSh}"

function main {
  local root="${PWD}/.."
  local data="${root}/four-shells-data-nixdb"
  local nixpkgs_local="${root}/nixpkgs"
  local nixpkgs_remote='https://github.com/NixOS/nixpkgs.git'
  local rev_data
  local rev_sha
  local rev_shas
  local rev_summary
  local rev_timestamp
  local revs

      rev_data="$(mktemp)" \
  &&  rev_shas="$(mktemp)" \
  &&  revs="$(mktemp)" \
  &&  utils_clone_repo "${nixpkgs_remote}" "${nixpkgs_local}" \
  &&  git -C "${nixpkgs_local}" rev-list \
        --all \
        --alternate-refs \
        --reflog \
        --topo-order \
        > "${revs}" \
  &&  sort < "${revs}" > "${rev_shas}" \
  &&  if ! test -e "${data}"
      then
            echo "[ERROR] Please create a workdir on: ${data}" \
        ||  return 1
      fi \
  &&  mkdir -p "${data}/pkgs" \
  &&  mkdir -p "${data}/revs" \
  &&  while read -r rev_sha
      do
        if ! test -e "${data}/revs/${rev_sha}.json"
        then
              git -C "${nixpkgs_local}" clean -xfd \
          &&  git -C "${nixpkgs_local}" reset --hard "${rev_sha}" \
          &&  rev_summary="$(git -C "${nixpkgs_local}" log -n 1 "${rev_sha}" --format=%s)" \
          &&  rev_timestamp="$(git -C "${nixpkgs_local}" log -n 1 "${rev_sha}" --format=%at)" \
          &&  if nix-env -q -a -f "${nixpkgs_local}" --json > "${rev_data}"
              then
                DATA="${data}" \
                python3.8 'cmd/data-nixdb-sync/sync.py' \
                  --rev-data "${rev_data}" \
                  --rev-sha "${rev_sha}" \
                  --rev-summary "${rev_summary}" \
                  --rev-timestamp "${rev_timestamp}" \
                  --revs "${revs}"
              else
                    echo "[ERROR] Unable to nix-env nixpkgs @ ${rev_sha}" \
                &&  echo -n 'null' > "${data}/revs/${rev_sha}.json"
              fi \
          ||  return 1
        fi
      done < "${rev_shas}"
}

main "${@}"
