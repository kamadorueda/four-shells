let
  sources = import ./sources.nix;
  nixpkgs = import sources.nixpkgs { };
in
  nixpkgs.stdenv.mkDerivation (
       (import ./ctx.nix)
    // (rec {
      name = "redis-local";

      buildInputs = [
        nixpkgs.redis
      ];
    })
  )
