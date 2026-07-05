from app.config import SCHEMA_PATH
from app.llm.client import ask_llm
from app.prompts.prompt_loader import load_prompt
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SQLRepair:
    """
    Repairs failed SQL queries using the LLM.
    """

    def __init__(self):

        self.prompt_template = load_prompt(
            "sql_repair.txt"
        )

        if not SCHEMA_PATH.exists():
            raise FileNotFoundError(
                f"Schema file not found: {SCHEMA_PATH}"
            )

        self.schema = SCHEMA_PATH.read_text(
            encoding="utf-8"
        )

    def repair(
        self,
        question: str,
        sql: str,
        error: str,
    ) -> str:

        logger.info("Repairing SQL...")

        prompt = (
            self.prompt_template
            .replace("{schema}", self.schema)
            .replace("{question}", question)
            .replace("{sql}", sql)
            .replace("{error}", error)
        )

        repaired_sql = ask_llm(prompt)

        repaired_sql = self._clean_sql(
            repaired_sql
        )

        logger.info(
            f"Repaired SQL:\n{repaired_sql}"
        )

        return repaired_sql

    @staticmethod
    def _clean_sql(sql: str) -> str:

        sql = sql.strip()

        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")

        return sql.strip()
