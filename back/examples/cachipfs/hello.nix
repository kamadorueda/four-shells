let
  pkgsHost = import <nixpkgs> { };
  pkgsSrc = pkgsHost.fetchzip {
    url = "https://github.com/nixos/nixpkgs/archive/2c09066dfd1e9f332603993829e128a0261e9840.zip";
    sha256 = "16nzc0h075snk0409wh2paysx0fqs07x0ah4vm10lhhwb5p9i6lf";
  };
  pkgs = import pkgsSrc { };
in
  pkgs.stdenv.mkDerivation {
    name = "hello";
    builder = builtins.toFile "builder" ''
      echo Hello World! > $out
    '';
  }
