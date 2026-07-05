import time

from app.agent.final_answer import FinalAnswerGenerator
from app.agent.reasoning import Action, ReasoningEngine
from app.rag.retriever import DocumentRetriever
from app.sql.agent import SQLAgent
from app.sql.formatter import SQLFormatter
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ReactAgent:
    """
    Manual ReAct implementation.

    Flow:

    Question
        ↓
    Reason
        ↓
    Choose Tool
        ↓
    Execute Tool
        ↓
    Observe
        ↓
    Generate Final Answer
    """

    def __init__(self):

        self.reasoning = ReasoningEngine()
        self.sql_agent = SQLAgent()
        self.retriever = DocumentRetriever()
        self.answer_generator = FinalAnswerGenerator()

    def ask(self, question: str) -> dict:

        start_time = time.perf_counter()
        logger.info("=" * 80)
        logger.info("Starting ReAct Agent")

        action = self.reasoning.decide(question)
        logger.info(f"Selected action: {action.value}")
        sql_result = ""
        rag_context = ""
        sources = []

        metadata = {
            "action": action.value
        }

        # ------------------------
        # SQL
        # ------------------------

        if action in (Action.SQL, Action.BOTH):
            sql_response = self.sql_agent.run(question)
            metadata["sql"] = {
                "success": sql_response["success"],
                "row_count": sql_response["row_count"],
                "repaired": sql_response["repaired"],
                "generated_sql": sql_response["generated_sql"],
                "executed_sql": sql_response["executed_sql"],
            }

            sql_result = SQLFormatter.format(sql_response)

        # ------------------------
        # RAG
        # ------------------------

        if action in (Action.RAG, Action.BOTH):
            rag_response = self.retriever.search(question)
            rag_context = rag_response["context"]
            sources.extend(rag_response["sources"])

        # ------------------------
        # Final Answer
        # ------------------------

        answer = self.answer_generator.generate(
            question=question,
            sql_result=sql_result,
            rag_context=rag_context,
        )

        execution_time_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2
        )

        metadata["execution_time_ms"] = execution_time_ms
        metadata["llm_model"] = "gpt-4.1-mini"
        metadata["embedding_model"] = "text-embedding-3-small"

        return {
            "answer": answer,
            "sources": sorted(list(set(sources))),
            "metadata": metadata,
        }
