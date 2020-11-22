let
  sources = import ../../../build/deps/nix/sources.nix;
  nixpkgs = import sources.nixpkgs { };

  build = { reqs, deps, py }:
    nixpkgs.stdenv.mkDerivation (
        (import ../../../build/utils/ctx)
      // (rec {
        name = "build-reqs";
        builder = ./builder.sh;
        buildInputs = deps ++ [ py ];
        reqsStr = builtins.concatStringsSep "\n" reqs;
        reqsFile = builtins.toFile "reqs" reqsStr;
      })
    );
in
  rec {
    configs = {
      prospector = {
        reqs = [
          "astroid==2.4.1"
          "dodgy==0.2.1"
          "flake8==3.8.4"
          "flake8-polyfill==1.0.2"
          "isort==4.3.21"
          "lazy-object-proxy==1.4.3"
          "mccabe==0.6.1"
          "pep8-naming==0.10.0"
          "prospector==1.3.0"
          "pycodestyle==2.6.0"
          "pydocstyle==5.1.1"
          "pyflakes==2.2.0"
          "pylint==2.5.2"
          "pylint-celery==0.3"
          "pylint-django==2.0.15"
          "pylint-flask==0.6"
          "pylint-plugin-utils==0.6"
          "PyYAML==5.3.1"
          "requirements-detector==0.7"
          "setoptconf==0.2.0"
          "six==1.15.0"
          "snowballstemmer==2.0.0"
          "toml==0.10.2"
          "wrapt==1.12.1"
        ];
        deps = [];
        py = nixpkgs.python38;
      };
    };

    derivations = builtins.mapAttrs (pkg: conf: build conf) configs;
  }
