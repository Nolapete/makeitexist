{
  description = "Ground-up development environment for stjosephaltar using uv/direnv/pre-commit workflow";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11"; 
  };

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs supportedSystems (system: f system);
    in
    {
      devShells = forAllSystems (system: let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };
      in {
        default = pkgs.mkShell {
          # Provide only necessary system tools/libraries for compilation and workflow
          buildInputs = [
            pkgs.python312  # Base Python interpreter
            pkgs.uv          # The uv tool
            pkgs.pre-commit  # The pre-commit tool
            pkgs.git         
            
            # C/Rust compilation dependencies
            pkgs.stdenv.cc   
            pkgs.libffi      
            pkgs.rustc       
            pkgs.cargo
            
            # --- CRITICAL FIX: Add GDAL and GEOS system libraries ---
            pkgs.gdal
            pkgs.geos
          ];

          # --- CRITICAL FIX: Ensure Django finds the libraries at runtime ---
          shellHook = ''
            export LD_LIBRARY_PATH="${pkgs.gdal}/lib:${pkgs.geos}/lib:$LD_LIBRARY_PATH"
          '';

        };
      });
    };
}
