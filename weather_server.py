from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

#initialize the MCP server
mcp=FastMCP("Weather")

# Constants
NWS_API_BASE="https://api.weather.gov"
USER_AGENT="weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""

    """
    Make an asynchronous GET request to the National Weather Service (NWS) API and return the JSON response.

    This function uses the httpx library to perform a non-blocking HTTP GET request to the given URL.
    It includes proper headers (like User-Agent and Accept) and handles possible errors gracefully.

    If the request is successful and returns a 200 OK status, the JSON content is parsed and returned
    as a Python dictionary. If any error occurs (such as network error, timeout, or bad HTTP status),
    the function catches the exception and returns None instead of crashing.

    Args:
        url (str): The API endpoint URL of the NWS service to fetch data from.

    Returns:
        dict[str, Any] | None:
            - A dictionary containing the parsed JSON response from the API if the request is successful.
            - None if there is an exception (e.g., timeout, invalid response, bad status code).

    Example:
        >>> url = "https://api.weather.gov/gridpoints/MPX/107,71/forecast"
        >>> data = await make_nws_request(url)
        >>> if data:
        >>>     print(data["properties"]["periods"][0]["detailedForecast"])
        >>> else:
        >>>     print("Failed to fetch data.")

    Notes:
        - The request timeout is set to 30 seconds.
        - The Accept header requests a response in GeoJSON format (used for geospatial data).
        - The function uses an async context manager with httpx.AsyncClient to manage the connection.
        - Make sure `USER_AGENT` is defined globally as a valid user-agent string.
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
        Event: {props.get('event', 'Unknown')}
        Area: {props.get('areaDesc', 'Unknown')}
        Severity: {props.get('severity', 'Unknown')}
        Description: {props.get('description', 'No description available')}
        Instructions: {props.get('instruction', 'No specific instructions provided')}
        """

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)



if __name__=="__main__":
    mcp.run(transport="streamable-http")