from app.config import SCHEMA_PATH
from app.llm.client import ask_llm
from app.prompts.prompt_loader import load_prompt
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SQLGenerator:
    """
    Generates SQLite queries from natural language.
    """

    def __init__(self):

        self.prompt_template = load_prompt(
            "sql_generation.txt"
        )

        if not SCHEMA_PATH.exists():
            raise FileNotFoundError(
                f"Schema file not found: {SCHEMA_PATH}"
            )

        self.schema = SCHEMA_PATH.read_text(
            encoding="utf-8"
        )

    def generate(self, question: str) -> str:

        logger.info("Generating SQL...")

        prompt = (
            self.prompt_template
            .replace("{schema}", self.schema)
            .replace("{question}", question)
        )

        sql = ask_llm(prompt)

        sql = self._clean_sql(sql)

        logger.info(f"Generated SQL:\n{sql}")

        return sql

    @staticmethod
    def _clean_sql(sql: str) -> str:
        """
        Remove markdown formatting if returned by the LLM.
        """

        sql = sql.strip()

        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")

        return sql.strip()
