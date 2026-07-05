from enum import Enum

from app.llm.client import ask_llm
from app.prompts.prompt_loader import load_prompt
from app.utils.logger import get_logger

logger = get_logger(__name__)


class Action(str, Enum):
    SQL = "SQL"
    RAG = "RAG"
    BOTH = "BOTH"


class ReasoningEngine:
    """
    Decides whether a question requires:
    - SQL
    - RAG
    - BOTH

    This is the first step of our manual ReAct loop.
    """

    def __init__(self):
        self.prompt_template = load_prompt("reasoning.txt")

    def decide(self, question: str) -> Action:

        logger.info("Starting reasoning step.")

        prompt = self.prompt_template.replace(
            "{question}",
            question.strip(),
        )

        response = ask_llm(prompt).strip().upper()
        logger.info(f"Reasoning result: {response}")

        if response == Action.SQL.value:
            return Action.SQL

        if response == Action.RAG.value:
            return Action.RAG

        if response == Action.BOTH.value:
            return Action.BOTH

        logger.warning(
            "Unexpected LLM output. Falling back to BOTH."
        )

        return Action.BOTH
