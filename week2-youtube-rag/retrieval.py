from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import config


def get_retriever(vector_store):
    return vector_store.as_retriever(
        search_kwargs={"k": 3}
    )


def get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=config.GROQ_API_KEY,
        temperature=0
    )


def answer_question(query, retriever):
    docs = retriever.invoke(query)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    prompt = PromptTemplate(
        template="""
You are a helpful assistant.

Use the provided context to answer the question.

If the context contains partial information,

provide the best answer possible based on the context.

Only say

"I don't have enough information from the video transcript."

if the context contains no relevant information.

Context:

{context}

Question:

{question}
""",
        input_variables=["context", "question"]
    )

    llm = get_llm()

    final_prompt = prompt.invoke(
        {
            "context": context,
            "question": query
        }
    )

    response = llm.invoke(final_prompt)

    return response.content, docs