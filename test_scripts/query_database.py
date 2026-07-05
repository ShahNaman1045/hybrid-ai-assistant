import sqlite3

DB_PATH = "data/database/enterprise.db"

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

query = """
SELECT
    quantity,
    unit_price,
    discount_pct
FROM order_items
LIMIT 20;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
