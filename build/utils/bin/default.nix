let
  math = import ../../../build/utils/math;
  sources = import ../../../build/deps/nix/sources.nix;
  nixpkgs = import sources.nixpkgs { };
  serverPkgsConfig = import ../../../server/pkgs/config.nix;

  utilsDerive = {
    bin,
    deps,
    description,
  }:
    nixpkgs.stdenv.mkDerivation (
        (import ../../../build/utils/ctx)
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

        srcBin = ../../../bin;
        srcBuild = ../../../build;
        srcServer = ../../../server;

        shebang = "#! ${nixpkgs.bash}/bin/bash";
      })
    );
  utilsGetDeps = builtins.getAttr "deps";
  utilsGetPythonpath = deps: builtins.concatStringsSep ":"  [
    (nixpkgs.lib.makeSearchPath "lib/python3.9/site-packages" deps)
    (nixpkgs.lib.makeSearchPath "lib/python3.8/site-packages" deps)
    (nixpkgs.lib.makeSearchPath "lib/python3.7/site-packages" deps)
    (nixpkgs.lib.makeSearchPath "lib/python3.6/site-packages" deps)
  ];
  attrs = {
    fourShells = {
      bin = "four-shells";
      deps = serverPkgsConfig.reqs;
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
  # Map(name -> pythonpath)
  attrsPythonpaths = builtins.mapAttrs (k: v: utilsGetPythonpath v) attrsDependencies;
in
  rec {
    allDependencies = attrsDependenciesFullList ++ attrsDerivationsFullList;
    dependencies = attrsDependencies;
    derivations = attrsDerivations;
    pythonpaths = attrsPythonpaths;
  }
