from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import config

def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL
    )

def get_vector_store(chunks):
    embedding_model = get_embedding_model()
    vector_store = FAISS.from_documents(
        documents= chunks,
        embedding=embedding_model
    )

    return vector_store