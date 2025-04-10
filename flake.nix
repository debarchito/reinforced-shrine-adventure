{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  outputs =
    { nixpkgs, ... }:
    let
      pkgs = import nixpkgs {
        system = "x86_64-linux";
        config.allowUnfree = true;
      };
    in
    {
      devShells."x86_64-linux".default = pkgs.mkShell {
        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
          pkgs.stdenv.cc.cc
          "/run/opengl-driver"
        ];
        venvDir = ".venv";
        packages = with pkgs; [
          python311
          python311Packages.venvShellHook
          python311Packages.pip
          python311Packages.pygame
        ];
      };
    };
}
