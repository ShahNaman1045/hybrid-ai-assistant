from app.llm.client import ask_llm
from app.prompts.prompt_loader import load_prompt
from app.utils.logger import get_logger

logger = get_logger(__name__)


class FinalAnswerGenerator:
    """
    Generates the final natural language answer
    using SQL results and/or document context.
    """

    def __init__(self):

        self.prompt = load_prompt(
            "final_answer.txt"
        )

    def generate(
        self,
        question: str,
        sql_result: str = "",
        rag_context: str = "",
    ) -> str:

        logger.info("Generating final answer...")

        prompt = (
            self.prompt
            .replace("{question}", question)
            .replace("{sql_result}", sql_result)
            .replace("{rag_context}", rag_context)
        )

        answer = ask_llm(
            prompt,
            temperature=0
        )

        logger.info("Final answer generated.")

        return answer
