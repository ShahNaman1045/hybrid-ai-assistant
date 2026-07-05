from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ToolType(str, Enum):
    SQL = "SQL"
    RAG = "RAG"
    BOTH = "BOTH"


@dataclass
class Observation:
    """
    Result returned by any tool.
    """

    tool: ToolType
    success: bool
    content: str
    metadata: dict = field(default_factory=dict)
    sources: list[str] = field(default_factory=list)


@dataclass
class AgentState:
    """
    Maintains the state of the ReAct loop.
    """

    question: str
    observations: list[Observation] = field(default_factory=list)
    final_answer: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
