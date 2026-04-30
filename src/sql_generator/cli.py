from __future__ import annotations

import argparse
import json

from sql_generator.evaluation import execution_accuracy, load_eval_pairs
from sql_generator.executor import execute_read_only
from sql_generator.generator import generate_sql
from sql_generator.schema import DatabaseSchema


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and evaluate SQL from natural language.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate", help="Generate SQL for a question.")
    generate_parser.add_argument("--schema", required=True)
    generate_parser.add_argument("--question", required=True)

    query_parser = subparsers.add_parser("query", help="Generate SQL and run it against SQLite.")
    query_parser.add_argument("--schema", required=True)
    query_parser.add_argument("--db", required=True)
    query_parser.add_argument("--question", required=True)

    eval_parser = subparsers.add_parser("evaluate", help="Evaluate execution accuracy.")
    eval_parser.add_argument("--schema", required=True)
    eval_parser.add_argument("--db", required=True)
    eval_parser.add_argument("--data", required=True)

    args = parser.parse_args()
    schema = DatabaseSchema.from_file(args.schema)
    if args.command == "generate":
        print(generate_sql(args.question, schema))
    elif args.command == "query":
        sql = generate_sql(args.question, schema)
        rows = execute_read_only(args.db, sql, schema)
        print(json.dumps({"sql": sql, "rows": rows}, indent=2))
    elif args.command == "evaluate":
        metrics = execution_accuracy(load_eval_pairs(args.data), args.db, schema)
        print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()

