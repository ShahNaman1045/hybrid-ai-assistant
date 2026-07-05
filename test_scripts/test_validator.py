from app.sql.validator import SQLValidator

queries = [
    "SELECT * FROM customers;",
    "DELETE FROM customers;",
    "DROP TABLE customers;",
    "UPDATE customers SET name='ABC';",
    "SELECT * FROM orders;"
]

for sql in queries:

    print("=" * 70)
    print(sql)

    print(SQLValidator.validate(sql))
