from __future__ import annotations

import json
from pathlib import Path

from sql_generator.executor import execute_read_only
from sql_generator.generator import generate_sql
from sql_generator.schema import DatabaseSchema


def load_eval_pairs(path: str | Path) -> list[dict[str, str]]:
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def execution_accuracy(pairs: list[dict[str, str]], db_path: str | Path, schema: DatabaseSchema) -> dict[str, float]:
    correct = 0
    for pair in pairs:
        predicted_sql = generate_sql(pair["question"], schema)
        predicted_rows = execute_read_only(db_path, predicted_sql, schema)
        expected_rows = execute_read_only(db_path, pair["sql"], schema)
        if normalize_rows(predicted_rows) == normalize_rows(expected_rows):
            correct += 1
    return {
        "examples": float(len(pairs)),
        "execution_accuracy": correct / len(pairs) if pairs else 0.0,
    }


def normalize_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return sorted(rows, key=lambda row: json.dumps(row, sort_keys=True))

