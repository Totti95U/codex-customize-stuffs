# Notion KB workflow shared by all five skills

The connected Notion workspace owns the data. This plugin stores entry points and procedures, not a copy of the schema, records, or page templates.

## Entry points and connection

- Hub page: `3df8983d-2e73-8153-afc9-fd32cc7b3b66` (`DTM Plugin Knowledge Base`).
- Initial discovery hints only: Plugin Library `collection://19f783a6-99d1-49cc-93cd-fbee033989c5`; Content Library `collection://3cfadbf3-e717-45a0-8be5-d88a95378b84`; Use Cases `collection://8abdd6c4-04b5-41d1-9cb4-b2d53360898d`; Asset × Use Case `collection://35686644-cbda-4c77-8e0f-b4cbce85df37`.
- Use a connected Notion app/MCP. Fetch `self` to identify the connected workspace and current tool access. Fetch the Hub at the start of each independent task and inspect its current Retrieval principle, library boundary, availability/verification semantics, response provenance, Asset × Use Case rules, and maintenance workflow. Follow the Hub if this file differs. Check `truncated` or unknown blocks before relying on the page.
- Discover current data sources from the Hub and fetch each relevant data source before a write. The IDs above are fallbacks for locating a source, never proof of its current schema. Content Library holds both thin discovery records and detailed documentation.
- Prefer the connected Notion content-search tool allowed by `self` (`ai_search` if available; otherwise `search`). Query one data source at a time if cross-source query is unavailable. Fetch candidate pages for rich text and evidence. If query limits or search coverage prevent a reliable duplicate check, do not create a record.

## Safety and provenance

- Reading and comparing records needs no additional confirmation. Create or update Notion data only when the user's current request explicitly asks for that operation. DTM advice alone grants no write authority.
- Before each create, search for an existing identity or asset/use-case pair and update it if appropriate. Ambiguous product identity, developer, edition, license, provenance, or duplicate matches must remain unresolved; use current schema's `Unknown` / `Needs verification` values when available and supported by evidence. Do not invent a record or a property value to make the workflow complete.
- Preserve unrelated fields, benchmark data, and Personal notes. Only change Personal notes when the user supplies their experience and asks to record it. Re-fetch changed pages and verify their identity, target fields, and relations.
- Label material as record-backed fact, suggested starting point, personal note, or inference. Carry confidence and verification caveats into the answer. Suggested numeric settings absent from the record are suggestions, not database facts.
- `Installed`, binary presence, and load success do not establish license, DAW operation, or full functionality. Content `Availability` and `Access` answer different questions. `Offline DSP ratio` is offline benchmark cost, not DAW realtime CPU; reported latency 0 does not prove zero-latency operation.
- Cite the relevant Notion page and, when used, official documentation. If a source cannot be reached or content is incomplete, say what was verified and what remains unknown.
