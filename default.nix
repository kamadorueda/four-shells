let
  sources = import ./build/deps/sources.nix;
  nixpkgs = import sources.nixpkgs { };
in
  nixpkgs.stdenv.mkDerivation rec {
    installPhase = ''
      mkdir -p "$out"
      mkdir -p "$out/bin"

      install "$repoBin/"* "$out/bin"
      cp -r "$repoBuild" "$out/build"
      cp -r "$repoSrcCoordinator" "$out/src_coordinator"
      cp -r "$repoSrcNode" "$out/src_node"
    '';

    name = "nix-ipfs";

    repoBin = ./bin;
    repoBuild = ./build;
    repoSrcCoordinator= ./src_coordinator;
    repoSrcNode = ./src_node;

    src = repoBin;
  }
