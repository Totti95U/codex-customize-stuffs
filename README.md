# codex-customize-stuffs

Codex と ChatGPT で使う personal customization をまとめた repository です。
global `AGENTS.md`、project 向けの preset、skills-only plugin、custom Pet を管理します。

## 含まれるもの

- [Global Codex Instructions](agents/global/README.md)：個人環境で共通して使う `AGENTS.md` の原本です。
- `agents/presets/`：development と research 用の `AGENTS.md` preset を置きます。
- [Retitle](plugins/retitle/README.md)：後から探しやすい会話タイトルを提案する plugin です。
- [Maintain AGENTS.md](plugins/maintain-agents-md/README.md)：完了した repository task から、将来も有効な `AGENTS.md` の規約だけを見直す plugin です。
- [トテトテ](pets/toe-toe/README.md)：この repository で管理する custom Pet です。

skills の正本は各 plugin の `skills/<skill-name>/` です。
standalone 用に同じ `SKILL.md` を複製せず、必要に応じて symbolic link を作成します。

## 導入

POSIX 互換 shell（macOS/Linux の Terminal、WSL、または Git Bash）で実行します。

```bash
git clone https://github.com/Totti95U/codex-customize-stuffs.git
cd codex-customize-stuffs
```

global instructions を導入する場合は、次を実行します。

```bash
./scripts/install-agents.sh
```

実行権限がない場合は次を試してください。

```bash
chmod +x scripts/install-agents.sh
./scripts/install-agents.sh
```

この script は `agents/global/AGENTS.md` を `~/.codex/AGENTS.md` に symbolic link として導入します。
既存の file や別の link は上書きしません。

Codex の standalone skill として plugin 内の skills を使う場合は、次を実行します。

```bash
./scripts/link-skill.sh
```

この script は `plugins/*/skills/*/SKILL.md` を検出し、各 skill directory を `~/.agents/skills/<skill-name>` に link します。
plugin 版と standalone 版を同時に有効化すると、同名 skill が重複して表示される場合があります。
通常は、plugin を導入するか standalone link を作るかのどちらか一方を選びます。

repository の plugin marketplace を Codex に追加する場合は、次を実行します。

```bash
codex plugin marketplace add Totti95U/codex-customize-stuffs --ref main
codex plugin marketplace list
```

## 開発と検証

repository の構成、plugin と skill の追加方法、Pet artifact の管理、検証手順は [Development Guide](docs/development.md) にまとめています。
この repository を編集するときに適用する規約は [AGENTS.md](AGENTS.md) を参照してください。

## License

[MIT License](LICENSE)
