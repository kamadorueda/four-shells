let
  sources = import ../../sources.nix;
  nixpkgs = import sources.nixpkgs { };

  awscli2 = (import (nixpkgs.fetchzip {
    url = "https://github.com/nixos/nixpkgs/archive/024f5b30e0a3231dbe99c30192f92ba0058d95f5.zip";
    sha256 = "0cdrah6qj0ax65l48l6rsngvbcxhzxn6ywyk341r9pi1m29jc6jd";
  }) { }).awscli2;
in
  nixpkgs.stdenv.mkDerivation (
       (import ../../build/ctx)
    // (rec {
      name = "server-deploy";

      buildInputs = [
        awscli2
        nixpkgs.git
        nixpkgs.nodejs
        nixpkgs.python38Packages.more-itertools
      ];
    })
  )
