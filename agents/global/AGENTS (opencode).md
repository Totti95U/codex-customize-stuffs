# AGENTS.md

## チャット時の指示

- ページデザインは Minimalism。背景はライトモードで白系の無彩色（#ffffff）、ダークモードで黒系（#333333 / #1c1c1c）。装飾グラデーションは禁止。
- 文中の変数・関数・数式は KaTeX でレンダリングする。

## General instructions

- Before a completed task's final response, invoke `$maintain-agents-md`.
- Clarify uncertain task requirements with the user; do not assume.

## Agent workflow

- The primary agent owns implementation. Delegate only well-scoped work that materially benefits; use ordinary agents for routine work. Do not duplicate delegated work; do only meaningful, non-overlapping work alongside it.
- Use `senior-consult` only for material mathematical/specification ambiguity, conflicting evidence, hard-to-reverse architecture, hidden invariant/API/data risks, or two serious failures without a root cause—not difficulty alone.
- Provide the question, assumptions, relevant files/symbols, evidence, alternatives, and attempts. Request analysis, not implementation; consult once per decision unless substantial new evidence appears.
- If uncertainty remains, ask the user with stakes, evidence, alternatives, consultant conclusions, and references. Pause only dependent work; do not guess.
- Use `wait_agent` only when the next critical-path step depends on its result, never for status polling. Prefer one long, event-driven wait; rely on completion/messages to wake it.
- Set `timeout_ms` to at least twice the estimated remaining time and at least 300000 ms; omit it if the estimate is unreliable.
- A timeout means no event, not failure. If state is unchanged, re-estimate and wait substantially longer (preferably ≥2× the previous timeout); do not immediately poll or shorten waits for acknowledgements/status.
- Send messages to running subagents only when new information materially changes their task.

## Runtime policies

Follow runtime policies and gate state injected as developer context for the current turn; never carry prior activation or overrides forward. When Evening Exploration is active, do not weaken or bypass it except through its defined override mechanism.

## HTML visual verification

Before completing HTML creation/edits, visually verify with Browser Use over HTTP, never `file://`. Start a temporary server from the repository root, e.g. `python3 -m http.server 8000 --bind 127.0.0.1`, and open `http://127.0.0.1:8000/<path-to-html>`.

Check layout, clipping/overflow, missing assets, relative paths, desktop rendering, and mobile widths when relevant. Stop the server afterward.

## Ponytail: efficient, not careless

Before coding, read the task and affected code and trace the flow end to end. Then stop at the first viable option:

1. Skip unnecessary work (YAGNI).
2. Reuse existing code/patterns.
3. Use the standard library.
4. Use native platform features.
5. Use installed dependencies.
6. Use one line if sufficient.
7. Otherwise, write the minimum working code.

- Fix root causes: inspect every caller of the function you touch and fix shared logic once, not only the reported path.
- No unrequested abstractions/boilerplate or avoidable dependencies. Prefer deletion, boring code, fewer files, and the shortest correct diff.
- Question complex requests: does a simpler solution cover the need?
- For equally small stdlib options, choose the one correct on edge cases.
- Mark deliberate shortcuts with a `ponytail:` comment stating their known ceiling and upgrade path.
- Never sacrifice understanding, trust-boundary validation, data-loss prevention, security, accessibility, real-hardware calibration, or explicit requirements.
- Non-trivial logic must leave one minimal runnable regression check (assert-based demo/self-check or small test file; no frameworks/fixtures). Trivial one-liners need no test.

These rules also apply when working on the Ponytail repository itself.
