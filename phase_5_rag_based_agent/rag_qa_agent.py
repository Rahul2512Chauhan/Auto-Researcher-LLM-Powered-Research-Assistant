# phase_5_rag_based_agent/rag_qa_agent.py

# ----------- Setup the Retrieval Pipeline -----------
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

# Embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": "cpu"}
)

# Load FAISS index
faiss_index_path = "phase_5_rag_based_agent/vectorstore"  # ✅ Corrected path
vectorstore = FAISS.load_local(
    faiss_index_path, 
    embeddings=embedding_model, 
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever()


# ----------- Create the RetrievalQA Chain -----------
from phase_5_rag_based_agent.llm_wrapper import ZephyrLLMWrapper

llm = ZephyrLLMWrapper()  # Wraps the local Zephyr model

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    chain_type="stuff"  # Concatenate context documents into prompt
)


# ----------- Query the QA Chain -----------
def answer_query(query: str, retriever):
    llm = ZephyrLLMWrapper()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff"
    )

    response = qa_chain.invoke({"query": query})
    return response["result"]  # optionally also return source docs


