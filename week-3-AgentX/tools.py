from datetime import date

from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
import wikipediaapi

# =========================
# Custom Tool
# =========================


@tool
def get_current_date() -> str:
    """
    Returns today's date.

    Use this tool whenever the user asks about:
    - latest
    - current
    - today
    - this year
    """
    return date.today().isoformat()


# =========================
# DuckDuckGo Search Tool
# =========================

search = DuckDuckGoSearchRun()


@tool
def duckduckgo_search(query: str) -> str:
    """Search the web for recent information."""
    return search.invoke(query)


# =========================
# Wikipedia Tool
# =========================

wiki = wikipediaapi.Wikipedia(user_agent="AgentX/1.0", language="en")


@tool
def wikipedia(query: str) -> str:
    """Search Wikipedia for encyclopedic information."""

    page = wiki.page(query)

    if not page.exists():
        return f"No Wikipedia article found for '{query}'."

    return page.summary[:10000]


# =========================
# Export all tools
# =========================

tools = [
    get_current_date,
    duckduckgo_search,
    wikipedia,
]
