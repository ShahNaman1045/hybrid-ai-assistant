from app.utils.logger import get_logger

logger = get_logger(__name__)


class SQLFormatter:
    """
    Formats SQL query results into compact text
    for the final LLM prompt.
    """

    @staticmethod
    def format(result: dict, max_rows: int = 10) -> str:
        """
        Convert SQL result into a compact table.

        Example:

        Customer | Revenue
        ABC Ltd | 12000
        XYZ Ltd | 11000
        """

        if not result["success"]:
            return f"SQL Execution Failed.\nError: {result['error']}"

        rows = result["rows"]

        if not rows:
            return "No records found."

        columns = result["columns"]

        output = []

        formatted_columns = [
            column.replace("_", " ").title()
            for column in columns
        ]

        output.append(" | ".join(formatted_columns))
        output.append("-" * 80)

        for row in rows[:max_rows]:

            values = []

            for column in columns:
                values.append(str(row[column]))

            output.append(" | ".join(values))

        if len(rows) > max_rows:
            output.append("")
            output.append(
                f"... {len(rows) - max_rows} more rows omitted ..."
            )

        logger.info("SQL result formatted.")

        return "\n".join(output)
