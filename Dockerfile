# Base alpine image configured with Nix
FROM nixos/nix:2.3

# Metadata
LABEL 'org.opencontainers.image.source' 'https://github.com/kamadorueda/4shells.com'

# Constants
ENV FOUR_SHELLS_REPO https://github.com/kamadorueda/4shells.com
ENV FOUR_SHELLS_REV c62f34fee27217956248451005b7710e52313f5d

ENV NIX_IPFS_REPO https://github.com/kamadorueda/nix-ipfs
ENV NIX_IPFS_REV aa9b05cf18498c4020a607831876fc5337cd1bfc

# Install all products from their respective sources
RUN   true \
  &&  nix-env -i -f "${FOUR_SHELLS_REPO}/archive/${FOUR_SHELLS_REV}.tar.gz" \
  &&  nix-store --optimise

# Interpreter for commands
ENTRYPOINT ["sh", "-c"]
