from __future__ import annotations

import sqlite3
from pathlib import Path

from sql_generator.schema import DatabaseSchema
from sql_generator.validator import validate_select_sql


def execute_read_only(db_path: str | Path, sql: str, schema: DatabaseSchema) -> list[dict[str, object]]:
    validate_select_sql(sql, schema)
    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(sql).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()

