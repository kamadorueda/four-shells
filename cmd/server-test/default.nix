let
  sources = import ../../build/deps/nix/sources.nix;
  nixpkgs = import sources.nixpkgs { };
  bin = import ../../build/utils/bin;
in
  nixpkgs.stdenv.mkDerivation (
       (import ../../build/utils/ctx)
    // (rec {
      name = "server-test";

      buildInputs = bin.dependencies.fourShells ++ [
        nixpkgs.python38Packages.pytest
        nixpkgs.python38Packages.pytestcov
      ];

      srcServerBack = ../../server/back;
      srcServerPublic = ../../server/public;
    })
  )
