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
├── hooks/
│   ├── hooks.json
│   └── scripts/
├── policies/
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
├── pets/
│    └── <pet-slug>/
│       ├── README.md
│       ├── recipe.md
│       ├── references/
│       ├── package/
│       │   ├── pet.json
│       │   ├── spritesheet.webp
│       │   ├── validation.json
│       │   ├── contact-sheet.png
│       │   └── look-directions.png
│       ├── previews/
│       │   └── animation.gif
│       └── CHANGELOG.md (optional)
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── scripts/
│   ├── install-agents.sh
│   ├── link-skills.sh
│   └── render-pet-preview.py
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
- `pets/`
  - Pet の生成済み instance を置く。Pet-generation skill は作成・更新の workflow であり、Pet 自体の保存場所ではない。
  - sprite sheet、manifest、validation result、preview は各 `pets/<pet-slug>/` に置き、skill や plugin に含めない。
- `pets/<pet-slug>/`
  - 一つの custom Pet を表す最小の管理単位。既存 Pet を更新するときは directory を作り直さず、`package/pet.json` の stable ID を維持して更新する。
  - `README.md` には Pet の紹介、`recipe.md` には再生成に必要な character・motion・制約、`references/` には参照画像や補足資料を置く。
- `pets/<pet-slug>/package/`
  - 配布・登録に使う完成 bundle。`pet.json`、sprite sheet、validation result と、確認用の contact sheet・look directions をまとめる。
- `pets/<pet-slug>/previews/`
  - 人間が animation を確認するための生成物を置く。sprite sheet を変更したら preview も更新する。
- `pets/<pet-slug>/references/`
  - Pet の仕様書、長い例、補足文書。
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

## Pet artifacts

Pet-generation skill で作るのは workflow である。
生成した Pet の完成品と再現に必要な情報は `pets/<pet-slug>/` に残す。

- 既存 custom Pet の名前、説明、sprite sheet を更新するときも、stable ID は `package/pet.json` の `id` を引き継ぐ。
- 登録済み Pet を削除する必要がある場合は、明示的な削除依頼を確認する。
- sprite sheet を更新したら、validator の結果と preview を更新し、animation と look directions を目視確認する。
- Git には完成 bundle、選択した preview、recipe、再現に必要な reference を残す。途中生成物は必要に応じて local Library に置く。
- 期限付きの sprite-sheet URL、upload session ID、credential、account 固有の deployment state は commit しない。

### Render an animation preview

`scripts/render-pet-preview.py` は sprite sheet の標準 animation rows から、状態名付きの loop GIF を生成する。
実行場所は repository root とする。

初回だけ、実行する Python environment に Pillow を導入する。

```bash
python -m pip install Pillow
```

次のように、入力 sprite sheet と出力 GIF の順に渡す。

```bash
python scripts/render-pet-preview.py \
  pets/toe-toe/package/spritesheet.webp \
  pets/toe-toe/previews/animation.gif
```

出力先の parent directory がなければ script が作成する。
入力は幅 1536 px、かつ v1 の高さ 1872 px または v2 の高さ 2288 px の atlas に限られる。
生成される GIF には `idle`、`running-right`、`running-left`、`waving`、`jumping`、`failed`、`waiting`、`running`、`review` の標準 9 state を順に収録する。

この preview は animation の連続性を目視確認するためのものであり、bundle の validator を置き換えない。
sprite sheet を変更したら、validation result を確認した後で preview を再生成し、両方を更新する。

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

## Runtime hooks and policies

`hooks/hooks.json` と `hooks/scripts/` は runtime の正本、`policies/` は行動規則の正本とする。
個人用の環境横断ルールなので plugin として配布せず、symbolic link で導入する。
global AGENTS.md に policy 本文を複製する必要はない。

Windows では repository root で次を実行する。

```powershell
py -3 scripts/install-hooks.py
```

macOS/Linux では次を実行する。

```bash
bash scripts/install-hooks.sh
```

Python 3.9 以上を使用する。Windows の symbolic link 作成には Developer Mode または管理者権限が必要になる。
導入先は `CODEX_HOME`、未設定なら `~/.codex`。
検証用には `--codex-home <temporary-directory>` を指定できる。
実運用でこの引数を使う場合は、Codex 起動環境にも同じ `CODEX_HOME` を設定する。

作成する link は次の3つ。

```text
<codex-home>/hooks.json -> <repo>/hooks/hooks.json
<codex-home>/hooks      -> <repo>/hooks/scripts
<codex-home>/policies   -> <repo>/policies
```

既存の file、directory、別の link は上書きしない。
全対象を先に検査し、衝突があれば作成前に終了する。同じ link への再実行は成功する。
作成途中に失敗した場合は、その実行が作った link だけを取り消す。
既存 hook がある場合は内容を確認して手動統合する。自動 merge は行わない。
runtime は自身の実体 path から repository の policy を読むため、起動 directory に依存しない。
repository の移動で link が切れるので、clone 先を維持する。

導入後は Codex の `/hooks` で設定を確認し、必要な trust review を行う。
この script は trust 設定を変更しない。更新後も review が必要になる場合がある。
対応する Codex と接続済み Notion tools が必要で、ChatGPT.com にはこの hook は導入されない。
ChatGPT 用の指示が必要な場合は policy から作成し、更新時に同期する。

時刻判定は毎回の UserPromptSubmit 時点で固定する。19:00〜04:59 JST は ACTIVE、05:00〜18:59 は INACTIVE。
継続中の処理を19時に中断する timer ではない。
正常時には prompt を block せず、Codex が探索を判定して Notion に保存し、一度断る。
昼間も INACTIVE を注入して、同じ会話の過去の夜間状態を解除する。
不正な event、夜間の policy 欠落・空ファイル・読み取り失敗では exit 2 で prompt を停止する。
Python 未導入や timeout など runtime 自体の起動失敗まで防ぐ強制的な security boundary ではない。

例外許可と保存済み判定は会話履歴と Notion の照合に依存する soft gate であり、hook は状態 DB を持たない。
Notion の保存失敗時にも探索は断る。既存 project は毎回更新せず、必要な Item のみ追加する。

検証は次を実行する。

```bash
python -m unittest discover -s hooks/tests -v
python -m json.tool hooks/hooks.json
bash -n scripts/install-hooks.sh
```

新しい Codex 会話では、夜間の新規アイデア、既定作業の完了、保存失敗、初回の例外文句、拒否後の例外、別の探索への再適用、翌朝の解除を確認する。
自動テストは時刻境界と JSON 契約、導入時の衝突・再実行を検証する。Notion の書き込み成功やモデルの意味判定は実機で別途確認する。

仕様参照: [OpenAI Hooks documentation](https://learn.chatgpt.com/docs/hooks)。

## References

- [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Package your plugin](https://developers.openai.com/plugins/build/plugins)
