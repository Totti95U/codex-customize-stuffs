# Quiz Gate

エージェントの作業を受け入れる前に、その内容を理解しているかを確認する skills-only plugin です。
対象の作業について HTML の briefing を作成して提示し、briefing と実コードに基づく quiz を行い、
すべての設問に正答するまで commit、merge、plan phase の完了、goal の完了を止めます。

外部 service、MCP server、認証、独自 UI は使用しません。workflow の正本は
[skills/quiz-gate/SKILL.md](skills/quiz-gate/SKILL.md) です。

## 使い方

```text
/quiz-gate
```

または「この作業を理解できているか確認して」と依頼します。対象を省略した場合は、
その session で直前に完了した作業を対象にします。`/goal` の完了、plan phase の完了、
merge の直前にも、この skill の利用を提案する想定です。

briefing は `.scratch/ledger/<YYYY-MM-DD>-<slug>.html` に作成します。設問と正答は
conversation 内に保持し、回答前に提示しません。

## 構成

```text
quiz-gate/
├── .codex-plugin/plugin.json
├── README.md
├── CHANGELOG.md
└── skills/
    └── quiz-gate/
        └── SKILL.md
```

配布用の plugin package の正本はこの directory です。skill を standalone で利用する場合でも、
`skills/quiz-gate/` を唯一の source として扱い、別の `SKILL.md` を複製して二重管理しないでください。

## 開発時の確認

```bash
python -m json.tool plugins/quiz-gate/.codex-plugin/plugin.json >/dev/null
```

plugin の追加・配布・marketplace 登録については、リポジトリ全体の
[development guide](../../docs/development.md) を参照してください。
