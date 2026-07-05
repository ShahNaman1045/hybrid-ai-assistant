from app.database.db import test_connection, get_tables

print("SQLite Version:", test_connection())

print("\nTables:\n")

for table in get_tables():
    print(table)
