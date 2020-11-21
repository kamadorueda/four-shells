# Base alpine image configured with Nix
FROM nixos/nix:2.3

# Metadata
LABEL 'org.opencontainers.image.source' 'https://github.com/kamadorueda/4shells.com'

# Constants
ENV FOUR_SHELLS_REPO https://github.com/kamadorueda/4shells.com
ENV FOUR_SHELLS_REV a5e434b5acc5cd1c26f0f9509f71fa2482b4b720

# Install all products from their respective sources
RUN   true \
  &&  nix-env -i -f "${FOUR_SHELLS_REPO}/archive/${FOUR_SHELLS_REV}.tar.gz" \
  &&  nix-store --optimise

# Interpreter for commands
ENTRYPOINT ["sh", "-c"]
