---
name: retrieve-assets
description: Find and compare the user's owned DTM plugins and content in the Notion Knowledge Base for a production problem or asset-choice question. Use for signal, sound, mix, workflow, or tool-selection requests; skip music theory, chord writing, and general composition questions with no asset choice.
---

# Retrieve assets (read only)

Read [the shared Notion workflow](../../references/notion-workflow.md), then fetch the current Hub. This skill never changes the KB. The Custom Instruction decides when KB consultation is useful; this skill defines how to retrieve once selected.

1. Identify signal/source, problem, goal, production stage, and constraints. If none calls for choosing an asset, answer without forcing a KB lookup.
2. Search Use Cases by Name, Query aliases, and nearby meaning. Read the best matching Use Case pages. Search more broadly if aliases or a vague question could hide a relevant case.
3. Follow their Asset Links into Asset × Use Case. Read Fit, Why, Starting point, Notes, and which of Plugin or Content is populated. Treat a malformed link as a data-quality issue, not a recommendation.
4. Fetch candidate Plugin/Content records and page bodies. For Content, check Host / Engine, Compatible Plugins, Requires, Availability, Access, Confidence, and the host Plugin when required. For Plugin, check Installed, Availability, benchmark evidence, Confidence, Status, and alternatives. Give priority to Summary, Strengths, Weaknesses / Caveats, Recommended uses, When I would choose this, Alternatives, Starting points, Personal notes, and AI Quick Reference.
5. Compare Primary first, then Specialist and Alternative by the user's constraints; include Experimental only with its caveat. Fetch the closest owned alternatives when the distinction matters. For a named asset, still inspect its relevant Use Cases and alternatives.

Return a concise choice rule: when to use A, when B is better, and what C is for. Separate record-backed facts, personal notes, inference, and any suggested starting point. Link the records used. If links or records are missing, say what could be confirmed; do not invent owned assets or availability.
