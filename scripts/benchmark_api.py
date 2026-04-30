from __future__ import annotations

import argparse
import time

from sql_generator.generator import generate_sql
from sql_generator.schema import DatabaseSchema


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark local SQL generation latency.")
    parser.add_argument("--schema", default="data/schema.json")
    parser.add_argument("--question", default="What were total sales by region?")
    parser.add_argument("--repeat", type=int, default=500)
    args = parser.parse_args()

    schema = DatabaseSchema.from_file(args.schema)
    started = time.perf_counter()
    for _ in range(args.repeat):
        generate_sql(args.question, schema)
    elapsed = time.perf_counter() - started
    print(f"queries={args.repeat} elapsed_seconds={elapsed:.3f} avg_ms={(elapsed / args.repeat) * 1000:.2f}")


if __name__ == "__main__":
    main()

