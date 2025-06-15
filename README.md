<h1 align="center">Fastapi AI Production Boilerplate</h1>

<h3 align="center">Simple starter repo for your Machine Learning/AI projects</h3>
<p align="center">
    <img src="public/thumbnail.png" alt="FastAPI AI Production Template Thumbnail" width="600">
</p>

<p align="center">
    <img src="https://img.shields.io/github/created-at/wahyudesu/Fastapi-AI-Production-Template?color=greenlime&style=flat" alt="Created date">
    <a href="https://github.com/wahyudesu/Fastapi-AI-Production-Template/commits/main">
        <img src="https://img.shields.io/github/last-commit/wahyudesu/Fastapi-AI-Production-Template?style=flat" alt="Last Commit">
    </a>
    <a href="https://github.com/wahyudesu/Fastapi-AI-Production-Template/blob/main/pyproject.toml">
        <img src="https://img.shields.io/badge/python-3.12%2B-greenlime?logo=python&style=flat" alt="Python Version">
    </a>
    <!-- <a href="https://github.com/wahyudesu/Fastapi-AI-Production-Template/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/wahyudesu/Fastapi-AI-Production-Template?color=greenlime&style=flat" alt="GitHub License">
    </a> -->
    <a href="https://sonarcloud.io/summary/new_code?id=wahyudesu_Fastapi-AI-Production-Template">
        <img src="https://sonarcloud.io/api/project_badges/measure?project=IbraheemTuffaha_python-fastapi-template&metric=alert_status&style=flat" alt="Quality Gate Status">
    </a>
    <a href="https://github.com/wahyudesu/Fastapi-AI-Production-Template">
        <img src="https://img.shields.io/github/repo-size/wahyudesu/Fastapi-AI-Production-Template?style=flat" alt="Repo Size">
    </a>
    <a href="https://github.com/wahyudesu">
        <img src="https://img.shields.io/github/followers/wahyudesu?style=flat" alt="Followers">
    </a>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3670A0?style=flat&logo=Python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi&logoColor=white" alt="FastAPI">
    <img src="https://img.shields.io/badge/Docker-%230db7ed.svg?style=flat&logo=Docker&logoColor=white" alt="Docker">
    <img src="https://img.shields.io/badge/Supabase-35bc7f?style=flat&logo=supabase&logoColor=white" alt="Supabase">
    <img src="https://img.shields.io/badge/Langchain-1C3C3C?style=flat&logo=Langchain&logoColor=white" alt="Langchain">
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
│   ├── routers/               # API routers (LLM, feedback, chatbot, etc)
│   │   ├── chatbot.py         # Chatbot endpoints (file upload, entity extraction, plagiarism, etc)
│   │   ├── example.py         # Example endpoints (LLM workflow, feedback, etc)
│   │   └── predict.py         # Prediction endpoints (ML Predict, summarization, relevance, etc)
│   └── model/                 # Model artifacts (pickle)
├── notebook/                  # Jupyter notebooks for experiments
├── public/                    # File static (image, documents, etc)
├── pyproject.toml             # Python dependencies & project config
├── uv.lock                    # Lockfile for uv/poetry
└── README.md                  # Project documentation
```
This modular approach keeps your code organized as your AI application grows in complexity.

> For comprehensive documentation, visit the FastAPI official docs.

## Installation & Setup

Make sure you have [`uv` installed](https://docs.astral.sh/uv/getting-started/installation/) .

```powershell
# Clone repository
git clone https://github.com/wahyudesu/fastapi-ai-template
cd fastapi-ai-template

# Install Python:
uv python install 3.12.8

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


## Run on local
```powershell
uv run fastapi dev
```
or

```powershell
uv run uvicorn main.app:app --reload
```

## Testing

```powershell
uv run pytest
```

## Deployment 

<p align="center">
    <img src="https://img.shields.io/badge/Deploy_on_DigitalOcean-%230167ff.svg?style=for-the-badge&logo=digitalOcean&logoColor=white" alt="DigitalOcean">
    <img src="https://img.shields.io/badge/Deploy_on_GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white" alt="Google Cloud">
    <img src="https://img.shields.io/badge/Deploy_on_Render-%23000000.svg?style=for-the-badge&logo=render&logoColor=white" alt="Render">
    <img src="https://img.shields.io/badge/Deploy_on_Railway-131415?style=for-the-badge&logo=railway&logoColor=white" alt="Railway">
</p>


> Project ini dikembangkan untuk workflow LLMOps/ML pipeline modern, siap untuk deployment di cloud maupun VPS.


## 🤝 Contributing

1. Fork this repository;
2. Create your branch: `git checkout -b my-new-feature`;
3. Commit your changes: `git commit -m 'Add some feature'`;
4. Push to the branch: `git push origin my-new-feature`.
5. After your pull request is merged, you can safely delete your branch.


## FAQ

<details>
    <summary><strong>Why Fastapi?</strong></summary>
    <ul>
        <li>FastAPI is a modern, high-performance web framework for building APIs with Python. For AI apps, it serves as the interface between your AI models and the outside world, allowing external systems to send data to your models and receive predictions or processing results. What makes FastAPI particularly appealing is its simplicity and elegance - it provides everything you need without unnecessary complexity.</li>
    </ul>
</details>

<details>
    <summary><strong>What is uvicorn?</strong></summary>
    <ul>
        <li>Ya, gratis untuk penggunaan secara personal dan non-komersial.</li>
    </ul>
</details>

<details>
    <summary><strong>Can support MCP Server?</strong></summary>
    <ul>
        <li>Ya, gratis untuk penggunaan secara personal dan non-komersial.</li>
    </ul>
</details>

<details>
    <summary><strong>How about security?</strong></summary>
    <ul>
        <li>Ya, open-source dibawah lisensi MIT.</li>
    </ul>
</details>
