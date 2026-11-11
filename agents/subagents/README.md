# Subagents (Agent Presets)

専用のサブエージェントの設定をまとめたものです。
現在は DeepSeek Harness (DSH) でのみ運用しています。
DSH に導入する場合は各 `.yml` ファイルの内容を `~/.dsh/profiles/<profile>/cordis.patch.yml` に適切な形で追記してください。プロバイダーやモデルはご自身の環境に合わせて変更してください。

現在、以下のサブエージェントが用意されています。

## review_code（preset `reviewer`）

モデル: `gpt-6.1-sol` (代替モデル: `gpt-6.1-terra`, `claude-opus-5.5` など)
Reasoning effort: `high`

エージェントが行った作業内容のレビューを行うサブエージェントです。コードの品質、スタイル、潜在的なバグ、セキュリティ上の懸念点などをチェックし、改善点を提案します。
「Reviewer を呼び出して作業内容のチェックを受けてください」と言った形で、親エージェントがレビューを依頼することができます。基本的には レビュワーからの指摘がなくなるまで自動的にコードの改善と再チェックを繰り返します。

## senior_consult（preset `senior-consult`）

モデル: `gpt-6-astra` (代替モデル: `claude-fable-5.2` など)
Reasoning effort: `high`

作業中のエージェントが高度な数学的・技術的問題に直面した際に呼び出すサブエージェントです。作業エージェントからの相談を受け、問題の分析、解決策の提案などを行います。
基本的には `AGENTS.md` の Agent workflow に従って呼び出されるため、人間側から直接呼び出すことはありません。

## inspect_image（preset `image-reader`）

モデル: `openai-codex/gpt-6.1-terra` (代替モデル: `claude-sonnet-5.5`, `gemini-3.8-flash-lite` など)
Reasoning effort: `low`

画像の読み取りが苦手なモデルからがスクリーンショットや UI 画像の確認を委譲するために呼び出されるサブエージェントです。

## 導入

各 harness により異なりますが、通常は `~/.[harness]/agents` 下に各 markdown ファイルを配置すれば導入できます。詳細は各 harness のドキュメントを参照してください。
