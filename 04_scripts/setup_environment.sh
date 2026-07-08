#!/usr/bin/env bash
set -e
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_PREFIX="$PROJECT_ROOT/.conda"
conda env create --prefix "$ENV_PREFIX" --file "$PROJECT_ROOT/environment.yml"
echo "Environment created at: $ENV_PREFIX"
echo "Activate with:"
echo "conda activate $ENV_PREFIX"
