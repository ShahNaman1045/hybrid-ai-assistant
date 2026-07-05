from app.rag.retriever import DocumentRetriever

retriever = DocumentRetriever()

result = retriever.search(
    "What is the travel reimbursement policy?"
)

print()
print("=" * 80)
print(result["context"])
print()
print(result["sources"])
