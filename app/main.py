from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from sql_generator.executor import execute_read_only
from sql_generator.generator import generate_sql
from sql_generator.schema import DatabaseSchema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "data" / "schema.json"
DB_PATH = ROOT / "data" / "sample_store.db"

app = FastAPI(title="LLM-Powered SQL Query Generator")


class QueryRequest(BaseModel):
    question: str
    execute: bool = False


@app.post("/generate-sql")
def generate_sql_endpoint(request: QueryRequest) -> dict:
    schema = DatabaseSchema.from_file(SCHEMA_PATH)
    sql = generate_sql(request.question, schema)
    response = {"sql": sql}
    if request.execute:
        response["rows"] = execute_read_only(DB_PATH, sql, schema)
    return response

