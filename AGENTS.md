# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastAPI AI Production Boilerplate - a minimal, production-ready starter for ML/AI backend services. Built with FastAPI, LangChain/LangGraph, and uvicorn.

## Common Commands

```bash
# Install dependencies
uv sync

# Development server (http://localhost:8000)
uv run uvicorn app.main:app --reload

# Lint with ruff
uv run ruff check

# Format with ruff
uv run ruff format

# Run pre-commit hooks
uv run pre-commit run --all-files

# Docker build
docker build -t fastapi-app .

# Docker run (port 80 inside container mapped to 8000)
docker run -p 8000:80 fastapi-app
```

## Architecture

### Entry Point: `app/main.py`
- Creates FastAPI app with title/description/version
- Includes 4 routers: `agent`, `chatbot`, `predict`, `mcp`
- Mounts FastApiMCP for MCP protocol
- Bearer token auth on all endpoints (via `verify_token` dependency)
- Scalar API docs at `/scalar`, Swagger at `/docs`

### Middleware: `app/middleware.py`
- `Middleware` class: per-IP rate limiting (60 req/min default) + request logging
- Logs URL, method, process_time via loguru

### Logging: `app/logger.py`
- Loguru logger writing to `app.log` with 10MB rotation

### Routers (`app/routers/`)
- **`agent.py`** - LangGraph agent with TavilySearch tool. Endpoints: `GET /agents/graph` (PNG diagram), `POST /agents/ask` (chat)
- **`chatbot.py`** - Simple LangChain chain with Groq LLM. `POST /chatbot/ask`
- **`predict.py`** - Iris species prediction via sklearn RandomForest. `POST /predict/iris`
- **`mcp.py`** - MCP endpoint serving CSV data. `GET /mcp/books`

### Model: `app/model/model-randomforest.pkl`
- Pre-trained sklearn RandomForest for Iris dataset (4 features → 1 species prediction)

### Notebooks (`notebooks/`)
- `iris-knn.ipynb`, `iris-randomforest.ipynb` - ML experiments
- `ai-agents/` - LangChain/LangGraph agent experiments

### Kubernetes (`k8s/`)
- `deployment.yaml`, `service.yaml`, `ingress.yaml`, `hpa.yaml`

## API Authentication

All endpoints protected by Bearer token. Token set via `API_TOKEN` env var. Pass as:
```
Authorization: Bearer <token>
```

## Environment Variables

```
GROQ_API_KEY      - Groq API key for LLM
TAVILY_API_KEY    - Tavily search API key
API_TOKEN         - Bearer token for endpoint protection
DEBUG             - Debug flag
```

## Key Libraries

- **FastAPI** + **uvicorn** - Web framework
- **LangChain** + **LangGraph** - AI agent orchestration
- **ruff** - Linting/formatting (config in `ruff.toml`)
- **loguru** - Logging
- **pre-commit** - Git hooks (config in `.pre-commit-config.yaml`)
