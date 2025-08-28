from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize the MCP server
mcp = FastMCP("search")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
BASE_URL = "https://api.tavily.com"

@mcp.tool()
def tavily_search(query: str, max_results: int = 5) -> dict[str, Any]:
    """
    Perform a Tavily web search.
    Args:
        query: The search query string.
        max_results: Maximum number of results to return (default 5).
    Returns:
        JSON response from Tavily API.
    """
    url = f"{BASE_URL}/search"
    headers = {"Authorization": f"Bearer {TAVILY_API_KEY}"}
    payload = {"query": query, "max_results": max_results}
    
    with httpx.Client() as client:
        response = client.post(url, headers=headers, json=payload)
    return response.json()

@mcp.tool()
def tavily_news(topic: str, days: int = 3) -> dict[str, Any]:
    """
    Fetch the latest news from Tavily.
    Args:
        topic: The topic to search news for.
        days: How many past days to fetch news (default 3).
    Returns:
        JSON response with news articles.
    """
    url = f"{BASE_URL}/news"
    headers = {"Authorization": f"Bearer {TAVILY_API_KEY}"}
    payload = {"query": topic, "days": days}
    
    with httpx.Client() as client:
        response = client.post(url, headers=headers, json=payload)
    return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio")
