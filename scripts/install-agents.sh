#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
repo_root="$(cd -- "$script_dir/.." && pwd -P)"

source_file="$repo_root/agents/global/AGENTS.md"

# Git for Windows の uname は MINGW64_NT-10.0-22631 のように Windows build を含む。
# Windows 11 は build 22000 以上。ponytail: WSL など Git Bash 以外では常に false。
is_windows_11() {
    local build

    build="$(uname -s | sed -n 's/.*_NT-10\.0-\([0-9]\{1,\}\).*/\1/p')"

    [[ -n "$build" ]] && [[ "$build" -ge 22000 ]]
}

# $2 が backup のときだけ既存の実ファイルを退避し、それ以外は上書きせず中断する。
install_link() {
    local target_file="$1"
    local on_existing="${2:-abort}"
    local target_dir current_target backup

    target_dir="$(dirname -- "$target_file")"
    mkdir -p "$target_dir"

    if [[ -L "$target_file" ]]; then
        current_target="$(readlink "$target_file")"

        if [[ "$current_target" == "$source_file" ]]; then
            echo "Already installed:"
            echo "  $target_file -> $source_file"
            return 0
        fi

        echo "Error: another symbolic link already exists:"
        echo "  $target_file -> $current_target"
        echo
        echo "Remove or rename it manually, then run this script again."
        return 1
    fi

    if [[ -e "$target_file" ]]; then
        # ln -s がコピーになる環境（Git Bash など）では、同一内容の実ファイルが配置済みの状態。
        if cmp -s -- "$source_file" "$target_file"; then
            echo "Already installed:"
            echo "  $target_file (identical copy of $source_file)"
            return 0
        fi

        if [[ "$on_existing" != "backup" ]]; then
            echo "Error: an existing AGENTS.md was found:"
            echo "  $target_file"
            echo
            echo "It was not overwritten."
            echo "Merge, rename, or remove it manually, then run this script again."
            return 1
        fi

        backup="$target_file.bak"
        if [[ -e "$backup" ]]; then
            backup="$backup.$(date +%Y%m%d%H%M%S)"
        fi

        mv -- "$target_file" "$backup"
        echo "Backed up the existing AGENTS.md:"
        echo "  $backup"
    fi

    ln -s "$source_file" "$target_file"

    echo "Installed global AGENTS.md:"
    echo "  $target_file -> $source_file"
}

if [[ ! -f "$source_file" ]]; then
    echo "Error: source file not found:"
    echo "  $source_file"
    exit 1
fi

install_link "${CODEX_HOME:-$HOME/.codex}/AGENTS.md"

if is_windows_11; then
    install_link "${DSH_HOME:-$HOME/.dsh}/AGENTS.md" backup
fi
