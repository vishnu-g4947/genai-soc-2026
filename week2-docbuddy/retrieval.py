from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from persistence import load_vector_store

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

def ask(question: str) -> tuple[str, str]:

    vector_store = load_vector_store()

    if vector_store is None:
        return (
            "No documents indexed yet.",
            "No context available."
        )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 5}
    )

    retrieved_docs = retriever.invoke(question)

    context_text = ""

    for doc in retrieved_docs:
        context_text += doc.page_content + "\n\n"

    prompt = PromptTemplate(
        template="""
You are a document question-answering assistant.

Answer ONLY using the provided context.

If the answer is not contained in the context, respond exactly with:

I don't have enough information in the documents.

Context:
{context}

Question:
{question}

Answer:
""",
        input_variables=["context", "question"]
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "context": context_text,
            "question": question
        }
    )

    context_display = ""

    for i, doc in enumerate(retrieved_docs):

        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", 0)

        preview = doc.page_content[:250]

        context_display += f"""
### Chunk {i + 1}

**Source:** {source}

**Page:** {page + 1}

```text
{preview}
```

"""
        
    return (response.content, context_display)