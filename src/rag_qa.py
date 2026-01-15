"""
Main entrypoint for GDPR-compliant RAG Q&A system.
End-to-end RAG orchestration with grounded generation.

"""

from rag_pipeline import retriever
from llm import generate_answer

def run_query(question):
    r = retriever()
    docs = r.get_relevant_documents(question)

    if not docs:
        print("Insufficient context to answer this question.")
        return

    context = "\n\n".join([doc.page_content for doc in docs])
    answer = generate_answer(context, question)

    print("QUESTION:", question)
    print("ANSWER:", answer)

if __name__ == "__main__":
    run_query("What is the company's data retention policy?")
