let
  sources = import ./build/deps/sources.nix;
  nixpkgs = import sources.nixpkgs { };
in
  nixpkgs.stdenv.mkDerivation rec {
    builder = builtins.toFile "builder.sh" "echo > $out";
    name = "4shells";
  }
