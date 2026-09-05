---
name: retitle
description: >
  Suggest or revise a title for the current ChatGPT or Codex conversation using
  the user's personal naming rules. Use only when the user explicitly asks for
  a chat title, asks to rename the current conversation, invokes this skill, or
  asks what this conversation should be called.
---

# Chat Title Naming

Generate a short title that helps the user recognize and recall this
conversation when viewing it months later in a long chat history.

This is a metadata task. It must not interfere with the main coding, research,
writing, or implementation task.

## Priority

The user's explicit request always takes precedence over this skill.

If the user specifies a title format, language, length, naming convention, or
other constraint, follow that instruction instead of the defaults below.

## Execution strategy

### Prefer isolated execution when available

When the host provides a collaboration or subagent mechanism, perform title
generation in a separate, bounded task rather than reasoning about naming
extensively in the main task.

Delegate only the information needed to choose a title:

- the current title, if known;
- the user's original goal;
- a compact description of the conversation's main development;
- distinctive user-created names, project names, technical terms, or
  conclusions; and
- these naming rules.

Do not delegate large raw command outputs, source files, unrelated repository
internals, detailed implementation history, secrets, credentials, or the full
parent context when a concise task brief is enough.

The delegated task should return only the recommended title and, only when
genuinely necessary, at most two alternatives. Do not expose its internal
analysis in the main conversation.

If isolated execution is unavailable, perform the naming task directly and
keep the reasoning minimal.

### Keep the task small

Use information already available from the conversation. Do not inspect
additional files, run commands, browse the web, change source files, or modify
project instructions solely to create a title.

If the available context is insufficient for a perfect title, make the best
reasonable choice instead of expanding the task.

This skills-only plugin proposes titles. It does not rename a ChatGPT or Codex
conversation automatically and does not open a Side Chat or other UI surface.

## Naming objective

The title is primarily for the person who participated in the conversation.

Optimize for:

\[
\text{Title quality}
\approx
\text{memory recall}

+

\text{topic distinctiveness}

+

\text{activity clarity}.
\]

Do not optimize primarily for:

\[
\text{coverage of all conversation content}.
\]

The title does not need to explain the conversation to an unfamiliar reader.
Ask: if the user saw this title among many chats several months from now, would
it quickly bring this conversation back to mind?

## Naming rules

### 1. Optimize for recall, not summarization

Identify the conversation's strongest memory anchor. Do not attempt to
summarize every substantial topic discussed. A later tangent does not need to
appear merely because it is technically important.

For example, "Eagle の AI description のモデル比較、blind test、HTML
評価アプリ、参考資料整理" is usually worse than "Eagle の AI 機能を使った
参考資料整理法" when the latter is the concept that best identifies the
conversation.

### 2. Preserve user-created names

Prefer names and terminology already used by the user. Examples include:

- これキミ
- ぼかしディザ
- テクスチャディザ
- BMH
- BMF
- RoD bridge
- Pacific Blues

Do not replace a memorable user-created name with a generic formal description
merely for self-contained readability.

Prefer "これキミの仕様設計" over "電子署名を用いたオンライン同一性証明サービスの
仕様設計" when これキミ is already the project's established name.

### 3. Include the activity when it improves recognition

A topic alone may be insufficient. Useful activity labels include:

- 解説
- 仕様設計
- 実装方法
- 撮影のコツ
- RAW 現像
- 再現法
- 選び方
- 比較
- 原因
- 提案

For example:

- CZ-210M について becomes CZ-210M を使った撮影のコツ.
- テクスチャディザ becomes テクスチャディザの仕様設計.

### 4. Do not improve a title that is already good enough

More specific does not necessarily mean better. If the existing title already
uniquely and naturally identifies the conversation, preserve it.

For example, 生活リズムを直したい may be better than
正午起床ループから抜けて生活リズムを前倒しする方法. Likewise,
減色アルゴリズムの提案 may already be sufficient.

Avoid title inflation.

### 5. Two major subjects may use /

If the conversation contains exactly two independent themes that are both
important memory anchors, preserve both.

Examples:

- Bridgeの実装方法 / partitioning をトーラス上の写像へ拡張する方法
- 料理向きのフィルムシミュレーション / Easy Reala Ace の RAW 現像再現法

Do not use / for a list of secondary details. Prefer one topic whenever
possible.

### 6. Conclusions can be titles

The most memorable part of a conversation may be its conclusion rather than
its question.

For example, レンズ補正の判断 can become 撮って出しにレンズ補正は要らない.

Do not force all titles into noun phrases. A question-style title is also
acceptable when it captures the memorable question naturally, such as
三色グラデーションは自動化できる?.

### 7. Prefer specific concepts over broad categories

Avoid generic titles such as:

- Julia の相談
- 写真について
- 研究の話
- AI 活用法
- デザインについて

when a distinctive concept is available. Use the concept that actually anchors
the user's memory.

## Conversation evolution

Do not assume that the initial user message permanently defines the title. A
conversation may evolve.

However, do not automatically rename based on the latest tangent. Choose the
title according to the conversation's conceptual identity. Consider a later
topic title-worthy only if it became one of the main reasons the user would
want to find this conversation again.

## Decision procedure

1. Read the current title if available.
2. Identify the conversation's strongest memory anchor.
3. Extract user-created names and distinctive technical terms.
4. Determine what the conversation actually did: explanation, design,
   implementation, comparison, debugging, advice, reproduction, conclusion,
   or another activity.
5. Ignore minor tangents.
6. Ask whether the current title is already sufficient.
7. If it is, keep it.
8. If there are two equally important independent anchors, consider /.
9. Produce the shortest natural title that reliably recalls the conversation.
10. Return only the title unless alternatives or reasoning were requested.

## Calibration examples

### Example A

Current title: HTML記事作成

Conversation: Creation of an explanatory article about Baby Mandelbrot Hydra
and BMF.

Preferred: BMH, BMF の解説書作成

### Example B

Current title: 描画切替方法比較

Conversation: The discussion evolved toward Julia macros including @kwdef and
@enum.

Preferred: Julia のマクロ、特に @kwdef と @enum について

### Example C

Current title: RAW現像方針を提案

Preferred: 暗い店内の写真を RAW 現像するときのコツ

### Example D

Current title: グラデーションと色空間

Preferred: 三色グラデーションは自動化できる?

### Example E

Current title: テクスチャディザ

Preferred: テクスチャディザの仕様設計

### Example F

Current title: 電子署名を使った同一性証明サービス

Preferred: これキミの仕様設計

### Example G

Current title: 生活リズムを直したい

Preferred: 生活リズムを直したい

A rename is unnecessary.

## Anti-patterns

Avoid:

- summarizing the whole thread;
- treating the last message as automatically the main topic;
- replacing memorable terminology with formal generic terminology;
- adding details merely because they are available;
- making every title maximally specific;
- generic formulations such as ○○についての相談;
- producing a long hierarchical title;
- exposing delegated-task reasoning in the main thread; and
- doing repository work solely to obtain a title.

## Output contract

When the user asks only for a title, return exactly one line containing the
recommended title.

Do not add an explanation, a Markdown heading, quotation marks, a label such
as Title, or alternatives.

If the user explicitly asks for alternatives, return at most three candidates,
with the best first.

If the existing title should remain unchanged, return that existing title
verbatim.
