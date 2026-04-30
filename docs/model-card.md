# Model Card

## Intended Use

Generate SQL from plain-English analytics questions for portfolio demos and internal data exploration prototypes.

## Not Intended For

- Running write operations against production databases.
- Exposing unrestricted database access.
- Answering questions without schema validation and access control.

## Data

The repository includes synthetic sample data. The full project concept assumes 80K text-to-SQL pairs for QLoRA fine-tuning.

## Metrics

Primary metric:

- Execution accuracy

Secondary metrics:

- SQL validity rate
- Average response latency
- Unsafe query rejection rate

## Risks

Generated SQL can be wrong, inefficient, or overbroad. In production, natural language interfaces need permission checks, query cost limits, audit logging, and result redaction.

## Mitigations

- Allow only read-only SQL.
- Validate tables against schema metadata.
- Add row limits and timeouts.
- Log generated SQL for review.

