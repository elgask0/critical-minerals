#!/usr/bin/env bash
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_PREFIX="$PROJECT_ROOT/.conda"
conda activate "$ENV_PREFIX"
