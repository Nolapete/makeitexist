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
            pkgs.curl
            
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

            # Check if coderabbit is installed and in the PATH when entering the shell
            if ! command -v coderabbit &> /dev/null; then
              echo "CodeRabbit CLI not found. Ensure it's installed (e.g., via the curl script) and in your PATH."
            else
              echo "CodeRabbit CLI available."
            fi

            # Define an alias to quickly check all ignored files (updated for recursive check)
            alias ci="bash -c \"{ git ls-files || git ls-files --others --exclude-standard; } | git check-ignore --verbose --stdin > gitignore_report.log 2>&1 && echo -e 'Report written to gitignore_report.log\\ngitignore check complete.'\""

            # Function to mark a file as locally unchanged (stops showing in git status)
            # Usage: au <file>
            au() { git update-index --assume-unchanged "$@"; }
            
            # Function to revert 'assume-unchanged' status
            # Usage: ac <file>
            ac() { git update-index --no-assume-unchanged "$@"; }
            
          '';

        };
      });
    };
}
