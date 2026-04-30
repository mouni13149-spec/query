import unittest

from sql_generator.generator import generate_sql
from sql_generator.schema import DatabaseSchema, TableSchema
from sql_generator.validator import validate_select_sql


class SQLGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.schema = DatabaseSchema(
            tables={
                "orders": TableSchema("orders", ["order_id", "region", "total_amount"]),
                "products": TableSchema("products", ["product_id", "product_name"]),
                "order_items": TableSchema("order_items", ["order_id", "product_id", "quantity", "unit_price"]),
                "customers": TableSchema("customers", ["customer_id", "region"]),
            }
        )

    def test_generate_sales_by_region(self):
        sql = generate_sql("What were total sales by region?", self.schema)

        self.assertIn("SUM(total_amount)", sql)
        self.assertIn("GROUP BY region", sql)

    def test_validator_blocks_delete(self):
        with self.assertRaises(ValueError):
            validate_select_sql("DELETE FROM orders;", self.schema)


if __name__ == "__main__":
    unittest.main()

