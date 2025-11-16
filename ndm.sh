#! /usr/bin/env bash

# A wrapper script to run Django manage.py commands within the Nix develop environment.
# Usage: ./ndm.sh [manage.py commands, e.g., runserver, migrate, check]

# Execute 'nix develop' and pass all arguments to the project's specific python interpreter
nix develop --command .venv/bin/python manage.py "$@"
