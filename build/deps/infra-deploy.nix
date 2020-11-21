let
  sources = import ./nix/sources.nix;
  nixpkgs = import sources.nixpkgs { };
in
  nixpkgs.stdenv.mkDerivation (
       (import ./ctx.nix)
    // (rec {
      name = "infra-deploy";

      buildInputs = [
        nixpkgs.graphviz
        nixpkgs.terraform_0_13
        nixpkgs.tflint
      ];
    })
  )
