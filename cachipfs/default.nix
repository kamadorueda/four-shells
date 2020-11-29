let
  sources = import ./build/deps/sources.nix;
  nixpkgs = import sources.nixpkgs { };
in
  nixpkgs.stdenv.mkDerivation rec {
    installPhase = ''
      in=$out/in/$name

      mkdir -p $in
      mkdir -p $out/bin

      cp -r $src/* $in

      for binary in \
        nix-ipfs-node \
        nix-ipfs-coordinator \

      do
        echo cd $in \&\& ./bin/$binary > $out/bin/$binary
        chmod +x $out/bin/$binary
      done
    '';
    meta = with nixpkgs.stdenv.lib; {
      description = "A Nix implementation of binary caches over IPFS";
      homepage = "https://github.com/kamadorueda/nix-ipfs";
      license = licenses.gpl3;
      maintainers = with maintainers; [
        kamadorueda
      ];
    };
    name = "nix-ipfs";
    src = builtins.path {
      inherit name;
      path = ./.;
    };
    version = "2020.11";
  }
