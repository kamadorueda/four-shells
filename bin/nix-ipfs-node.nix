let
  sources = import ../build/deps/sources.nix;
  nixpkgs = import sources.nixpkgs { };
in
  nixpkgs.stdenv.mkDerivation rec {
    name = "nix-ipfs-node";

    buildInputs = [
    ];
  }
