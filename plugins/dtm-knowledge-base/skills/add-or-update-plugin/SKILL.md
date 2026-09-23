---
name: add-or-update-plugin
description: Add or update an executable DTM plugin, instrument, effect, host, or utility in the user's Notion Plugin Library when the user explicitly requests a KB change. Do not use for ordinary DTM advice or for sample packs, Kontakt libraries, and other content.
---

# Add or update a plugin (write)

Read [the shared Notion workflow](../../references/notion-workflow.md) and the current Hub. A user request to add or update this asset authorizes the corresponding KB write; advice alone does not.

1. Fetch the current Plugin Library data source schema. Verify current property names, types, options, and the Hub's Plugin page format.
2. Search Plugin Library for Name and Developer, including spelling/version variants. Fetch all plausible matches. Resolve the exact product/edition; if ambiguous, stop that write and report the candidates.
3. Update the existing record when identity matches. Create only if no match remains and duplicate checking was reliable. Record the minimum evidence-backed identity and any other fields the request and sources support. Do not infer ownership, license, authorization, installed state, DAW compatibility, CPU class, or zero latency from product marketing or one benchmark field.
4. For requested documentation, follow the Hub page format and prioritize decision-useful strengths, caveats, alternatives among registered assets, and starting points. Preserve unrelated page sections, benchmark fields, and Personal notes.
5. Re-fetch the record and verify identity plus changed fields. Return its Notion link, what changed, evidence, and unresolved verification items. If no change was needed, report the matched record instead of creating another.
