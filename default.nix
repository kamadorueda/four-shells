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

    meta = with nixpkgs.stdenv.lib; {
      description = "A Nix implementation of binary caches over IPFS";
      homepage = "https://github.com/kamadorueda/nix-ipfs";
      license = licenses.gpl3;
      maintainers = with maintainers; [
        kamadorueda
      ];
    };

    name = "nix-ipfs";

    repoBin = ./bin;
    repoBuild = ./build;
    repoSrc= ./src;

    src = repoBin;

    version = "2020.11";
  }
