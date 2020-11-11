let
  sources = import ../build/deps/sources.nix;
  nixpkgs = import sources.nixpkgs { };
in
  nixpkgs.stdenv.mkDerivation rec {
    name = "nix-ipfs-node";

    buildInputs = [
      nixpkgs.python38
      nixpkgs.python38Packages.starlette
      nixpkgs.python38Packages.uvicorn
    ];

    repoSrcNixIPFSNode = ../src/nix_ipfs_node;
  }
