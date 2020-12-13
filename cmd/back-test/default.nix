let
  back = import ../../back;
  nixpkgs = import sources.nixpkgs { };
  sources = import ../../sources.nix;
in
  nixpkgs.stdenv.mkDerivation (
       (import ../../build/ctx)
    // (rec {
      name = "server-test";

      buildInputs = builtins.concatLists [
        back.dependencies
        [
          nixpkgs.python38Packages.pytest
          nixpkgs.python38Packages.pytestcov
        ]
      ];

      srcBack = ../../back;
    })
  )
