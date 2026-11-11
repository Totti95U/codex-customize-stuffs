# AGENTS.md

## General instructions

- グラフィカルデザインは minimalism を採用し、[デジタル庁デザインシステム（DADS）](https://design.digital.go.jp/dads/)に準拠する。
  - DADS を基にしたローカルデザインシステムとして扱う。色・タイポグラフィ・余白・角の形状・コンポーネントは DADS のデザイントークン（`@digital-go-jp/design-tokens`）と定義に従い、独自値は DADS に該当がない場合に限る。
  - 背景はライトモードで白系の無彩色（#fafafa）、ダークモードで黒系（#101010）に上書きする。DADS にはダークモードの定義がないため、ダークモードの色は下記のコントラスト比を満たすように独自に定める。
  - テキストは文字サイズにかかわらず背景とのコントラスト比 4.5:1 以上、アイコンや枠線などの非テキストは隣接色と 3:1 以上を確保する。
  - 装飾グラデーションは禁止。
- 文中の変数・関数・数式は KaTeX でレンダリングする。
- Before a completed task's final response, invoke `$maintain-agents-md`.
- ユーザーへの質問や最終応答によるユーザーへの報告などは日本語で行ってください。
- Clarify uncertain task requirements with the user; do not assume.
- ユーザーが提示した方法よりも効率的・効果的な方法がある場合は遠慮なくユーザーに提案してください。

## Developing instructions

- This is an internal services under development, do not provide backward compatibility or data migration.
- Follow KISS: update documentation first, write tests (TDD), then implement only the required functionality.
- Before finishing, remove unnecessary code and check documentation consistency.
- 基本方針は「コードには How、テストコードには What、コミットログには Why、コードコメントには Why not」。コードコメントは、別の方法を採用しなかった理由や制約に限定し、コードの動作説明など、それ以外は書かない。
- When a repository's documentation and its existing code disagree, follow the conventions used in the existing code, and in your final reply point out each inconsistency you found between the documentation and the code.
- Avoid unnecessary secondary labels and descriptions. Let the layout do the explaining.

## Agent workflow

- The primary agent owns implementation. Delegate only well-scoped work that materially benefits; use ordinary agents for routine work. Do not duplicate delegated work; do only meaningful, non-overlapping work alongside it.
- Use `senior-consult` only for material mathematical/specification ambiguity, conflicting evidence, hard-to-reverse architecture, hidden invariant/API/data risks, or two serious failures without a root cause—not difficulty alone.
- Provide the question, assumptions, relevant files/symbols, evidence, alternatives, and attempts. Request analysis, not implementation; consult once per decision unless substantial new evidence appears.
- If uncertainty remains, ask the user with stakes, evidence, alternatives, consultant conclusions, and references. Pause only dependent work.
- Use `wait_agent` only when the next critical-path step depends on its result, never for status polling. Prefer one long, event-driven wait; rely on completion/messages to wake it.
- Set `timeout_ms` to at least twice the estimated remaining time and at least 300000 ms; omit it if the estimate is unreliable.
- A timeout means no event, not failure. If state is unchanged, re-estimate and wait substantially longer (preferably ≥2× the previous timeout); do not immediately poll or shorten waits for acknowledgements/status.
- Send messages to running subagents only when new information materially changes their task.

## 既知の環境問題

- `agentsview sync` が `unsupported required event type "job/registered"` で終了コード 1 になるのは既知のバージョン不整合（agentsview v0.46.1 が DSH の `job/registered` / `job/settled` を未対応）。環境破損ではないので原因調査をやり直さないこと。他ソースと該当イベントを含まない DSH セッションは正常に同期されるため、`agentsview update --check --force` で更新が出るまで放置し、`disabled_agents` の変更や `~/.dsh/sessions` のログ改変で回避しない。

## HTML visual verification

Before completing HTML creation/edits, visually verify with Browser Use over HTTP, never `file://`. Start a temporary server from the repository root, e.g. `python3 -m http.server 8000 --bind 127.0.0.1`, and open `http://127.0.0.1:8000/<path-to-html>`.

Check layout, clipping/overflow, missing assets, relative paths, desktop rendering, and mobile widths when relevant. Stop the server afterward.
