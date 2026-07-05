import re

from app.utils.logger import get_logger

logger = get_logger(__name__)


class SQLValidator:
    """
    Validates that generated SQL is safe to execute.
    Only SELECT queries are allowed.
    """

    FORBIDDEN_KEYWORDS = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "CREATE",
        "TRUNCATE",
        "REPLACE",
        "MERGE",
        "ATTACH",
        "DETACH",
        "PRAGMA",
        "VACUUM",
    ]

    @classmethod
    def validate(cls, sql: str) -> bool:
        """
        Returns True if SQL is safe.
        """

        sql = sql.strip()

        if not sql:
            logger.error("Generated SQL is empty.")
            return False

        if not sql.upper().startswith("SELECT"):
            logger.error("Only SELECT statements are allowed.")
            return False

        normalized_sql = re.sub(r"\s+", " ", sql.upper())

        for keyword in cls.FORBIDDEN_KEYWORDS:

            if re.search(rf"\b{keyword}\b", normalized_sql):
                logger.error(f"Forbidden SQL keyword detected: {keyword}")
                return False

        logger.info("SQL validation passed.")

        return True
