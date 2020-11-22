let
  configs = [
    (import ../../server/pkgs/four_shells/config.nix)
  ];
in
  {
    reqs = builtins.concatLists (builtins.map (builtins.getAttr "reqs") configs);
  }
