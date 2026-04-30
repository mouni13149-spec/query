from __future__ import annotations

import re

from sql_generator.schema import DatabaseSchema
from sql_generator.validator import validate_select_sql


def generate_sql(question: str, schema: DatabaseSchema) -> str:
    lowered = question.lower()

    if "sales by region" in lowered or "revenue by region" in lowered:
        sql = "SELECT region, ROUND(SUM(total_amount), 2) AS total_sales FROM orders GROUP BY region ORDER BY total_sales DESC;"
    elif "top" in lowered and "product" in lowered and ("revenue" in lowered or "sales" in lowered):
        limit = extract_limit(lowered, default=5)
        sql = (
            "SELECT p.product_name, ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue "
            "FROM order_items oi JOIN products p ON oi.product_id = p.product_id "
            "GROUP BY p.product_name ORDER BY revenue DESC "
            f"LIMIT {limit};"
        )
    elif "average order" in lowered:
        sql = "SELECT ROUND(AVG(total_amount), 2) AS average_order_value FROM orders;"
    elif "customers" in lowered and "region" in lowered:
        sql = "SELECT region, COUNT(*) AS customer_count FROM customers GROUP BY region ORDER BY customer_count DESC;"
    elif "orders per month" in lowered or "monthly orders" in lowered:
        sql = "SELECT SUBSTR(order_date, 1, 7) AS month, COUNT(*) AS orders FROM orders GROUP BY month ORDER BY month;"
    elif "total orders" in lowered:
        sql = "SELECT COUNT(*) AS total_orders FROM orders;"
    else:
        sql = fallback_query(schema)

    validate_select_sql(sql, schema)
    return sql


def extract_limit(text: str, default: int) -> int:
    match = re.search(r"\btop\s+(\d+)", text)
    if not match:
        return default
    return max(1, min(int(match.group(1)), 100))


def fallback_query(schema: DatabaseSchema) -> str:
    first_table = next(iter(schema.tables.values()))
    return f"SELECT * FROM {first_table.name} LIMIT 10;"

