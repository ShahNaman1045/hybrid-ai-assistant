from pathlib import Path
from app.database.schema import get_database_schema

schema = get_database_schema()
output_file = Path("data/database/schema.txt")

print("Saving schema to:", output_file.resolve())

output_file.write_text(schema, encoding="utf-8")

print("Schema exported successfully!")
