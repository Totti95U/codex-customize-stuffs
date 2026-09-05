# Development Guide

このドキュメントでは、`codex-customize-stuffs` に含まれる `AGENTS.md`、skills、plugins、marketplace の開発・検証・導入方法を説明する。

## Repository layout

```text
codex-customize-stuffs/
├── AGENTS.md
├── agents/
│   ├── global/
│   │   └── AGENTS.md
│   └── presets/
├── plugins/
│   └── <plugin-name>/
│       ├── .codex-plugin/
│       │   └── plugin.json
│       ├── skills/
│       │   └── <skill-name>/
│       │       ├── SKILL.md
│       │       ├── agents/
│       │       │   └── openai.yaml
│       │       ├── references/
│       │       ├── scripts/
│       │       └── assets/
│       └── README.md
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── scripts/
│   ├── install-agents.sh
│   └── link-skills.sh
└── docs/
    └── development.md
```

各 directory の役割は次のとおり。

- `AGENTS.md`
  - この repository を Codex が編集するときに適用される指示。
  - 配布用の global instructions ではない。
- `agents/global/AGENTS.md`
  - 個人環境の `~/.codex/AGENTS.md` として使用する global instructions の原本。
- `agents/presets/`
  - 用途別・project 別に導入できる `AGENTS.md` の雛形。
- `plugins/`
  - ChatGPT と Codex に配布する plugin の原本。
- `plugins/<plugin-name>/skills/`
  - plugin に含める skill の原本。
  - 同じ skill の standalone 用コピーを別 directory に作らない。
- `.agents/plugins/marketplace.json`
  - この repository に含まれる plugins の catalog。
- `scripts/`
  - global instructions や standalone skills を local environment に導入する補助 script。

## Source-of-truth policy

配布対象 skill の唯一の原本は、次の場所に置く。

```text
plugins/<plugin-name>/skills/<skill-name>/
```

standalone skill として使用するためだけに、同じ `SKILL.md` を別の directory へコピーしてはならない。

Codex CLI や IDE extension で standalone skill が必要な場合は、`scripts/link-skills.sh` を使って plugin 内の skill directory への symbolic link を作成する。

plugin 版と symbolic link 版の同じ skill を同時に有効化すると、同名 skill が重複して表示される可能性がある。通常は次のいずれか一方を使用する。

- ChatGPT または plugin 対応 Codex：plugin を install する
- Codex IDE extension または standalone 開発：`link-skills.sh` を使用する

## Adding a skill

新しい skill を追加するときは、最初にどの plugin に属するかを決める。

既存 plugin と目的、更新単位、依存関係が共通する場合は、その plugin の `skills/` に追加する。

```text
plugins/<plugin-name>/skills/<skill-name>/SKILL.md
```

既存 plugin から独立して install、公開、versioning したい場合は、新しい plugin を作成する。

各 skill は最低限、次の形式の `SKILL.md` を持つ。

```yaml
---
name: example-skill
description: Describe what this skill does and when it should or should not be used.
---

Instructions for completing the workflow.
```

skill の `name` は repository 内で一意な kebab-case 名にする。

`description` には次を簡潔に記載する。

- skill が達成する user goal
- 発火させるべき状況
- 必要であれば、発火させるべきでない状況

詳細な説明、長い例、仕様書は `SKILL.md` に詰め込まず、必要に応じて以下へ分離する。

- `references/`：補足文書、仕様、長い例
- `scripts/`：決定的に実行する必要がある処理
- `assets/`：template、画像、starter file
- `agents/openai.yaml`：表示情報、implicit invocation policy、tool dependencies

## Adding a plugin

新しい plugin は次の構造で作成する。

```text
plugins/<plugin-name>/
├── .codex-plugin/
│   └── plugin.json
└── skills/
    └── <skill-name>/
        └── SKILL.md
```

最小の `plugin.json` は次の形式とする。

```json
{
  "name": "example-plugin",
  "version": "0.1.0",
  "description": "Describe the capability provided by this plugin.",
  "repository": "https://github.com/Totti95U/codex-customize-stuffs",
  "license": "MIT",
  "skills": "./skills/"
}
```

次の名前を一致させる。

- `plugins/<plugin-name>/` の directory 名
- `plugin.json` の `name`
- `marketplace.json` の plugin entry にある `name`
- `marketplace.json` の `source.path`

plugin を追加または rename した場合は、`.agents/plugins/marketplace.json` も同じ変更内で更新する。

MCP server、hooks、UI、外部 service を利用しない skills-only plugin には、不要な `.mcp.json`、`.app.json`、`hooks/` を追加しない。

## Updating the marketplace

repository の marketplace は次に置く。

```text
.agents/plugins/marketplace.json
```

plugin ごとに `plugins` 配列へ一つの entry を追加する。

```json
{
  "name": "example-plugin",
  "source": {
    "source": "local",
    "path": "./plugins/example-plugin"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Productivity"
}
```

`source.path` は repository root を基準とする `./` 始まりの相対 path にする。repository の外部を参照する path や、開発者個人の絶対 path を記載しない。

## Local setup

repository を clone する。

```bash
git clone https://github.com/Totti95U/codex-customize-stuffs.git
cd codex-customize-stuffs
```

### Install global AGENTS.md

```bash
./scripts/install-agents.sh
```

この script は次の symbolic link を作成する。

```text
~/.codex/AGENTS.md
    -> agents/global/AGENTS.md
```

既存の `~/.codex/AGENTS.md` がある場合、script は上書きせず終了する。既存内容を確認し、手動で統合または退避してから再実行する。

repository を移動または削除すると symbolic link が切れるため、clone 先は安定した場所にする。

### Link standalone skills

```bash
./scripts/link-skills.sh
```

この script は、次の pattern に一致するすべての skill を検出する。

```text
plugins/*/skills/*/SKILL.md
```

各 skill directory への symbolic link を次に作成する。

```text
~/.agents/skills/<skill-name>
```

既存 file、directory、または別の symbolic link と衝突した場合は上書きしない。

### Add the plugin marketplace

```bash
codex plugin marketplace add Totti95U/codex-customize-stuffs --ref main
```

登録状態を確認する。

```bash
codex plugin marketplace list
```

repository または marketplace を更新した後は、必要に応じて次を実行する。

```bash
codex plugin marketplace upgrade totti95u-customizations
```

marketplace 名が異なる場合は、`codex plugin marketplace list` に表示された名前を使用する。

ChatGPT desktop app で local plugin を更新した場合は、app を再起動し、新しい conversation で動作を確認する。

## Validation

変更内容に応じて、少なくとも以下を確認する。

### JSON

```bash
python -m json.tool .agents/plugins/marketplace.json >/dev/null
```

各 plugin manifest も検証する。

```bash
find plugins -path '*/.codex-plugin/plugin.json' -print0 |
  while IFS= read -r -d '' file; do
    python -m json.tool "$file" >/dev/null
  done
```

### Shell scripts

```bash
bash -n scripts/*.sh
```

可能であれば、既存 file を上書きしないことと、二度実行しても安全であることを一時的な environment で確認する。

### Skills

各 skill について、次を確認する。

- `SKILL.md` が存在する
- frontmatter に `name` と `description` がある
- skill 名が repository 内で重複していない
- `description` が発火条件を具体的に表している
- `SKILL.md` から参照する file が存在する
- local machine 固有の絶対 path に依存していない
- credentials、tokens、個人情報を含んでいない
- 明示的な呼び出しで期待どおり動作する
- 関係のない request で暗黙に発火しない

### Plugins

各 plugin について、次を確認する。

- `.codex-plugin/plugin.json` が存在する
- `name`、`version`、`description` が設定されている
- `skills` が正しい相対 path を参照している
- marketplace の `name` と `source.path` が一致している
- plugin を新しい conversation で install して代表的な request を試した
- skill が使われるべき positive case と、使われるべきでない negative case の両方を試した

## Versioning

plugin の公開上の変更は、`plugin.json` の `version` を更新する。

version は Semantic Versioning を基本とする。

- patch：誤字修正、説明改善、互換性のある軽微な調整
- minor：新しい skill や後方互換性のある機能追加
- major：既存の発火条件、入力、出力、依存関係を大きく変える変更

開発中の local-only 修正では、すべての commit で version を上げる必要はない。配布または release する単位で version を更新する。

利用者に影響する変更がある場合は、plugin directory 内の `CHANGELOG.md` または repository の release notes に記録する。

## Security and portability

repository には次を commit しない。

- API keys、access tokens、passwords
- OAuth client secrets
- private certificates
- local machine 固有の絶対 path
- user-specific cache
- generated credentials
- plugin installation cache

`.app.json` や `.mcp.json` を追加するときは、identifier と secret を区別する。公開可否が不明な値は commit する前に確認する。

scripts は既存の user file を無断で削除または上書きしてはならない。衝突を検出した場合は、対象 path を表示して終了する。

## Maintenance policy

同じ説明を `README.md`、`development.md`、`AGENTS.md`、各 plugin の `README.md` に重複して記載しない。

- `README.md`：repository の概要と導入への入口
- `docs/development.md`：詳細な開発・検証手順
- root `AGENTS.md`：Codex が常に守る短い規約
- plugin の `README.md`：その plugin 固有の目的、使い方、test cases

実装や運用方法が変わった場合は、関連する documentation も同じ変更内で更新する。

Codex の作業中に、将来も繰り返し適用すべき repository-wide rule が判明した場合のみ、root `AGENTS.md` の更新を検討する。一度限りの作業内容や進捗記録は `AGENTS.md` に追加しない。

## References

- [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Package your plugin](https://developers.openai.com/plugins/build/plugins)