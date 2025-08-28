from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_openai import AzureChatOpenAI

from dotenv import load_dotenv
load_dotenv()

import asyncio
print("hello")

async def main():
    client=MultiServerMCPClient(
        {
            "weather": {
                "url": "http://localhost:8000/mcp",  # Ensure server is running here
                "transport": "streamable_http",
            },
            "stock": {
                "command": "python",  # Command to run the stock server
                "args": ["stock_server.py"],  # Arguments for the command
                "transport": "stdio",
            },
            "search": {
                "command": "python",  # Command to run the search server
                "args": ["search_server.py"],  # Arguments for the command
                "transport": "stdio",
            },

        }
    )

    import os
    os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

    tools=await client.get_tools()

    
    # Print information about available tools
    print("=" * 50)
    print("AVAILABLE TOOLS:")
    print("=" * 50)
    for i, tool in enumerate(tools, 1):
        print(f"\n{i}. Tool Name: {tool.name}")
        print(f"   Description: {tool.description}")
        if hasattr(tool, 'args_schema') and tool.args_schema:
            print(f"   Parameters: {tool.args_schema}")
        print("-" * 30)
    
    print(f"\nTotal tools available: {len(tools)}")
    print("=" * 50)
    
    model = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="openai/gpt-oss-20b"
    )
    agent=create_react_agent(
        model,tools
    )

    print("\nSending query...")
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "get me the stock price of AAPL, and whats the weather in New York, whats the recent news in ai ?"}]}
    )
    print("response:", response['messages'][-1].content)


asyncio.run(main())