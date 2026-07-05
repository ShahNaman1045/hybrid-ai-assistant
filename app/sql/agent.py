from app.sql.executor import SQLExecutor
from app.sql.generator import SQLGenerator
from app.sql.repair import SQLRepair
from app.sql.validator import SQLValidator
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SQLAgent:
    """
    Complete SQL pipeline.

    Flow:

    Question
        ↓
    Generate SQL
        ↓
    Validate
        ↓
    Execute
        ↓
    Success?
        │
      Yes ───────────────► Return
        │
        ▼
    Repair SQL
        ↓
    Validate
        ↓
    Execute
        ↓
    Return
    """

    def __init__(self):

        self.generator = SQLGenerator()
        self.executor = SQLExecutor()
        self.repair = SQLRepair()

    def run(self, question: str) -> dict:

        logger.info("=" * 80)
        logger.info("Starting SQL Agent")

        generated_sql = self.generator.generate(question)

        if not SQLValidator.validate(generated_sql):

            return {
                "success": False,
                "question": question,
                "generated_sql": generated_sql,
                "executed_sql": None,
                "rows": [],
                "columns": [],
                "row_count": 0,
                "repaired": False,
                "error": "Generated SQL failed validation."
            }

        result = self.executor.execute(generated_sql)

        if result["success"]:

            return {
                "success": True,
                "question": question,
                "generated_sql": generated_sql,
                "executed_sql": generated_sql,
                "rows": result["rows"],
                "columns": result["columns"],
                "row_count": result["row_count"],
                "repaired": False,
                "error": None
            }

        logger.info("Execution failed. Trying SQL repair...")

        repaired_sql = self.repair.repair(
            question=question,
            sql=generated_sql,
            error=result["error"],
        )

        if not SQLValidator.validate(repaired_sql):

            return {
                "success": False,
                "question": question,
                "generated_sql": generated_sql,
                "executed_sql": repaired_sql,
                "rows": [],
                "columns": [],
                "row_count": 0,
                "repaired": True,
                "error": "Repaired SQL failed validation."
            }

        repaired_result = self.executor.execute(
            repaired_sql
        )

        return {
            "success": repaired_result["success"],
            "question": question,
            "generated_sql": generated_sql,
            "executed_sql": repaired_sql,
            "rows": repaired_result["rows"],
            "columns": repaired_result["columns"],
            "row_count": repaired_result["row_count"],
            "repaired": True,
            "error": repaired_result["error"]
        }
