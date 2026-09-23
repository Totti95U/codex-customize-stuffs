# DTM Knowledge Base

Five skills use a connected Notion app to search and maintain the user's `DTM Plugin Knowledge Base`. The live [Hub](https://app.notion.com/p/3df8983d2e738153afc9fd32cc7b3b66) supplies recording rules and page formats. The plugin stores no copied schema and makes no automatic changes during ordinary DTM advice.

| Skill | Use when | Access |
| --- | --- | --- |
| `retrieve-assets` | Compare owned tools/content for a production problem | Read only |
| `add-or-update-plugin` | Explicitly add or update executable software | Write |
| `add-or-update-content` | Explicitly add or update a separate content collection | Write |
| `document-asset` | Explicitly document an existing asset | Write |
| `link-use-cases` | Explicitly maintain asset/use-case relations | Write |

## Enable

Connect the Notion app to the workspace containing the Hub and grant it access to the Hub and its databases. From the repository root in a compatible Codex CLI, install the local marketplace and plugin:

```text
codex plugin marketplace add .
codex plugin add dtm-knowledge-base@totti95u-customizations
```

If this marketplace name is already registered from a remote snapshot, update that marketplace after the repository change is available there, then install the plugin. Start a new conversation so the skills are loaded. The Notion connection is separate from the plugin package; no token is stored here.

For ChatGPT, use a client that supports this local plugin and the connected Notion app. If either capability is absent, use the same skill instructions in a supported Codex environment. The exact install UI may differ by client.

## Small Custom Instruction routing rule

> When a DTM question would benefit from choosing among my owned plugins or content, consult the DTM Knowledge Base plugin. For music theory or composition questions without asset choice, answer directly. Only change the Notion KB when I explicitly ask to add, update, document, or link records.

New content starts as a thin Content Library record; detailed documentation is added to that same record when useful.
