from sqlalchemy import create_engine, text

from app.config import DATABASE_URL
from app.utils.logger import get_logger

logger = get_logger(__name__)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)


def test_connection():
    """
    Test SQLite connection.
    """

    with engine.connect() as conn:

        version = conn.execute(
            text("SELECT sqlite_version();")
        ).scalar()

        logger.info(f"SQLite Version: {version}")

        return version


def get_tables():
    """
    Return all tables in database.
    """

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                ORDER BY name;
            """)
        )

        return [row[0] for row in result]
