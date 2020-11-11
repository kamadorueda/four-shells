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
      cp -r "$repoSrc" "$out/src"
    '';

    name = "nix-ipfs";

    repoBin = ./bin;
    repoBuild = ./build;
    repoSrc= ./src;

    src = repoBin;
  }
