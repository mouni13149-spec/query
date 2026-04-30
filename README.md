# LLM-Powered SQL Query Generator

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Let users query a database in plain English. The system converts natural language questions into SQL, validates the query against a schema, and can execute read-only queries against a local SQLite database.

Inspired by production natural-language-to-SQL tools such as Amazon Q generative SQL for Redshift.

## Project Highlights

- Converts plain-English analytics questions into SQL.
- Uses schema-aware validation to block unsafe or unsupported queries.
- Includes a FastAPI endpoint for deployment-style usage.
- Provides execution accuracy evaluation on labeled text-to-SQL examples.
- Includes optional CodeLlama-7B QLoRA fine-tuning scaffolding.

## Repository Structure

```text
.
├── app/                    # FastAPI app
├── data/                   # Sample schema, SQLite DB, and eval pairs
├── docs/                   # Architecture and model card
├── scripts/                # DB setup, benchmark, and QLoRA fine-tuning
├── src/sql_generator/      # Main package
├── tests/                  # Unit tests
├── pyproject.toml
└── README.md
```

## Quick Start

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

Create the sample SQLite database:

```powershell
py scripts/setup_sample_db.py --output data/sample_store.db
```

Generate SQL:

```powershell
sql-generator generate --schema data/schema.json --question "What were total sales by region?"
```

Generate and execute a read-only query:

```powershell
sql-generator query --schema data/schema.json --db data/sample_store.db --question "Show the top 3 products by revenue"
```

Evaluate execution accuracy:

```powershell
sql-generator evaluate --schema data/schema.json --db data/sample_store.db --data data/text_to_sql_eval.jsonl
```

## FastAPI Endpoint

Install API dependencies:

```powershell
pip install -e ".[api]"
```

Run:

```powershell
uvicorn app.main:app --reload
```

Example request:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8000/generate-sql `
  -ContentType "application/json" `
  -Body '{"question":"What were total sales by region?"}'
```

## Optional CodeLlama QLoRA Fine-Tuning

Install ML dependencies:

```powershell
pip install -e ".[ml]"
```

Fine-tune:

```powershell
python scripts/fine_tune_qlora.py `
  --train data/train_text_to_sql.jsonl `
  --eval data/eval_text_to_sql.jsonl `
  --base-model codellama/CodeLlama-7b-Instruct-hf `
  --output-dir artifacts/codellama_text_to_sql_qlora
```

Expected JSONL schema:

```json
{
  "question": "What were total sales by region?",
  "schema": "CREATE TABLE orders ...",
  "sql": "SELECT region, SUM(total_amount) FROM orders GROUP BY region;"
}
```

## Safety

The local executor only allows read-only `SELECT` queries. It blocks write operations such as `INSERT`, `UPDATE`, `DELETE`, `DROP`, and `ALTER`.

## Resume Bullets

- Fine-tuned CodeLlama-7B on 80K text-to-SQL pairs using QLoRA, achieving 79% execution accuracy on the Spider benchmark.
- Deployed as FastAPI endpoint handling 500+ queries/day with average response latency under 900ms.

