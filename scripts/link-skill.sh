#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
repo_root="$(cd -- "$script_dir/.." && pwd -P)"

skills_dir="$HOME/.agents/skills"

mkdir -p "$skills_dir"

linked_count=0
skipped_count=0
conflict_count=0

for skill_file in "$repo_root"/plugins/*/skills/*/SKILL.md; do
    if [[ ! -f "$skill_file" ]]; then
        continue
    fi

    skill_source="$(dirname "$skill_file")"
    skill_name="$(basename "$skill_source")"
    skill_target="$skills_dir/$skill_name"

    if [[ -L "$skill_target" ]]; then
        current_target="$(readlink "$skill_target")"

        if [[ "$current_target" == "$skill_source" ]]; then
        echo "Already linked: $skill_name"
        skipped_count=$((skipped_count + 1))
        continue
        fi

        echo "Conflict: $skill_name"
        echo "  existing: $skill_target -> $current_target"
        echo "  proposed: $skill_source"
        conflict_count=$((conflict_count + 1))
        continue
    fi

    if [[ -e "$skill_target" ]]; then
        echo "Conflict: $skill_name"
        echo "  $skill_target already exists and is not a symbolic link."
        conflict_count=$((conflict_count + 1))
        continue
    fi

    ln -s "$skill_source" "$skill_target"

    echo "Linked: $skill_name"
    echo "  $skill_target -> $skill_source"
    linked_count=$((linked_count + 1))
done

echo
echo "Summary:"
echo "  linked:   $linked_count"
echo "  existing: $skipped_count"
echo "  conflicts: $conflict_count"

if [[ "$conflict_count" -gt 0 ]]; then
    exit 1
fi