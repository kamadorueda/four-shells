let
  sources = import ../../build/deps/nix/sources.nix;
  nixpkgs = import sources.nixpkgs { };
  py-deps = import ../../build/utils/py-deps;
  bin = import ../../build/utils/bin;
in
  nixpkgs.stdenv.mkDerivation (
       (import ../../build/utils/ctx)
    // (rec {
      name = "server-lint";

      buildInputs = bin.dependencies.fourShells ++ [
        nixpkgs.mypy
        py-deps.derivations.prospector
      ];
    })
  )
