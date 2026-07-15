from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages

from langgraph.prebuilt import ToolNode, tools_condition

from langgraph.checkpoint.sqlite import SqliteSaver

from langchain_groq import ChatGroq

from typing_extensions import TypedDict, Annotated

import sqlite3

from tools.tools_rag import search_documents
from tools.tools_search import search_web, search_wikipedia
from tools.tools_vision import describe_image

from langchain_core.messages import SystemMessage

class State(TypedDict):
    messages: Annotated[list, add_messages]
    
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

tools = [
    search_documents,
    search_web,
    search_wikipedia,
    describe_image
]

llm_with_tools = llm.bind_tools(tools)

def assistant(state: State):

    system_prompt = SystemMessage(
    content="""
    You are HybridSight, an intelligent assistant.

    You have access to four tools:

    1. search_documents:
       Use this tool whenever the user asks questions about an uploaded PDF.

    2. search_web:
       Use this tool for current events and recent information.

    3. search_wikipedia:
       Use this tool for general knowledge and factual topics.

    4. describe_image:
       Use this tool whenever the user asks about an uploaded image.

    If the user's request does not require any tool, answer directly.
    Do not call a tool unless it is necessary.
    """
)

    response = llm_with_tools.invoke(
        [system_prompt] + state["messages"]
    )

    return {
        "messages": [response]
    }
    
tool_node = ToolNode(tools)

graph = StateGraph(State)

graph.add_node('assistant', assistant)
graph.add_node('tools', tool_node)

graph.add_edge(START, 'assistant')
graph.add_conditional_edges('assistant', tools_condition)
graph.add_edge("tools", "assistant")

conn = sqlite3.connect(
    'chatbot.db',
    check_same_thread=False
)

memory = SqliteSaver(conn)

chatbot = graph.compile(checkpointer= memory)

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in memory.list(None):
        thread_id = checkpoint.config["configurable"]["thread_id"]
        all_threads.add(thread_id)
    return list(all_threads)