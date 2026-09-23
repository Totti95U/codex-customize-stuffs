---
name: link-use-cases
description: Create or update Notion Asset × Use Case relations for an existing DTM plugin or content record when the user explicitly asks to organize its use cases. Do not use for read-only recommendations or to invent an asset record.
---

# Link use cases (write)

Read [the shared Notion workflow](../../references/notion-workflow.md) and the current Hub. Relation writes require an explicit user request.

1. Fetch current Use Cases and Asset × Use Case schemas and the exact asset record. Search Use Cases by Name, Query aliases, Goal, Source, Stage, and Problem type. Reuse a semantic match; create a product-independent Use Case only if none exists and the request authorizes linking/new Use Case work.
2. For each desired asset/use-case pair, search the Asset × Use Case data source by Name and relation, then fetch plausible matches. Update an existing pair; create only when uniqueness is reliable. Follow the Hub's current naming rule.
3. Set exactly one of Plugin or Content, exactly one Use Case, and a supported Fit. Write Why as the concrete reason the asset suits the goal, Starting point as the first practical action, and Notes for constraints or uncertainty. Do not turn a suggestion into a verified product fact or prescribe one fixed recipe for every situation.
4. Re-fetch each relation. Verify the asset/use-case pair, Plugin XOR Content, Fit, Why, and Starting point; then report created/updated/reused links and any unresolved duplicates or evidence gaps.
