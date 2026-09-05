#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
repo_root="$(cd -- "$script_dir/.." && pwd -P)"

source_file="$repo_root/agents/global/AGENTS.md"
codex_dir="${CODEX_HOME:-$HOME/.codex}"
target_file="$codex_dir/AGENTS.md"

if [[ ! -f "$source_file" ]]; then
    echo "Error: source file not found:"
    echo "  $source_file"
    exit 1
fi

mkdir -p "$codex_dir"

if [[ -L "$target_file" ]]; then
    current_target="$(readlink "$target_file")"

    if [[ "$current_target" == "$source_file" ]]; then
        echo "Already installed:"
        echo "  $target_file -> $source_file"
        exit 0
    fi

    echo "Error: another symbolic link already exists:"
    echo "  $target_file -> $current_target"
    echo
    echo "Remove or rename it manually, then run this script again."
    exit 1
fi

if [[ -e "$target_file" ]]; then
    echo "Error: an existing AGENTS.md was found:"
    echo "  $target_file"
    echo
    echo "It was not overwritten."
    echo "Merge, rename, or remove it manually, then run this script again."
    exit 1
fi

ln -s "$source_file" "$target_file"

echo "Installed global AGENTS.md:"
echo "  $target_file -> $source_file"