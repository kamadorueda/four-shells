let
  math = import ../../../build/utils/math;
  sources = import ../../../build/deps/nix/sources.nix;
  nixpkgs = import sources.nixpkgs { };
  clientConfig = import ../../../client/config.nix;
  serverBackConfig = import ../../../server/back/config.nix;

  utilsDerive = {
    bin,
    deps,
    description,
  }:
    nixpkgs.stdenv.mkDerivation (
        (import ../../../build/utils/ctx)
      // (rec {
        pname = bin;
        version = "${math.currentYearStr}.12";

        builder = ./builder.sh;
        buildInputs = deps;

        meta = with nixpkgs.stdenv.lib; {
          description = description;
          homepage = "https://4shells.com";
          license = licenses.gpl3;
          maintainers = with maintainers; [ kamadorueda ];
        };

        srcBin = ../../../bin;
        srcBuild = ../../../build;
        srcClient = ../../../client;
        srcServerBack = ../../../server/back;
        srcServerPublic = ../../../server/public;

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
    fourShellsClient = {
      bin = "4s";
      deps = clientConfig.reqs;
      description = "Four Shells Client";
    };
    fourShellsServerBack = {
      bin = "4s-server-back";
      deps = serverBackConfig.reqs;
      description = "Four Shells Server Back-End";
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
