# Global Codex Instructions

`AGENTS.md` は、私用の Codex 共通指示の正本です。リポジトリごとの
ルールではなく、会話の書き方、HTML 作成時の方針、完了時の確認手順など、
どの作業ディレクトリでも一貫して適用したい内容を置きます。

## 導入

リポジトリの root で、POSIX 互換の shell（macOS/Linux の Terminal、WSL、
または Git Bash）から次を実行します。

```bash
./scripts/install-agents.sh
```

この script は `~/.codex/AGENTS.md` からこのディレクトリの `AGENTS.md` へ
symbolic link を作成します。既存の file や別の link は上書きしません。同じ
link がすでに存在するときは、そのまま成功として終了します。

導入後は source の `AGENTS.md` を更新すればよく、再インストールは不要です。
ただし、clone したリポジトリを移動または削除すると link が無効になるため、
再度この script を実行してください。

## 適用範囲

Codex は `~/.codex/AGENTS.md` をグローバル指示として読み込み、作業場所に
近いリポジトリ内の `AGENTS.md` はそれより優先されます。したがって、ここには
個人の恒久的な作業方針だけを記載します。特定の codebase の build command、
directory layout、team rule は、その repository の root または適切な下位
directory の `AGENTS.md` に置いてください。

指示そのものを変更するときは [AGENTS.md](AGENTS.md) を編集します。この README
は導入方法と適用範囲の説明であり、指示内容の複製ではありません。

## 関連資料

- [Repository development guide](../../docs/development.md)
- [OpenAI Docs: AGENTS.md によるカスタム指示](https://learn.chatgpt.com/ja-JP/docs/agent-configuration/agents-md)
