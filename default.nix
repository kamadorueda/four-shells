let
  sources = import ./build/deps/sources.nix;
  nixpkgs = import sources.nixpkgs { };
in
  nixpkgs.stdenv.mkDerivation rec {
    installPhase = ''
      in=$out/in/4shells

      mkdir -p $in
      mkdir -p $out/bin

      cp -r $src/* $in

      for binary in 4shells
      do
        echo cd $in \&\& ./bin/$binary > $out/bin/$binary
        chmod +x $out/bin/$binary
      done
    '';
    meta = with nixpkgs.stdenv.lib; {
      description = "";
      homepage = "https://4shells.com";
      license = null;
      maintainers = with maintainers; [
        kamadorueda
      ];
    };
    name = "4shells";
    src = builtins.path {
      inherit name;
      path = ./.;
    };
    version = "2020.11";
  }
