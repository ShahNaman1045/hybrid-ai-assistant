from app.database.mysql_to_sqlite import MySQLToSQLiteConverter

converter = MySQLToSQLiteConverter(
    mysql_file="data/database/enterprise_orders_mysql.sql",
    sqlite_file="data/database/enterprise.db",
)

converter.convert()
