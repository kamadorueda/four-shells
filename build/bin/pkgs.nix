let
  math = import ../deps/math.nix;
  sources = import ../deps/nix/sources.nix;
  nixpkgs = import sources.nixpkgs { };

  utilsDerive = {
    bin,
    deps,
    description,
  }:
    nixpkgs.stdenv.mkDerivation (
        (import ../deps/ctx.nix)
      // (rec {
        pname = bin;
        version = "${math.currentYearStr}.11";

        builder = ./builder.sh;
        buildInputs = deps;

        meta = with nixpkgs.stdenv.lib; {
          description = description;
          homepage = "https://4shells.com/${bin}";
          license = licenses.gpl3;
          maintainers = with maintainers; [ kamadorueda ];
        };

        srcBin = ../../bin;
        srcBuild = ../../build;
        srcServer = ../../server;

        shebang = "#! ${nixpkgs.bash}/bin/bash";
      })
    );
  utilsGetDeps = builtins.getAttr "deps";

  attrs = {
    attrFourShells = {
      bin = "four-shells";
      deps = [
        nixpkgs.cacert
        nixpkgs.python38
        nixpkgs.python38Packages.aioextensions
        nixpkgs.python38Packages.starlette
        nixpkgs.python38Packages.uvicorn
        nixpkgs.python38Packages.uvloop
      ];
      description = "Four Shells server";
    };
  };
  # Map(name -> derivation)
  attrsDerivations = builtins.mapAttrs (k: v: utilsDerive v) attrs;
  # List(derivation)
  attrsDerivationsFullList = builtins.attrValues attrsDerivations;
  # Map(name -> dependencies)
  attrsDependencies = builtins.mapAttrs (k: v: v.deps) attrs;
  # List(dependencies)
  attrsDependenciesFullList = builtins.concatLists (builtins.attrValues attrsDependencies);
in
  rec {
    derivations = attrsDerivations;
    dependencies = attrsDependenciesFullList ++ attrsDerivationsFullList;
  }
