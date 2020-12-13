let
  math = import ../build/math;
  nixpkgs = import sources.nixpkgs { };
  sources = import ../sources.nix;
in
  rec {
    dependencies = [
      nixpkgs.python38
      nixpkgs.python38Packages.aioextensions
      nixpkgs.python38Packages.boto3
      nixpkgs.python38Packages.authlib
      nixpkgs.python38Packages.httpx
      nixpkgs.python38Packages.starlette
      nixpkgs.python38Packages.uvloop
    ];
    derivation = nixpkgs.stdenv.mkDerivation (
        (import ../build/ctx)
      // (rec {
        binary = ./bin;
        builder = ../build/lib/replace.sh;
        buildInputs = dependencies;
        meta = with nixpkgs.stdenv.lib; {
          description = "Four Shells Server Back-End";
          homepage = "https://4shells.com";
          license = licenses.gpl3;
          maintainers = with maintainers; [ kamadorueda ];
        };
        pname = "4s";
        shebang = "#! ${nixpkgs.bash}/bin/bash";
        srcBuild = ../build;
        srcBack = ../back;
        version = "${math.currentYearStr}.12";
      })
    );
  }
