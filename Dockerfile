# syntax=docker/dockerfile:experimental

# Base alpine image configured with Nix
FROM nixos/nix:2.3

# Install all products from their respective sources
RUN   --mount=type=bind,src=./build/deps/sources.json,target=/4shells.com/build/deps/sources.json \
      --mount=type=bind,src=./build/deps/sources.nix,target=/4shells.com/build/deps/sources.nix \
      --mount=type=bind,src=./default.nix,target=/4shells.com/default.nix \
      nix-env \
        --install \
        --file '/4shells.com/default.nix' \
  &&  nix-env \
        --install 'nix-ipfs' \
        --file 'https://github.com/kamadorueda/nix-ipfs/archive/2194b0e727bca15163e760c3c13592c7c29f285d.tar.gz' \
  &&  nix-store --optimise

# Metadata
LABEL 'org.opencontainers.image.source' 'https://github.com/kamadorueda/4shells.com'
