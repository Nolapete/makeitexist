{ p, requirementsFile }:
let
  frozenReqs = pkgs.callPackage p.pip2nix {
    inherit requirementsFile;
  };
in
frozenReqs.env
