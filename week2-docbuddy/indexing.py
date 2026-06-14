from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import os
from config import embeddings

def index_documents(pdf_paths):

    all_docs = []

    for pdf_path in pdf_paths:

        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        filename = os.path.basename(pdf_path)

        for doc in docs:
            doc.metadata["source"] = filename

        all_docs.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(all_docs)

    vector_store = Chroma(
        collection_name="sample",
        embedding_function=embeddings,
        persist_directory="./chroma_store"
    )

    vector_store.add_documents(chunks)

    return len(chunks)