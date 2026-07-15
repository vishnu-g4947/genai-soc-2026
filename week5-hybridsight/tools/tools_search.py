from langchain.tools import tool

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import WikipediaQueryRun

from langchain_community.utilities import WikipediaAPIWrapper

search = DuckDuckGoSearchRun()

wikipedia = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper()
)

@tool
def search_web(query: str) -> str:
    """
    Search the internet for recent information and current events.

    Use this tool whenever the user asks about:

    - Recent news
    - Current events
    - Latest developments
    - Trending topics
    - Information that may have changed over time

    Examples:

    - "What happened in AI this week?"
    - "Latest cricket scores"
    - "Who won yesterday's match?"
    - "Current weather in Mumbai"

    Do not use this tool for PDF questions, image analysis,
    or timeless factual knowledge.

    Args:
        query: The user's search query.

    Returns:
        Relevant information retrieved from the web.
    """
    
    result = search.invoke(query)
    return result

@tool
def search_wikipedia(query: str) -> str:
    """
    Search Wikipedia for general knowledge and factual information.

    Use this tool for educational topics, historical facts,
    scientific concepts, biographies, and subjects that do not
    require real-time information.

    Examples:

    - "Who was Albert Einstein?"
    - "Explain quantum computing"
    - "What is recursion?"
    - "Tell me about the French Revolution"

    Do not use this tool for uploaded PDFs, current events,
    or image-related questions.

    Args:
        query: The user's question.

    Returns:
        Relevant information from Wikipedia.
    """
    result = wikipedia.invoke(query)
    return result