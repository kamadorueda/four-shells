let
  nixpkgs = import sources.nixpkgs { };
  sources = import ../../sources.nix;
in
  nixpkgs.stdenv.mkDerivation (
       (import ../../build/ctx)
    // (rec {
      name = "data-nixdb-sync";

      buildInputs = [
        nixpkgs.cacert
        nixpkgs.git
        nixpkgs.nix
        nixpkgs.python38
      ];
    })
  )
