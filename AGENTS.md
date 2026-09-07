# Repository Guidelines

## Purpose

This repository stores reusable Codex and ChatGPT customizations, including AGENTS.md templates, skills, plugins, and a local plugin marketplace.

Read `docs/development.md` before changing the repository structure, installation scripts, plugin packaging, or marketplace configuration.

## Source of truth

- Treat `plugins/<plugin-name>/skills/<skill-name>/` as the canonical source for every distributable skill.
- Do not create a second standalone copy of a skill. Use symbolic links for standalone Codex installation.
- Treat `agents/global/AGENTS.md` as the source for the user's global Codex instructions.
- Do not confuse `agents/global/AGENTS.md` with this root `AGENTS.md`. This file governs work on this repository only.
- Do not modify `agents/global/AGENTS.md` unless the requested task includes changing the user's global instructions.

## Repository structure

- Store plugins under `plugins/<plugin-name>/`.
- Store plugin manifests at `plugins/<plugin-name>/.codex-plugin/plugin.json`.
- Store plugin skills under `plugins/<plugin-name>/skills/`.
- Store the repository marketplace at `.agents/plugins/marketplace.json`.
- Store reusable AGENTS.md templates under `agents/`.
- Store human-facing development documentation under `docs/`.
- Store installation and maintenance scripts under `scripts/`.
- Store personal runtime hooks under `hooks/` and their canonical behavioral policies under `policies/`; do not duplicate policy bodies in hooks, plugins, or global instructions.

Do not add new top-level directories without a clear repository-wide purpose.

## Skills and plugins

- Use the available skill-creator workflow when creating or substantially changing a skill.
- Use the available plugin-creator workflow when creating or substantially changing a plugin package.
- Keep each skill focused on one recognizable user goal.
- Keep detailed references, examples, scripts, and assets outside `SKILL.md` when they would make its main instructions difficult to scan.
- Keep plugin and skill names stable and use kebab-case.
- Avoid duplicate skill names across plugins.
- When adding or renaming a plugin, update `.agents/plugins/marketplace.json` in the same change.
- Keep the plugin directory name, manifest `name`, marketplace `name`, and marketplace `source.path` consistent.
- Do not add MCP, app, hook, or UI configuration unless the plugin actually requires it.

## Editing rules

- Preserve unrelated user changes in the working tree.
- Make the smallest coherent change that satisfies the request.
- Use relative paths in committed configuration and documentation.
- Do not commit credentials, secrets, machine-specific absolute paths, local caches, or generated installation state.
- Installation scripts must be idempotent and must not overwrite existing user files without explicit confirmation.
- Do not duplicate detailed operational instructions from `docs/development.md` in this file.
- Update relevant documentation when changing repository layout, installation behavior, plugin packaging, or marketplace behavior.

## Validation

Run checks relevant to the changed files.

For JSON changes:

```bash
python -m json.tool .agents/plugins/marketplace.json >/dev/null
find plugins -path '*/.codex-plugin/plugin.json' -print0 |
  while IFS= read -r -d '' file; do
    python -m json.tool "$file" >/dev/null
  done
```

For shell script changes:

```bash
bash -n scripts/*.sh
```

For skill changes, verify that:

- `SKILL.md` contains valid `name` and `description` frontmatter.
- All referenced files exist.
- The description covers both intended triggers and important non-triggers.
- The skill works for representative positive cases.
- The skill does not activate for representative negative cases.

For plugin changes, verify that:

- `.codex-plugin/plugin.json` exists and contains the expected version and paths.
- The marketplace entry resolves to the correct plugin directory.
- The installed plugin works in a new conversation.

If a listed command cannot run because a required tool is unavailable, report that limitation instead of silently skipping validation.

## Versioning and documentation

- Update a plugin version when preparing a distributable release.
- Record user-visible changes in the plugin changelog or release notes.
- Do not increase versions mechanically for every local development commit.
- Keep `README.md` concise and use `docs/development.md` for detailed maintenance instructions.

## Maintaining these instructions

Update this `AGENTS.md` only when a durable repository-wide rule has been established.

Do not add temporary task notes, implementation progress, one-off decisions, or information that belongs in a skill, plugin README, issue, or commit message.

## Pet artifacts

- Store generated Pet projects under `pets/<pet-slug>/`, not inside a skill or plugin directory.
- Treat Pet-generation skills as workflows and Pet directories as generated instances.
- Preserve an existing custom Pet's stable ID when updating its name, description, or sprite sheet.
- Never recreate an existing Pet merely to apply an update.
- Validate and preview a changed sprite sheet before updating the registered Pet.
- Do not commit expiring sprite-sheet URLs, upload session IDs, credentials, or account-local deployment state.
- Do not delete a registered Pet unless the user explicitly requests deletion.
- Keep only selected final artifacts and reproducibility information in Git; generated working files may remain in Library.
