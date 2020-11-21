let
  sources = import ./nix/sources.nix;
  nixpkgs = import sources.nixpkgs { };
in
  nixpkgs.stdenv.mkDerivation (
       (import ./ctx.nix)
    // (rec {
      name = "build-lint";

      buildInputs = [
        nixpkgs.shellcheck
      ];
    })
  )
