from sqlalchemy import inspect

from app.database.db import engine
from app.utils.logger import get_logger

logger = get_logger(__name__)


def get_database_schema() -> str:
    """
    Extract database schema including:
    - Tables
    - Columns
    - Primary Keys
    - Foreign Keys

    Returns:
        str: Formatted schema description for the LLM.
    """

    inspector = inspect(engine)

    schema = []

    tables = inspector.get_table_names()

    logger.info(f"Found {len(tables)} tables.")

    for table in sorted(tables):

        schema.append(f"Table: {table}")

        # -------------------------
        # Columns
        # -------------------------
        columns = inspector.get_columns(table)

        for column in columns:
            schema.append(
                f"  - {column['name']} ({column['type']})"
            )

        # -------------------------
        # Primary Key
        # -------------------------
        primary_key = inspector.get_pk_constraint(table)

        if primary_key and primary_key.get("constrained_columns"):
            pk_columns = ", ".join(
                primary_key["constrained_columns"]
            )
            schema.append(f"  Primary Key: {pk_columns}")

        # -------------------------
        # Foreign Keys
        # -------------------------
        foreign_keys = inspector.get_foreign_keys(table)

        if foreign_keys:

            schema.append("  Foreign Keys:")

            for fk in foreign_keys:

                source_columns = ", ".join(
                    fk["constrained_columns"]
                )

                target_columns = ", ".join(
                    fk["referred_columns"]
                )

                schema.append(
                    f"    {source_columns} -> "
                    f"{fk['referred_table']}.{target_columns}"
                )

        schema.append("")

    logger.info("Schema extraction completed successfully.")

    return "\n".join(schema)
