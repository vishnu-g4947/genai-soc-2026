import os 
from langchain.tools import tool
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

FAISS_PATH = 'faiss_index'

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

def create_vector_store(pdf_path: str):
    
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    chunks = text_splitter.split_documents(documents)
    
    if os.path.exists(FAISS_PATH):
        
        vector_store = FAISS.load_local(
            FAISS_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
        
        vector_store.add_documents(chunks)
        
    else:
        vector_store = FAISS.from_documents(
            chunks,
            embeddings
        )
        
    vector_store.save_local(FAISS_PATH)
    
@tool
def search_documents(query: str)-> str:
    """
    Search the uploaded PDF documents and retrieve relevant information.
    Use this tool whenever the user asks questions about the contents
    of an uploaded PDF, requests a summary of the document, asks for
    specific information contained in the document, or refers to the
    uploaded file using phrases like:
    - "Summarize the document"
    - "Analyze the uploaded PDF"
    - "What does the document say about X?"
    - "Give me the key points"
    - "Find information in the PDF"
    Do not use this tool for general knowledge questions, web searches,
    or image-related queries.
    Args:
        query: The user's question about the uploaded document.
    Returns:
        Relevant text extracted from the uploaded PDF.
    """
    
    if not os.path.exists(FAISS_PATH):
        return "No document has been uploaded yet."
    
    vector_store = FAISS.load_local(
        FAISS_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 2}
    )
    
    docs = retriever.invoke(query)
    
    context = "\n\n".join(
        doc.page_content for doc in docs
    )
    
    return context