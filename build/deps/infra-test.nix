let
  sources = import ./sources.nix;
  nixpkgs = import sources.nixpkgs { };
in
  nixpkgs.stdenv.mkDerivation (
       (import ./ctx.nix)
    // (rec {
      name = "infra-test";

      buildInputs = [
        nixpkgs.terraform_0_13
        nixpkgs.tflint
      ];
    })
  )
