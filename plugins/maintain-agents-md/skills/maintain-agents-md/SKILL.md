---
name: maintain-agents-md
description: >
  Review a completed repository task to decide whether AGENTS.md needs
  a durable repository-specific instruction update. Do not use this
  skill for task logs, temporary state, or generic development advice.
---

Review the completed task before the final response.
Default to `NO_UPDATE`. A required review is not a required edit.

1. Inspect:
  - the user request and decisions made during the task;
  - the final diff;
  - commands that were actually verified;
  - non-obvious failures, constraints, and repository conventions;
  - the AGENTS.md files applicable to the affected paths.

2. Consider only knowledge that meets all of these conditions:
  - repository-specific;
  - likely to remain valid across future tasks;
  - non-obvious from the code or standard tooling;
  - actionable for a future coding agent.

  Before accepting a candidate, identify:
  - the concrete mistake or incorrect decision this instruction prevents;
  - the behavior or constraint verified in this task, or the user's explicit
    lasting policy, that supports it;
  - why ordinary reading of the code or existing documentation would not
    already provide the guidance when needed;
  - why it applies beyond this task without turning a local implementation
    choice into a permanent requirement.

  Reject the candidate if any condition is unmet or uncertain. If none
  qualify, return `NO_UPDATE` without editing. Do not write these acceptance
  justifications into AGENTS.md.

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
  - do not copy implementation descriptions or procedures from other docs;
    if their guidance must be seen before an action to prevent the identified
    mistake, add only a short instruction pointing to the existing source.

6. Re-read the resulting instruction chain and check for contradictions.

Boundary examples:
- A new function's purpose and arguments: no update; this belongs in code
  or API documentation.
- A test command passed in this task: no update on that fact alone.
- A command assumed to be a local check was verified to publish externally:
  a brief warning and verified local-only alternative may qualify if this
  is a lasting behavior and existing instructions do not already cover it.

Return one of:
- `NO_UPDATE` when no durable knowledge qualifies.
- `UPDATED <path>` followed by a one-sentence description of the rule.
