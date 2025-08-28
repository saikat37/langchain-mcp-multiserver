# MCP LangGraph

A lightweight Multi-Server MCP (Model Control Plane) demo that wires small service adapters (weather, stock, search) into a multi-server agent client using LangGraph / LangChain adapters.

This repository is intended as a development and staging reference for integrating LLMs (Groq, Azure, etc.) with small local microservices using the MCP pattern. It includes:

- `client.py` — sample MultiServer MCP client that launches/attaches to local service servers and creates an agent.
- `search_server.py` — a search MCP server that calls Tavily (or other search provider).
- `stock_server.py` — stock price server (stdio transport).
- `weather_server.py` — weather server (HTTP MCP endpoint).
- `.env` — environment variables (secrets; DO NOT commit to VCS).

## Goals
- Simple, reproducible local development flow using Python.
- Clear separation between compute (LLM client) and small tool services exposed via MCP.
- Production minded README: deployment notes, secrets handling, and testing guidance.

## Quick start (Windows PowerShell)
1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file at the repo root (see Environment variables below).

4. Start servers (each in its own terminal).

```powershell
# HTTP MCP server (weather)
python weather_server.py

# stdio MCP servers
python stock_server.py
python search_server.py

# Run the client which creates the agent and calls tools
python client.py
```

Notes
- If you prefer to have the MCP servers managed as background services, use a process manager (systemd, supervisor, PM2, or Docker Compose). See Deployment below.

## Environment variables
Create a `.env` file and store secrets there. Never commit secrets to git. Example keys required by this project:

- GROQ_API_KEY — Your Groq API key
- TAVILY_API_KEY — Tavily API key for search
- LANGCHAIN_ENDPOINT, LANGCHAIN_API_KEY, LANGCHAIN_PROJECT — (optional) LangSmith / LangChain tracing

Example `.env` (DO NOT paste real keys into source control):

```env
GROQ_API_KEY="your_groq_key_here"
TAVILY_API_KEY="your_tavily_key_here"
# Optional tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="your_langchain_key"
```

## Configuration contract (what components expect)
- Each MCP service exposes a small set of typed tools via `mcp.tool()` decorators. Tools are stateless functions that accept simple inputs and return strings or serializable objects.
- The client expects to find the weather service at `http://localhost:8000/mcp` by default (see `client.py`). Adjust the URL if you run the server on another port.
- `client.py` reads `GROQ_API_KEY` and `GROQ_MODEL` from the environment. Change to Azure or other providers by editing the model instantiation.

## Tests and smoke checks
This repository does not yet include unit tests. Minimal smoke tests you can run manually:

- Verify env variables are loaded

```powershell
python -c "import os; print('GROQ:', bool(os.getenv('GROQ_API_KEY')))
```

- Run `search_server.py` and call its endpoint (if an HTTP transport is used) or run `client.py` to exercise the multi-server flow.

## Production deployment notes
For production, consider the following:

- Containerize services with Docker. Run each service in its own container and use a process orchestrator (Docker Compose, Kubernetes).
- Store secrets in a secret store (Azure Key Vault, AWS Secrets Manager, HashiCorp Vault) or use environment injection via your CI/CD.
- Use health checks and restart policies in your process manager.
- Log to a central location (structured JSON) and attach a log level configuration.
- Pin dependencies in `requirements.txt` and use regular security scans.

Example (Docker Compose) — high level

1. Build images for each server.
2. Configure environment variables via compose secrets or environment files.
3. Expose/route only what is necessary; avoid exposing internal MCP ports publicly.

## Security and privacy
- Do not commit `.env` or any file containing secrets or tokens.
- When connecting to external LLM providers, review their data retention and privacy policy before sending sensitive data.
- Use least privilege API keys when possible.

## Troubleshooting
- If the client fails to reach a tool, confirm the corresponding server is running and the transport configuration (HTTP/stdio) matches between client and server.
- If you see event loop errors when wrapping async functions into synchronous LangChain tools, your environment may already run an event loop (e.g., Jupyter). Use `nest_asyncio` or provide async-capable tooling.
- For HTTP timeouts increase `httpx` timeouts in the server helper.

## Contributing
- Open an issue for design or security discussions before large changes.
- Keep tool signatures stable. If you change a tool's input schema, bump the agent/tool compatibility version.

## License
Specify the license you want to use (e.g., MIT). Add a `LICENSE` file if you change this.

---

If you want, I can:
- Add a `Dockerfile`/`docker-compose.yml` and sample `Makefile` to make deployment reproducible.
- Add a minimal `requirements.txt` with pinned versions and basic unit tests for the tool wrappers.

Tell me which next step you'd like. 
