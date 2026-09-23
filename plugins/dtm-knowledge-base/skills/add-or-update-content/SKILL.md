---
name: add-or-update-content
description: Add or update a sample pack, Kontakt library, preset bank, expansion, IR library, or other separate DTM content collection in the user's Notion KB when explicitly requested. Do not use for executable plugins or ordinary DTM advice.
---

# Add or update content (write)

Read [the shared Notion workflow](../../references/notion-workflow.md) and the current Hub. Only an explicit add/update request authorizes a write. Never inspect local files unless the user explicitly permits that separate action.

1. Apply the Hub's current Plugin/Content boundary. Keep inseparable factory content on its Plugin page. For separate collections, fetch the current Content Library schema before writing.
2. Search Content Library for the same product, developer, edition/version, and host. Fetch plausible matches. Reuse an existing record when identity matches; unresolved collisions block creation.
3. For a new discovery, create a thin Content Library record with evidence-backed Name, Content Type, Host / Engine, Availability, and Access. Put source evidence on the page or in a suitable field that exists in the live schema. If no local files were inspected, state `local manifest not inspected`; do not claim installation or exact manifest from official product information.
4. Add detailed documentation to that same record only when the user requests detail or the collection has independent retrieval/comparison value. Use the Hub's Content page format. A thin record alone is not proof of sound, quality, or use case.
5. Re-fetch the changed record and verify identity, fields, and evidence. Return its link and any unknown edition, provenance, version, availability, access, or license.
