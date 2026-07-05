from pathlib import Path

from app.utils.logger import get_logger

logger = get_logger(__name__)

# app/prompts/
PROMPTS_DIR = Path(__file__).parent


def load_prompt(filename: str) -> str:
    """
    Load a prompt file from the prompts directory.

    Args:
        filename: Prompt file name (e.g. sql_generation.txt)

    Returns:
        Prompt text.
    """

    file_path = PROMPTS_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {file_path}"
        )

    logger.info(f"Loaded prompt: {filename}")

    return file_path.read_text(
        encoding="utf-8"
    ).strip()
