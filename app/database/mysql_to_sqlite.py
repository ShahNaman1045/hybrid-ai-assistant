import re
import sqlite3
from pathlib import Path

from app.utils.logger import get_logger

logger = get_logger(__name__)


class MySQLToSQLiteConverter:
    def __init__(self, mysql_file: str, sqlite_file: str):
        self.mysql_file = Path(mysql_file)
        self.sqlite_file = Path(sqlite_file)

    def clean_mysql_sql(self, sql: str) -> str:
        """
        Converts a MySQL dump into SQLite-compatible SQL.
        """

        # Remove MySQL SET statements
        sql = re.sub(r"SET .*?;", "", sql)

        # Remove ENGINE definitions
        sql = re.sub(r"ENGINE=InnoDB", "", sql)

        # Remove CHARSET definitions
        sql = re.sub(r"DEFAULT CHARSET=\w+", "", sql)

        # Remove COLLATE definitions
        sql = re.sub(r"COLLATE=\w+", "", sql)

        # Replace AUTO_INCREMENT
        sql = sql.replace(
            "INT AUTO_INCREMENT PRIMARY KEY",
            "INTEGER PRIMARY KEY AUTOINCREMENT",
        )

        # Replace BOOLEAN type
        sql = sql.replace("TINYINT(1)", "INTEGER")

        # Replace DECIMAL
        sql = re.sub(
            r"DECIMAL\(\d+,\d+\)",
            "REAL",
            sql,
        )

        # Replace ENUM(...) with TEXT
        sql = re.sub(
            r"ENUM\([^)]+\)",
            "TEXT",
            sql,
        )

        # Remove unsigned
        sql = sql.replace("UNSIGNED", "")

        return sql

    def convert(self):

        logger.info("Reading MySQL dump...")

        sql = self.mysql_file.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        sql = self.clean_mysql_sql(sql)

        logger.info("Creating SQLite database...")

        conn = sqlite3.connect(self.sqlite_file)

        conn.executescript(sql)

        conn.commit()
        conn.close()

        logger.info("SQLite database created successfully!")
