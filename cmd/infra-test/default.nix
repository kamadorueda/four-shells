let
  sources = import ../../sources.nix;
  nixpkgs = import sources.nixpkgs { };
in
  nixpkgs.stdenv.mkDerivation (
       (import ../../build/ctx)
    // (rec {
      name = "infra-test";

      buildInputs = [
        nixpkgs.graphviz
        nixpkgs.terraform_0_13
        nixpkgs.tflint
      ];
    })
  )
