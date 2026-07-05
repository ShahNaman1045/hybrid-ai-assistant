from openai import OpenAI

from app.config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    EMBEDDING_MODEL,
)
from app.utils.logger import get_logger

logger = get_logger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)


class OpenAIClient:

    def __init__(self):
        self.client = client

    def ask(
        self,
        prompt: str,
        temperature: float = 0,
    ) -> str:

        logger.info("Calling OpenAI Chat Model...")

        response = self.client.responses.create(
            model=OPENAI_MODEL,
            input=prompt,
            temperature=temperature,
        )

        return response.output_text.strip()

    def embedding(self, text: str) -> list[float]:

        logger.info("Creating embedding...")

        response = self.client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text,
        )

        return response.data[0].embedding


llm = OpenAIClient()


def ask_llm(prompt: str, temperature: float = 0) -> str:
    """
    Wrapper around the OpenAI client with basic error handling.
    """

    try:
        return llm.ask(prompt, temperature)

    except Exception as e:
        logger.exception("OpenAI request failed.")
        raise RuntimeError(
            f"Failed to communicate with OpenAI: {e}"
        ) from e
