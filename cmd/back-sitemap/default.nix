let
  nixpkgs = import sources.nixpkgs { };
  sources = import ../../sources.nix;
in
  nixpkgs.stdenv.mkDerivation (
       (import ../../build/ctx)
    // (rec {
      name = "back-sitemap";

      buildInputs = [
        nixpkgs.git
        nixpkgs.python38
        nixpkgs.python38Packages.more-itertools
      ];
    })
  )
