# AGENTS.md

## チャット時の指示

- 一人称は "私" を使ってください
- 英語に抵抗感はないので、固有名詞や専門用語など日本語に自然に訳せないものは英語のままにしてください
- HTML などのページデザインは Minimalism, Constructivism, Flat, Bento を採用してください。ライトモードでは背景を白 (#ffffff に近い無彩色)、ダークモードでは背景を黒 (#333333 や #1c1c1c に近い色) を使ってください
- 装飾としてのグラデーションは使わないでください
- 文中に変数や関数、数式が登場する場合は KaTeX を使用して変数、関数、数式のレンダリングを行ってください。

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
