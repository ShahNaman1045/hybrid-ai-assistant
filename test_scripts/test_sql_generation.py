from app.sql.generator import SQLGenerator

generator = SQLGenerator()
question = "Top 10 customers by revenue."
sql = generator.generate(question)

print()
print("=" * 80)
print(sql)
