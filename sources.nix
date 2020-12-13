let
  pkgs = import <nixpkgs> { };
in
  {
    nixpkgs = pkgs.fetchzip {
      url = "https://github.com/NixOS/nixpkgs/archive/712c2405b1c4ddf461a1eafd640165583d1c0cca.zip";
      sha256 = "0p7pasfl0smbphqjm7x59f35vhl5r4r3l5i51pw07hmaxwf22529";
    };
  }
