"""
Ingestion pipeline for GDPR-compliant enterprise RAG system.

Responsibilities:
- Load approved internal documents
- Chunk content for data minimisation
- Apply PII masking before embedding
- Generate embeddings
- Persist vectors for retrieval

Design focus:
Privacy-by-design and separation of ingestion from query-time processing.
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ibm import WatsonxEmbeddings
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames

from pii_masking import mask_pii

PERSIST_DIRECTORY = "vectorstore"

## Document loader
def document_loader(file_path):
    loader = PyPDFLoader(file_path)
    loaded_document = loader.load()
    return loaded_document

## Text splitter
def text_splitter(data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        length_function=len,
    )
    chunks = text_splitter.split_documents(data)
    return chunks

## Embedding model
def watsonx_embedding():
    embed_params = {
        EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 512,
        EmbedTextParamsMetaNames.RETURN_OPTIONS: {"input_text": True},
    }
    watsonx_embedding = WatsonxEmbeddings(
        model_id="ibm/slate-125m-english-rtrvr-v2",
        url="https://us-south.ml.cloud.ibm.com",
        project_id="2b3c4d5e-6789-4abc-9def-0123456789ab",
        params=embed_params,
    )
    return watsonx_embedding

## Vector db. Create and configure vector databases to store embeddings
def vector_database(chunks):
    # Apply PII masking before embedding (GDPR control)
    for chunk in chunks:
        chunk.page_content = mask_pii(chunk.page_content)

    embedding_model = watsonx_embedding()

    vectordb = Chroma.from_documents(chunks, embedding_model, persist_directory=PERSIST_DIRECTORY)
    vectordb.persist()
    return vectordb

if __name__ == "__main__":
    # Load documents
    documents = document_loader("../data/data.pdf")

    # Split documents into chunks
    chunks = text_splitter(documents)

    # Create and persist vector database
    vector_database(chunks)

    print("Ingestion complete. Vectors persisted to:", PERSIST_DIRECTORY)





