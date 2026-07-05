from app.sql.executor import SQLExecutor

executor = SQLExecutor()

sql = """
SELECT *
FROM customers
LIMIT 5;
"""

result = executor.execute(sql)

print(result)
