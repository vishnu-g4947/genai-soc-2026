from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tools import tools
from typing import TypedDict, Annotated
from langchain_core.messages import SystemMessage, BaseMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

llm_with_tools = llm.bind_tools(tools)


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


system_prompt = SystemMessage(content=("""
            You are AgentX.

            IMPORTANT TOOL RULES:

            1. Whenever the user asks about any person,
            biography,
            CEO,
            founder,
            scientist,
            politician,
            actor,
            company,
            organization,
            country,
            place,
            historical event,
            or concept,

            ALWAYS call the Wikipedia tool FIRST.

            Do NOT answer these questions using your own knowledge.

            2. Only answer directly if the Wikipedia tool fails.

            3. Use DuckDuckGo only for:
            - latest news
            - recent events
            - today's information
            - current prices
            - live data

            4. Use the current date tool whenever the user asks about:
            - today
            - current date
            - this year
            - latest"""))


def assistant_node(state: AgentState):
    response = llm_with_tools.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}


tool_node = ToolNode(tools)

graph_builder = StateGraph(AgentState)

graph_builder.add_node("assistant", assistant_node)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "assistant")
graph_builder.add_conditional_edges("assistant", tools_condition)
graph_builder.add_edge("tools", "assistant")

conn = sqlite3.connect(database="agent_memory.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

chatbot = graph_builder.compile(checkpointer=checkpointer)


def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)
