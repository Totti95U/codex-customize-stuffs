# Runtime hooks

`hooks.json` は global hook 設定、`scripts/` はその runtime の正本です。
夜間探索 hook は JST の時刻を判定し、[policy](../policies/evening-exploration.md) を読み込みます。
探索の意味判定と Notion 操作は Codex が担当します。

導入・検証方法と制約は [Development Guide](../docs/development.md#runtime-hooks-and-policies) を参照してください。
