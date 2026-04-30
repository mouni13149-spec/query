from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TableSchema:
    name: str
    columns: list[str]


@dataclass(frozen=True)
class DatabaseSchema:
    tables: dict[str, TableSchema]

    @classmethod
    def from_file(cls, path: str | Path) -> "DatabaseSchema":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        tables = {
            table["name"]: TableSchema(name=table["name"], columns=list(table["columns"]))
            for table in data["tables"]
        }
        return cls(tables=tables)

    def has_table(self, name: str) -> bool:
        return name in self.tables

    def has_column(self, table: str, column: str) -> bool:
        return self.has_table(table) and column in self.tables[table].columns

    def to_prompt(self) -> str:
        return "\n".join(
            f"{table.name}({', '.join(table.columns)})"
            for table in self.tables.values()
        )

