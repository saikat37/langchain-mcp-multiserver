from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import requests

#initialize the MCP server
mcp=FastMCP("stock")

@mcp.tool()
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=XM21A2B5U6XD8B6T"
    r = requests.get(url)
    return r.json()



if __name__=="__main__":
    mcp.run(transport="stdio")