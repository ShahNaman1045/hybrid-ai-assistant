from fastapi import APIRouter, HTTPException

from app.agent.react import ReactAgent
from app.api.models import AskRequest, AskResponse
from app.rag.ingest import DocumentIngestor
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="",
    tags=["Hybrid AI Assistant"],
)

agent = ReactAgent()
ingestor = DocumentIngestor()


@router.get("/")
def home():
    return {
        "message": "Hybrid AI Assistant is running."
    }

@router.post(
    "/ask",
    response_model=AskResponse,
)
def ask(request: AskRequest):

    logger.info(f"Question: {request.question}")

    try:
        result = agent.ask(request.question)

        return AskResponse(
            answer=result["answer"],
            sources=result["sources"],
            metadata=result["metadata"],
        )

    except Exception as e:
        logger.exception("Error while processing question.")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.post("/ingest")
def ingest():

    try:
        ingestor.ingest()

        return {
            "success": True,
            "message": "Documents ingested successfully."
        }

    except Exception as e:
        logger.exception("Document ingestion failed.")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
