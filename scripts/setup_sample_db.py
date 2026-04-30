from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a sample SQLite store database.")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    db_path = Path(args.output)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    connection = sqlite3.connect(str(db_path))
    try:
        connection.executescript(
            """
            CREATE TABLE customers (
              customer_id INTEGER PRIMARY KEY,
              customer_name TEXT NOT NULL,
              region TEXT NOT NULL
            );

            CREATE TABLE products (
              product_id INTEGER PRIMARY KEY,
              product_name TEXT NOT NULL,
              category TEXT NOT NULL
            );

            CREATE TABLE orders (
              order_id INTEGER PRIMARY KEY,
              customer_id INTEGER NOT NULL,
              order_date TEXT NOT NULL,
              region TEXT NOT NULL,
              total_amount REAL NOT NULL,
              FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
            );

            CREATE TABLE order_items (
              order_item_id INTEGER PRIMARY KEY,
              order_id INTEGER NOT NULL,
              product_id INTEGER NOT NULL,
              quantity INTEGER NOT NULL,
              unit_price REAL NOT NULL,
              FOREIGN KEY(order_id) REFERENCES orders(order_id),
              FOREIGN KEY(product_id) REFERENCES products(product_id)
            );
            """
        )
        connection.executemany(
            "INSERT INTO customers VALUES (?, ?, ?)",
            [
                (1, "Acme Retail", "West"),
                (2, "Northstar Labs", "East"),
                (3, "Summit Foods", "Midwest"),
                (4, "Blue Ridge Co", "West"),
            ],
        )
        connection.executemany(
            "INSERT INTO products VALUES (?, ?, ?)",
            [
                (1, "Analytics Pro", "Software"),
                (2, "Data Sync", "Software"),
                (3, "Support Plan", "Service"),
            ],
        )
        connection.executemany(
            "INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
            [
                (101, 1, "2026-01-15", "West", 1200.0),
                (102, 2, "2026-01-20", "East", 2100.0),
                (103, 3, "2026-02-10", "Midwest", 800.0),
                (104, 4, "2026-02-18", "West", 1700.0),
                (105, 1, "2026-03-05", "West", 950.0),
            ],
        )
        connection.executemany(
            "INSERT INTO order_items VALUES (?, ?, ?, ?, ?)",
            [
                (1, 101, 1, 1, 900.0),
                (2, 101, 3, 1, 300.0),
                (3, 102, 1, 2, 900.0),
                (4, 102, 2, 1, 300.0),
                (5, 103, 2, 2, 400.0),
                (6, 104, 1, 1, 900.0),
                (7, 104, 3, 2, 400.0),
                (8, 105, 2, 1, 650.0),
                (9, 105, 3, 1, 300.0),
            ],
        )
        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    main()

