---
name: maintain-agents-md
description: >
  Review a completed repository task and update the most appropriate
  AGENTS.md with durable repository-specific knowledge. Do not use this
  skill for task logs, temporary state, or generic development advice.
---

Review the completed task before the final response.

1. Inspect:
  - the user request and decisions made during the task;
  - the final diff;
  - commands that were actually verified;
  - non-obvious failures, constraints, and repository conventions;
  - the AGENTS.md files applicable to the affected paths.

2. Extract only knowledge that is:
  - repository-specific;
  - likely to remain valid across future tasks;
  - non-obvious from the code or standard tooling;
  - actionable for a future coding agent.

3. Never record:
  - completion status or a summary of the current task;
  - dates, issue numbers, branch names, or temporary file names;
  - speculative conclusions;
  - one-off failures that do not imply a stable constraint;
  - generic programming advice;
  - secrets, credentials, or machine-specific absolute paths;
  - rules already stated elsewhere.

4. Choose the narrowest appropriate scope:
  - repository-wide guidance goes in the root AGENTS.md;
  - subsystem-specific guidance goes in the nearest applicable
    nested AGENTS.md;
  - create a nested AGENTS.md only when placing the rule at the root
    would incorrectly affect unrelated code.

5. Edit minimally:
  - preserve existing wording and user changes;
  - add or revise the smallest possible number of bullets;
  - remove an obsolete instruction only when the task supplied
    direct evidence that it is no longer correct;
  - avoid duplicating information available in README or generated docs
    unless an agent must know it before working.

  6. Re-read the resulting instruction chain and check for contradictions.

Return one of:
- `NO_UPDATE` when no durable knowledge qualifies.
- `UPDATED <path>` followed by a one-sentence description of the rule.