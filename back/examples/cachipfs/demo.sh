#! /usr/bin/env bash

set -e

# Install the Four Shells CLI
nix-env -i 4s -f https://4shells.com/install

# These environment variables are required
if ! test -n "${CACHIPFS_API_TOKEN}"
then
  echo '[ERROR] Please export CACHIPFS_API_TOKEN for this script to work'
  exit 1
fi
if ! test -n "${CACHIPFS_PORT}"
then
  echo '[ERROR] Please export CACHIPFS_PORT for this script to work'
  exit 1
fi

# Check that the CachIPFS daemon is running
if ! curl "http://localhost:${CACHIPFS_PORT}/ping"
then
  echo '[ERROR] Please remember to execute: 4s cachipfs daemon, on another console'
  echo '[ERROR] See https://4shells.com/docs#retrieving-from-ipfs'
  exit 1
fi

# Let's use a Hello World file for the sake of the demo
# We'll put this file in the cache and then retrieve it from there
echo 'Hello World from CachIPFS!' > file
nix_store_path="$(nix add-to-store file)"

# Publish `nix_store_path`
4s cachipfs publish "${nix_store_path}"

# Remove `nix_store_path` from the local machine
nix-store --delete "${nix_store_path}"

# This will fetch `nix_store_path` from IPFS
nix-store \
  --option 'narinfo-cache-negative-ttl' 0 \
  --option 'narinfo-cache-positive-ttl' 0 \
  --option 'extra-substituters' "http://localhost:${CACHIPFS_PORT}" \
  --realise \
  "${nix_store_path}"

# Read the path
cat "${nix_store_path}"
