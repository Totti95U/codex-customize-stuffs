---
name: quiz-gate
description: Comprehension gate before accepting agent work. Builds an HTML briefing of what the agent did (architecture overview, per-subsystem prose tied to real code, decisions, assumptions, verification limits), quizzes the user on it, explains every answer afterwards, and blocks commit/merge/phase completion/goal completion until the user passes. Use when the user invokes /quiz-gate, or propose it before declaring a /goal complete, marking a plan phase done, or merging.
---

The user must understand what they accept well enough to defend it. You surface what was decided on their behalf, give them what they need to understand it without rereading raw source, then check that they own it. Speak in the user's language.

## 1. Scope

Take the target from the user's input; otherwise use the most recent finished unit of work in this session (a `/goal`, a plan phase, a branch diff, a set of result files). State the target in one line and continue unless it is ambiguous.

## 2. Briefing and questions

Delegate to one fresh-context `subagent` (default model). Give it only the artifact pointers — paths, diff base, result files, plan sections, the original request — not your own summary, so it cannot inherit your blind spots. It reads the artifacts and returns the questions (below) after writing the briefing.

### Briefing: `.scratch/ledger/<YYYY-MM-DD>-<slug>.html`

One self-contained HTML file the user reads before the quiz, so that answering needs understanding, not source archaeology. Size it to the work; skip nothing in the minimum, pad nothing beyond it.

Minimum:

- **Overview figure**: the system's architecture at a glance — components/stages, what flows between them (data, files, calls, certificates), and where the new work sits. For research or computation, show the pipeline from inputs to result files, and the structure of the mathematical claim (statements, which depend on which) beside it.
- **Per-subsystem sections**: for each subsystem, what it does and why, in prose, **paired with the real code**. Quote short verbatim excerpts with `path:line-range`; connect each sentence of the prose to the lines it describes (numbered markers or side-by-side). For math, pair each statement or formula with the function/file that implements or checks it, and say what the code does not cover. Fold long excerpts in `<details>`. Never paraphrase code as if it were quoted.
- **Decisions made for the user**: defaults chosen, scope cut, which requirement won when two clashed, reinterpretations.
- **Assumptions**: parameter ranges, genericity, tolerances, exact vs floating-point, input data provenance.
- **Verification**: each check that ran (command, observed output); for each, what it proves and what it does **not** prove (e.g. exact vs numerical PASS, a finite sample of a parameter range, a test sharing the implementation's mistake).
- **Not verified / open**.
- A status line at the end, initially "pending".

The briefing explains the work; it must not contain the quiz questions or keys. Questions test application — edge cases, "what breaks if this is reverted", what a PASS guarantees over which range — so reading the briefing is necessary and sufficient, but no answer appears verbatim.

Format: follow the AGENTS.md graphical design rules. Diagrams as Mermaid or inline SVG; formulas rendered with KaTeX. Verify the file visually per the AGENTS.md "HTML visual verification" rule before returning.

### Questions

3–6, each with its answer key, a 2–4 sentence explanation, and the briefing section / code location it targets. Mix:

- multiple choice with plausible distractors drawn from real alternatives (plus a one-line reason each distractor is wrong);
- free response in the user's own words.

Target decisions, assumptions, and verification limits, not trivia. Good shapes: "why is this line/step here?", "what breaks if this is reverted / this hypothesis is dropped?", "what exactly does this PASS guarantee, and over what range?", "which step is the crux?", "reconstruct the argument's skeleton without looking", "what happens on this edge case / at this parameter value?". Include at least one code line or proof step at random. Each question must be answerable from the briefing and the code it points to.

When the subagent returns, check cheaply yourself: open 2–3 quoted excerpts against the source, and confirm each key against the artifacts. Drop questions whose keys you cannot confirm.

## 3. Hand off, then wait

Present the briefing with `present`, tell the user it is ready, and **end the turn**. Do not ask the questions in the same turn. Start the quiz when the user replies (e.g. that they have read it). Keep the questions and keys in this conversation; never show them early.

## 4. Quiz

Ask all questions in one `ask_user_question` call: multiple-choice questions with shuffled options and no `(Recommended)` marker; free-response questions with no options. Never reveal or hint at keys before the user answers.

## 5. Grading and follow-up

Grade each answer. A free response passes when it captures the key's substance, whatever the wording.

Keep one even register for right and wrong answers alike, so a miss does not read as an event. For a miss:

- Start from what was right in the answer, concretely, when something was — the part of the reasoning that holds, not a compliment.
- Say what the answer missed in one or two sentences, pointing at the file, line, or step.
- When the miss traces to something the work or the briefing left implicit — an unrecorded decision, a misleading name, a check whose limits were not stated — say so plainly and fix it in the briefing. Only when it is true.
- When the user's answer exposes a real error in the work, say that directly: the gate found a defect. Fix it or record it before going on.
- Then go straight to a re-ask: a different question on the same point, no harder than the original.

Do not use praise words, exclamations, reassurance ("don't worry", "good try"), apologies, or scores like "2/5". Do not lecture beyond what the miss needs.

If the same point is missed twice, stop quizzing it and offer the user a choice: walk through that part together, or reread it themselves and come back. Retest it afterwards.

## 6. Gate and explanations

Pass means every point answered correctly, including re-asks. On pass, give a short explanation for **every** question, including those answered right: the key, why it holds in 2–4 sentences, and where it lives (briefing section, `path:line`). For multiple choice, add one line on why the notable distractor fails. Same even register: no congratulation, no score.

Then close with one line naming what the user now owns, and set the briefing's status line to "passed <date>".

Until pass, do not commit, merge, mark a plan phase done, or declare a goal complete for this target. If the user explicitly chooses to accept without passing, respect it and set the status to "accepted without passing" plus the open points.
