# Maintain AGENTS.md

完了した repository task を振り返り、将来も有効な repository 固有の知見だけを
適切な `AGENTS.md` に反映する skills-only plugin です。作業ログを残したり、
今回だけの判断をルール化したりするための plugin ではありません。

外部 service、MCP server、認証、独自 UI は使用しません。実際の workflow の
正本は [skills/maintain-agents-md/SKILL.md](skills/maintain-agents-md/SKILL.md) です。

## すること・しないこと

この skill は、依頼内容、最終 diff、実行した検証、失敗から得られた制約、対象
path に適用される既存の `AGENTS.md` を確認します。そのうえで、次の条件をすべて
満たすルールだけを追加または更新します。

- repository 固有である
- 将来の task にも有効である
- code や標準 tool からは自明でない
- 次の agent が実行に移せる

恒久的なルールがなければ `AGENTS.md` は変更しません。進捗、日時、branch 名、
一回限りの失敗、一般的な開発助言、secret や machine 固有の path は記録対象外です。
更新が必要な場合も、repository 全体には root の `AGENTS.md`、局所的な規約には
最も近い nested `AGENTS.md` を選び、最小限の差分に留めます。

## 使い方

repository task の実装と検証が終わった後に、次のように明示して使います。

```text
$maintain-agents-md
```

または「この完了済み task から、永続的な `AGENTS.md` の更新が必要か確認して」
と依頼します。skill は最終回答の前に実行する想定です。更新しない結論も正常な
結果であり、既存の指示を無理に増やしません。

## 構成

```text
maintain-agents-md/
├── .codex-plugin/plugin.json
├── README.md
├── CHANGELOG.md
└── skills/
    └── maintain-agents-md/
        └── SKILL.md
```

配布用の plugin package の正本はこの directory です。skill を standalone で
利用する場合でも、`skills/maintain-agents-md/` を唯一の source として扱い、別の
`SKILL.md` を複製して二重管理しないでください。

## 開発時の確認

manifest と skill の変更後は、少なくとも次を確認します。

```bash
python -m json.tool plugins/maintain-agents-md/.codex-plugin/plugin.json >/dev/null
```

plugin の追加・配布・marketplace 登録については、リポジトリ全体の
[development guide](../../docs/development.md) を参照してください。

## 関連資料

- [AGENTS.md によるカスタム指示](https://learn.chatgpt.com/ja-JP/docs/agent-configuration/agents-md)
- [OpenAI Docs: カスタマイズ](https://learn.chatgpt.com/ja-JP/docs/customization/overview)
