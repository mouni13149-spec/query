# Architecture

The project has four layers:

- Schema loader for table and column metadata.
- Text-to-SQL generator that maps natural language to schema-aware SQL.
- Validator that blocks unsafe SQL and unknown tables.
- Executor that runs read-only queries against SQLite.

```mermaid
flowchart LR
  A["User question"] --> B["SQL generator"]
  C["Database schema"] --> B
  B --> D["SQL validator"]
  D --> E["Read-only executor"]
  E --> F["Rows + SQL response"]
```

## Production Path

The local generator is deterministic for demos and tests. The QLoRA script provides a training path for CodeLlama-style text-to-SQL models using schema-question-SQL triples.

