from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend import config, utils
import os

def ingest_documents():
    docs = []
    for file_path in utils.list_documents(config.DOC_DIR):
        if file_path.endswith(".pdf"):
            text = utils.pdf_to_text(file_path)
            docs.append({"text": text, "metadata": {"source": file_path}})
        elif file_path.endswith(".txt"):
            with open(file_path, "r") as f:
                docs.append({"text": f.read(), "metadata": {"source": file_path}})
    return docs

def build_vector_store():
    docs = ingest_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP)
    split_docs = []
    for doc in docs:
        for chunk in splitter.split_text(doc["text"]):
            split_docs.append({"text": chunk, "metadata": doc["metadata"]})
    texts = [d["text"] for d in split_docs]
    metadatas = [d["metadata"] for d in split_docs]
    vectordb = Chroma.from_texts(
        texts,
        OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY),
        metadatas=metadatas,
        persist_directory=config.CHROMA_DIR
    )
    vectordb.persist()
    return vectordb

def load_vector_store():
    return Chroma(
        persist_directory=config.CHROMA_DIR,
        embedding_function=OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
    )

if __name__ == "__main__":
    build_vector_store()
    print("Vector store built and persisted.")