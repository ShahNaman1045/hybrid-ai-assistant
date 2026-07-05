from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4.1-mini"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "text-embedding-3-small"
)

DATABASE_URL = f"sqlite:///{BASE_DIR / 'data' / 'database' / 'enterprise.db'}"

SCHEMA_PATH = BASE_DIR / "data" / "database" / "schema.txt"

DOCUMENT_PATH = BASE_DIR / "data" / "documents"

CHROMA_DB_PATH = str(BASE_DIR / "chroma_db")

TOP_K_RESULTS = int(
    os.getenv("TOP_K_RESULTS", 5)
)
