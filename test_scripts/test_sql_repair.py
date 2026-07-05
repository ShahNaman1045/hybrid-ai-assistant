from app.sql.repair import SQLRepair

repair = SQLRepair()

question = "Top 10 customers by revenue."

bad_sql = """
SELECT *
FROM customer;
"""

error = "no such table: customer"

fixed_sql = repair.repair(
    question=question,
    sql=bad_sql,
    error=error,
)

print(fixed_sql)
