let
  sources = import ../../build/deps/nix/sources.nix;
  nixpkgs = import sources.nixpkgs { };
in
  nixpkgs.stdenv.mkDerivation (
       (import ../../build/deps/ctx.nix)
    // (rec {
      name = "infra-test";

      buildInputs = [
        nixpkgs.graphviz
        nixpkgs.terraform_0_13
        nixpkgs.tflint
      ];
    })
  )
