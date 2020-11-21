let
  sources = import ../build/deps/nix/sources.nix;
  nixpkgs = import sources.nixpkgs { };
in
  nixpkgs.stdenv.mkDerivation (
       (import ../build/deps/ctx.nix)
    // (rec {
      name = "4shells";

      buildInputs = [
        nixpkgs.aioextensions
        nixpkgs.cacert
        nixpkgs.ipfs
        nixpkgs.python38
        nixpkgs.python38Packages.aiohttp
        nixpkgs.python38Packages.starlette
        nixpkgs.python38Packages.uvicorn
        nixpkgs.python38Packages.uvloop
      ];

      repoSrcFourShells = ../src/4shells;
    })
  )
