let
  back = import ../../back;
  sources = import ../../sources.nix;
  nixpkgs = import sources.nixpkgs { };
  py-deps = import ../../build/py-deps;
in
  nixpkgs.stdenv.mkDerivation (
       (import ../../build/ctx)
    // (rec {
      name = "back-lint";

      buildInputs = builtins.concatLists [
        back.dependencies
        [
          nixpkgs.mypy
          py-deps.derivations.prospector
        ]
      ];

      srcBack = ../../back;
    })
  )
