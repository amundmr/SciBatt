{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
  };

  outputs = {
    nixpkgs,
    ...
  }: let
    systems = ["x86_64-linux" "aarch64-linux" "aarch64-darwin" "x86_64-darwin"];
    eachSystem = systems: f: let
      op = attrs: system: let
        ret = f system;
        op = attrs: key:
          attrs
          // {
            ${key} =
              (attrs.${key} or {})
              // {${system} = ret.${key};};
          };
      in
        builtins.foldl' op attrs (builtins.attrNames ret);
    in
      builtins.foldl' op {} systems;
  in
    eachSystem systems (system: let
      pkgs = import nixpkgs {inherit system;};
      galvani = pkgs.python3Packages.buildPythonPackage rec {
        pname = "galvani";
        version = "0.4.1";
        nativeBuildInputs = with pkgs.python3Packages; [setuptools pip pytest pkgs.which];
        propagatedBuildInputs = with pkgs.python3Packages; [numpy];
        src = pkgs.python3Packages.fetchPypi {
          inherit pname version;
          sha256 = "sha256-T1ezLB3GFa82IUH6YJfcmGiLc3i3SvjXD6KKdec6F28=";
        };
      };
      gamry_parser = pkgs.python3Packages.buildPythonPackage rec {
        pname = "gamry_parser";
        version = "0.4.6";
        nativeBuildInputs = with pkgs.python3Packages; [setuptools];
        src = pkgs.python3Packages.fetchPypi {
          inherit pname version;
          sha256 = "sha256-NlMQRTXgUnce69ZI6MtEOawAYh/qO56cRbR3faKB1GE=";
        };
        pyproject=true;
      };
    in rec {
      packages.default = pkgs.python3Packages.buildPythonPackage {
        pname = "SciBatt";
        version = "0.0.1";
        pyproject = true;
        src = ./.;

        nativeBuildInputs = with pkgs; [
            hatch
        ];

        propagatedBuildInputs = with pkgs.python3Packages; [
          numpy
          pandas
          matplotlib
          galvani
          gamry_parser
        ];
      };

      devShells.default = pkgs.mkShell {
        packages = with pkgs; [
          (python3.withPackages (p: [packages.default p.pytest p.pip p.pdoc]))
          ruff
        ];
      };
    });
}