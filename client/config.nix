let
  sources = import ../build/deps/nix/sources.nix;
  nixpkgs = import sources.nixpkgs { };
in
  {
    reqs = [
      nixpkgs.python38
      nixpkgs.python38Packages.aioextensions
      nixpkgs.python38Packages.starlette
      nixpkgs.python38Packages.uvloop
    ];
  }
