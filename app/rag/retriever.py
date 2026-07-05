import chromadb

from app.config import CHROMA_DB_PATH, TOP_K_RESULTS
from app.llm.client import llm
from app.utils.logger import get_logger

logger = get_logger(__name__)


class DocumentRetriever:

    COLLECTION_NAME = "enterprise_documents"

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=CHROMA_DB_PATH
        )

    def search(
        self,
        question: str,
        top_k: int = TOP_K_RESULTS,
    ) -> dict:

        logger.info("Searching vector database...")

        # Always fetch the latest collection
        collection = self.client.get_collection(
            self.COLLECTION_NAME
        )

        embedding = llm.embedding(question)

        result = collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]

        context = []
        sources = []

        for document, metadata in zip(documents, metadatas):

            context.append(document)

            source = (
                f"{metadata['document']} "
                f"(Page {metadata['page']})"
            )

            if source not in sources:
                sources.append(source)

        logger.info(
            f"Retrieved {len(context)} chunks."
        )

        return {
            "context": "\n\n".join(context),
            "sources": sources,
        }
