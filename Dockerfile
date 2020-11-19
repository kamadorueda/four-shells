# syntax=docker/dockerfile:experimental

# Base alpine image configured with Nix
FROM nixos/nix:2.3

ENV FOUR_SHELLS_REPO https://github.com/kamadorueda/4shells.com
ENV FOUR_SHELLS_REV c62f34fee27217956248451005b7710e52313f5d

ENV NIX_IPFS_REPO https://github.com/kamadorueda/nix-ipfs
ENV NIX_IPFS_REV 2194b0e727bca15163e760c3c13592c7c29f285d

# Install all products from their respective sources
RUN   true \
  &&  nix-env -i -f "${FOUR_SHELLS_REPO}/archive/${FOUR_SHELLS_REV}.tar.gz" \
  &&  nix-env -i -f "${NIX_IPFS_REPO}/archive/${NIX_IPFS_REV}.tar.gz" \
  &&  nix-store --optimise

# Metadata
LABEL 'org.opencontainers.image.source' 'https://github.com/kamadorueda/4shells.com'
