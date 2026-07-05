from pathlib import Path
import uuid

import chromadb
import fitz

from app.config import (
    CHROMA_DB_PATH,
    DOCUMENT_PATH,
)
from app.llm.client import llm
from app.utils.logger import get_logger

logger = get_logger(__name__)


class DocumentIngestor:
    COLLECTION_NAME = "enterprise_documents"

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=CHROMA_DB_PATH
        )

    def ingest(self):

        logger.info("Preparing Chroma collection...")

        # Delete existing collection if it exists
        try:
            self.client.delete_collection(
                self.COLLECTION_NAME
            )
            logger.info("Existing collection deleted.")
        except Exception:
            logger.info("No existing collection found.")

        self.collection = self.client.create_collection(
            self.COLLECTION_NAME
        )

        documents = list(
            Path(DOCUMENT_PATH).glob("*.pdf")
        )

        logger.info(
            f"Found {len(documents)} PDF documents."
        )

        total_chunks = 0

        for pdf in documents:

            logger.info(f"Reading {pdf.name}")

            chunks = self._extract_chunks(pdf)

            logger.info(
                f"{len(chunks)} chunks extracted."
            )

            for chunk in chunks:
                embedding = llm.embedding(
                    chunk["text"]
                )
                self.collection.add(
                    ids=[str(uuid.uuid4())],
                    documents=[chunk["text"]],
                    embeddings=[embedding],
                    metadatas=[
                        {
                            "document": pdf.name,
                            "page": chunk["page"],
                        }
                    ],
                )

            total_chunks += len(chunks)

        logger.info(
            f"Ingestion completed. "
            f"Indexed {total_chunks} chunks."
        )

    def _extract_chunks(
        self,
        pdf_path: Path,
        chunk_size: int = 1000,
        overlap: int = 200,
    ) -> list[dict]:

        document = fitz.open(pdf_path)
        chunks = []

        for page_number, page in enumerate(document):
            text = page.get_text()
            start = 0

            while start < len(text):
                end = start + chunk_size
                chunks.append(
                    {
                        "text": text[start:end],
                        "page": page_number + 1,
                    }
                )
                start += chunk_size - overlap

        document.close()

        return chunks
