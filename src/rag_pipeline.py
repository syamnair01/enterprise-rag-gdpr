"""
Retrieval and generation pipeline for enterprise RAG system.

Responsibilities:
- Load persisted vector database
- Perform similarity-based retrieval
- Assemble contextual input
- Enforce grounded generation
- Log retrieval activity for auditability

This pipeline intentionally prioritises transparency and governance
over response creativity.
"""
from langchain.vectorstores import Chroma
from langchain_ibm import WatsonxEmbeddings
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames

PERSIST_DIRECTORY = "vectorstore"

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

## Retriever
def retriever():
    embedding_model = watsonx_embedding()
    vectordb = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_model
    )
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})
    return retriever

