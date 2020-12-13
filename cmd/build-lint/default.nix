let
  sources = import ../../sources.nix;
  nixpkgs = import sources.nixpkgs { };
in
  nixpkgs.stdenv.mkDerivation (
       (import ../../build/ctx)
    // (rec {
      name = "build-lint";

      buildInputs = [
        nixpkgs.shellcheck
      ];
    })
  )
