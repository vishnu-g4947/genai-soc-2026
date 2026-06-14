import os
from langchain_chroma import Chroma

from config import embeddings


def load_vector_store():

    if not os.path.exists("./chroma_store"):
        return None

    vector_store = Chroma(
        collection_name="sample",
        embedding_function=embeddings,
        persist_directory="./chroma_store"
    )

    return vector_store