from __future__ import annotations

import re

from sql_generator.schema import DatabaseSchema

BLOCKED_KEYWORDS = {
    "alter",
    "attach",
    "create",
    "delete",
    "drop",
    "insert",
    "pragma",
    "replace",
    "truncate",
    "update",
}


def validate_select_sql(sql: str, schema: DatabaseSchema) -> None:
    normalized = sql.strip().lower()
    if not normalized.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")
    if ";" in normalized[:-1]:
        raise ValueError("Multiple statements are not allowed.")

    tokens = set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", normalized))
    blocked = tokens & BLOCKED_KEYWORDS
    if blocked:
        raise ValueError(f"Blocked SQL keyword: {sorted(blocked)[0]}")

    table_names = extract_table_names(normalized)
    unknown_tables = [table for table in table_names if not schema.has_table(table)]
    if unknown_tables:
        raise ValueError(f"Unknown table: {unknown_tables[0]}")


def extract_table_names(sql: str) -> list[str]:
    names = []
    for pattern in (r"\bfrom\s+([a-zA-Z_][a-zA-Z0-9_]*)", r"\bjoin\s+([a-zA-Z_][a-zA-Z0-9_]*)"):
        names.extend(re.findall(pattern, sql))
    return names

