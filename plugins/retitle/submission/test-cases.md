# Chat Title Naming — Submission Test Cases

These cases are written for the Plugin submission portal. They test a
skills-only workflow, so no tool call, authentication, fixture account, or
external data is required.

## Positive cases

### 1. Direct title request

User prompt:

> この会話に合うタイトルを付けて。

Expected behavior:

- Activate Chat Title Naming.
- Identify the strongest memory anchor from the available conversation.
- Return exactly one title line with no heading, explanation, or quotation
  marks.

Expected result shape:

> <recommended title>

### 2. Good existing title stays unchanged

Conversation context:

> 現在のタイトルは「生活リズムを直したい」。会話全体も生活リズムを直す
> ことが主題で、より具体的な説明は記憶の助けにならない。

User prompt:

> 今のタイトルを見直して。

Expected behavior:

- Activate Chat Title Naming.
- Preserve the existing title because it is already concise and sufficiently
  distinctive.

Expected result shape:

> 生活リズムを直したい

### 3. User-created project name wins over a generic description

Conversation context:

> 「これキミ」という既存プロジェクトの identity proof UX と仕様を設計した。

User prompt:

> この会話のタイトルを提案して。

Expected behavior:

- Activate Chat Title Naming.
- Preserve the memorable project name instead of replacing it with a broad
  formal description.

Expected result shape:

> これキミの仕様設計

### 4. Two equally important independent subjects

Conversation context:

> 料理写真向きのフィルムシミュレーションと、Easy Reala Ace の RAW 現像再現法を
> 同じ深さで扱った。

User prompt:

> 後で探しやすいタイトルにして。

Expected behavior:

- Activate Chat Title Naming.
- Keep the two independent memory anchors.
- Use one slash only; do not append secondary details.

Expected result shape:

> 料理向きのフィルムシミュレーション / Easy Reala Ace の RAW 現像再現法

### 5. Explicit alternatives

Conversation context:

> BMH と BMF の説明記事を作成した。

User prompt:

> タイトル候補を3つ出して。

Expected behavior:

- Activate Chat Title Naming.
- Return no more than three candidates, best first.
- Include the specific terms BMH and BMF in the best candidate.

Expected result shape:

> BMH, BMF の解説書作成
>
> <optional alternative>
>
> <optional alternative>

## Negative cases

### 1. Ordinary writing request

User prompt:

> このメールを丁寧な日本語に直して。

Expected behavior:

- Do not activate Chat Title Naming.
- Perform only the ordinary writing task.

Reason:

The user did not ask for a conversation title or a title revision.

### 2. Conversation summary request

User prompt:

> この会話を1000字で要約して。

Expected behavior:

- Do not activate Chat Title Naming unless the user separately asks for a
  title.
- Produce a summary, not a title.

Reason:

Summarization and title generation are different workflows.

### 3. General research request

User prompt:

> ChatGPT のタイトル生成が下手な原因を調べて。

Expected behavior:

- Do not activate Chat Title Naming.
- Follow the applicable research workflow instead.

Reason:

The user is asking about title generation, not asking to name the current
conversation.
