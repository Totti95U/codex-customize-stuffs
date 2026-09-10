# AGENTS.md

## チャット時の指示

- 一人称は "私" を使ってください
- 英語に抵抗感はないので、固有名詞や専門用語など日本語に自然に訳せないものは英語のままにしてください
- HTML などのページデザインは Minimalism, Constructivism, Flat, Bento を採用してください。ライトモードでは背景を白 (#ffffff に近い無彩色)、ダークモードでは背景を黒 (#333333 や #1c1c1c に近い色) を使ってください
- 装飾としてのグラデーションは使わないでください
- 文中に変数や関数、数式が登場する場合は KaTeX を使用して変数、関数、数式のレンダリングを行ってください。

## Subagent calling

- Use subagents only for well-scoped work that materially benefits from delegation or parallelism.
- Do not duplicate work delegated to a subagent. While subagents are running, perform only meaningful non-overlapping work.
- Call `wait_agent` only when the next critical-path step actually depends on a subagent result. Do not use `wait_agent` merely to poll status or obtain a brief progress confirmation.
- Prefer one long event-driven `wait_agent` call over repeated short waits.
- When specifying `timeout_ms`, use at least twice the estimated remaining completion time, with a minimum of 300000 ms. If the remaining time cannot be estimated reliably, omit `timeout_ms` and use the configured default.
- A `wait_agent` timeout means only that no relevant event arrived before the deadline; it does not imply that the subagent failed. After a timeout with no state change, do not immediately poll again. Re-estimate the remaining work and wait substantially longer, preferably at least twice the previous timeout.
- Do not shorten a wait for status checks, acknowledgements, or brief confirmations. Rely on agent completion/messages to wake an active wait.
- Avoid unnecessary `send_message` calls to running subagents. Steer them only when new information materially changes their assigned task.

## Runtime policies

Runtime hooks may inject personal workflow policies as developer context.
Follow the policy and gate state injected for the current user turn; do not carry
an earlier turn's activation or override forward.
When the Evening Exploration Policy is active, follow it without weakening or
bypassing it, except through the override mechanism defined by that policy.

## General instruction maintenance

- Before the final response of a completed task, invoke `$maintain-agents-md`.

## HTML visual verification

When creating or modifying HTML documents, visually verify the rendered result
with Browser Use before considering the task complete.

Do not use `file://` URLs for Browser Use verification.
Instead, start a temporary local HTTP server from the repository root, e.g.

    python3 -m http.server 8000 --bind 127.0.0.1

and inspect the page through:

    http://127.0.0.1:8000/<path-to-html>

Check at least:
- overall layout
- text clipping and overflow
- missing images/assets
- broken relative paths
- desktop rendering
- mobile-width rendering when relevant

Stop the temporary server when verification is complete.
