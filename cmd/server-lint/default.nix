let
  sources = import ../../sources.nix;
  nixpkgs = import sources.nixpkgs { };
  py-deps = import ../../build/py-deps;
  bin = import ../../build/bin;
in
  nixpkgs.stdenv.mkDerivation (
       (import ../../build/ctx)
    // (rec {
      name = "server-lint";

      buildInputs = bin.dependencies.fourShells ++ [
        nixpkgs.mypy
        py-deps.derivations.prospector
      ];

      srcServerBack = ../../server/back;
    })
  )
