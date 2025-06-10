<h1 align="center">Fastapi AI Production Template</h1>

<p align="center">Simple starter template for your Machine Learning/AI projects.</p>

<p align="center">
    <a href="https://github.com/wahyudesu/Fastapi-AI-Production-Template">
        <img src="https://img.shields.io/github/last-commit/wahyudesu/Fastapi-AI-Production-Template?style=flat-square" alt="Last Commit">
    </a>
    <a href="https://github.com/wahyudesu/Fastapi-AI-Production-Template">
        <img src="https://img.shields.io/github/languages/top/wahyudesu/Fastapi-AI-Production-Template?style=flat-square" alt="Top Language">
    </a>
    <a href="https://github.com/wahyudesu/Fastapi-AI-Production-Template">
        <img src="https://img.shields.io/github/languages/count/wahyudesu/Fastapi-AI-Production-Template?style=flat-square" alt="Languages Count">
    </a>
    <a href="https://github.com/wahyudesu/Fastapi-AI-Production-Template">
        <img src="https://img.shields.io/github/repo-size/wahyudesu/Fastapi-AI-Production-Template?style=flat-square" alt="Repo Size">
    </a>
    <a href="https://github.com/wahyudesu">
        <img src="https://img.shields.io/github/followers/wahyudesu?style=flat-square" alt="Followers">
    </a>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi&logoColor=white" alt="FastAPI">
    <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white" alt="Docker">
    <img src="https://img.shields.io/badge/Supabase-3ECF8E?style=flat&logo=supabase&logoColor=white" alt="Supabase">
    <img src="https://img.shields.io/badge/langchain-1C3C3C?style=flat&logo=langchain&logoColor=white" alt="Langchain">
    <img src="https://img.shields.io/badge/Pydantic-E92063?style=flat&logo=Pydantic&logoColor=white" alt="Pydantic">
</p>

## Use Case
- Build and serve machine learning models via production-ready APIs
- Create scalable and easily deployable AI/ML backend services
- Develop AI Agent applications based on FastAPI
- Integrate LLM workflows, monitoring, and prompt management
- Support end-to-end model experimentation, deployment, and monitoring


## Features
- [`FastAPI`](https://fastapi.tiangolo.com/) for API and backend
- [`LangChain`](https://www.langchain.com/) for LLM integration and AI workflows
- [`Groq`](https://groq.com/) for fast LLM inference and model provider
- [`uv`](https://docs.astral.sh/uv/) for Python environment management
- [`Docker`](https://www.docker.com/) for containerization
- [`PostgreSQL`](https://www.postgresql.org/) for database
- [`Ruff`](https://docs.astral.sh/ruff/) for Python linting and formatting
- [`Opik`](https://www.comet.com/site/products/opik/) for ai agent and prompt management monitoring

## Project structure

```
root-project/
├── app/
│   ├── main.py                # FastAPI app entrypoint
│   ├── dependencies.py        # Dependency injection (token, etc)
│   ├── internal/              # Internal/private routers (e.g. admin)
│   ├── routers/               # API routers ()
│   │   ├── assignment.py      # Assignment upload & analysis endpoints
│   │   ├── feedback.py        # AI feedback endpoints (LLM, LangChain, etc)
│   │   ├── users.py           # User management endpoints
│   │   └── items.py           # Example endpoints
│   └── model/                 # Model artifacts (pickle, etc)
│       └── pickle/
│           └── best_model-1.pkl
├── notebook/                  # Jupyter notebooks for experiments
├── public/                    # File file statis
├── .env                       # Environment variables (API keys, etc)
├── pyproject.toml             # Python dependencies & project config
├── uv.lock                    # Lockfile for uv/poetry
└── README.md                  # Project documentation
```

## Installation & Setup (Local)

```powershell
# Clone repository
git clone https://github.com/wahyudesu/fastapi-ai-template
cd fastapi-ai-template

# Development
uv venv
.venv\Scripts\activate
uv sync

# Copy and edit .env file
cp .env.example .env
# Edit .env according to your needs

# Build & start all services (FastAPI, Airflow, MLflow, monitoring, etc.)
docker compose up --build -d

# Check service status
docker compose ps
```

## Testing

```powershell
uv run pytest
```

## Deployment GCP

1. Deploy VM (Ubuntu) di GCP Compute Engine
2. Install Docker & Docker Compose di VM
3. Clone repo & copy `.env` ke VM
4. Jalankan:
   ```bash
   docker compose up --build -d
   ```
5. (Opsional) Setup Nginx reverse proxy & SSL untuk domain


> Project ini dikembangkan untuk workflow LLMOps/ML pipeline modern, siap untuk deployment di cloud maupun VPS.

## FAQ
1. **Apakah ini gratis?**
  - Ya, gratis untuk penggunaan secara personal dan non-komersial.
2. **Apakah ini open-source?**
  - Ya, open-source dibawah lisensi MIT.

