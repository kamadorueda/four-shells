let
  math = import ../deps/math.nix;
  sources = import ../deps/nix/sources.nix;
  nixpkgs = import sources.nixpkgs { };

  derive = {
    deps,
    bin,
  }:
    nixpkgs.stdenv.mkDerivation (
        (import ../deps/ctx.nix)
      // (rec {
        pname = bin;
        version = "${math.currentYearStr}.11";

        builder = ./builder.sh;
        buildInputs = deps;

        meta = with nixpkgs.stdenv.lib; {
          description = "";
          homepage = "https://4shells.com/${bin}";
          license = licenses.gpl3;
          maintainers = with maintainers; [ kamadorueda ];
        };

        srcBin = ../../bin;
        srcBuild = ../../build;
        srcServer = ../../server;
      })
    );
in
  {
    attr4Shells = derive {
      bin = "4shells";
      deps = [
        nixpkgs.cacert
        nixpkgs.python38
        nixpkgs.python38Packages.aioextensions
        nixpkgs.python38Packages.starlette
        nixpkgs.python38Packages.uvicorn
        nixpkgs.python38Packages.uvloop
      ];
    };
  }
