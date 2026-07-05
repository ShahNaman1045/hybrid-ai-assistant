from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database.db import engine
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SQLExecutor:
    """
    Executes validated SQL queries against the SQLite database.
    """

    def execute(self, sql: str) -> dict:
        """
        Execute a SQL query and return the result.

        Returns:
        {
            "success": bool,
            "columns": [...],
            "rows": [...],
            "row_count": int,
            "error": str | None
        }
        """

        logger.info("Executing SQL query.")

        try:
            with engine.connect() as conn:

                result = conn.execute(text(sql))

                columns = list(result.keys())

                rows = [
                    dict(zip(columns, row))
                    for row in result.fetchall()
                ]

                logger.info(
                    f"Query executed successfully. "
                    f"Rows returned: {len(rows)}"
                )

                return {
                    "success": True,
                    "columns": columns,
                    "rows": rows,
                    "row_count": len(rows),
                    "error": None,
                }

        except SQLAlchemyError as e:

            logger.error(f"SQL Execution Error: {e}")

            return {
                "success": False,
                "columns": [],
                "rows": [],
                "row_count": 0,
                "error": str(e),
            }

        except Exception as e:

            logger.exception("Unexpected database error.")

            return {
                "success": False,
                "columns": [],
                "rows": [],
                "row_count": 0,
                "error": str(e),
            }
