# AGENTS.md

## General instructions

- ページデザインは Minimalism。背景はライトモードで白系の無彩色（#fafafa）、ダークモードで黒系（#101010）。装飾グラデーションは禁止。
- 文中の変数・関数・数式は KaTeX でレンダリングする。
- Before a completed task's final response, invoke `$maintain-agents-md`.
- ユーザーへの質問や最終応答によるユーザーへの報告などは日本語で行ってください。
- Clarify uncertain task requirements with the user; do not assume.

## Developing instructions

- This is an internal services under development, do not provide backward compatibility or data migration.
- Follow KISS: update documentation first, write tests (TDD), then implement only the required functionality.
- Before finishing, remove unnecessary code and check documentation consistency.
- 基本方針は「コードには How、テストコードには What、コミットログには Why、コードコメントには Why not」。コードコメントは、別の方法を採用しなかった理由や制約に限定し、コードの動作説明など、それ以外は書かない。
- When a repository's documentation and its existing code disagree, follow the conventions used in the existing code, and in your final reply point out each inconsistency you found between the documentation and the code.

## Agent workflow

- The primary agent owns implementation. Delegate only well-scoped work that materially benefits; use ordinary agents for routine work. Do not duplicate delegated work; do only meaningful, non-overlapping work alongside it.
- Use `senior-consult` only for material mathematical/specification ambiguity, conflicting evidence, hard-to-reverse architecture, hidden invariant/API/data risks, or two serious failures without a root cause—not difficulty alone.
- Provide the question, assumptions, relevant files/symbols, evidence, alternatives, and attempts. Request analysis, not implementation; consult once per decision unless substantial new evidence appears.
- If uncertainty remains, ask the user with stakes, evidence, alternatives, consultant conclusions, and references. Pause only dependent work.
- Use `wait_agent` only when the next critical-path step depends on its result, never for status polling. Prefer one long, event-driven wait; rely on completion/messages to wake it.
- Set `timeout_ms` to at least twice the estimated remaining time and at least 300000 ms; omit it if the estimate is unreliable.
- A timeout means no event, not failure. If state is unchanged, re-estimate and wait substantially longer (preferably ≥2× the previous timeout); do not immediately poll or shorten waits for acknowledgements/status.
- Send messages to running subagents only when new information materially changes their task.

## HTML visual verification

Before completing HTML creation/edits, visually verify with Browser Use over HTTP, never `file://`. Start a temporary server from the repository root, e.g. `python3 -m http.server 8000 --bind 127.0.0.1`, and open `http://127.0.0.1:8000/<path-to-html>`.

Check layout, clipping/overflow, missing assets, relative paths, desktop rendering, and mobile widths when relevant. Stop the server afterward.
