let
  sources = import ../../build/deps/nix/sources.nix;
  nixpkgs = import sources.nixpkgs { };
in
  nixpkgs.stdenv.mkDerivation (
       (import ../../build/deps/ctx.nix)
    // (rec {
      name = "server-lint";

      buildInputs = [
        nixpkgs.mypy
      ];
    })
  )
