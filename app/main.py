import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer  # security scheme
from fastapi_mcp import FastApiMCP
from .routers import agent, chatbot, predict, mcp
from .logger import logger
from .middleware import Middleware
from scalar_fastapi import get_scalar_api_reference, Layout, Theme

load_dotenv()

security = HTTPBearer()

API_TOKEN = os.getenv("API_TOKEN")

app = FastAPI(
    title="FastAPI Project",
    description="Simple FastAPI boilerplate for your AI/ML projects.",
    version="1.0.0",
)

app.include_router(agent.router)  # research agent
app.include_router(predict.router)  # ml predict
app.include_router(chatbot.router)  # chatbot
app.include_router(mcp.router)  # mcp weather service

app.add_middleware(Middleware)

# Create an MCP server based on this app
mcp = FastApiMCP(
    app,
    include_operations=["get_csv_data"]
)

# Mount the MCP server directly to your app
mcp.mount()

# Dependency to verify Bearer Token
def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials.credentials

@app.get("/", dependencies=[Depends(verify_token)])
async def root():
    logger.info('Request to index page')
    return {"message": "Hello World!", "description": app.description}

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
        layout=Layout.MODERN,
        theme=Theme.KEPLER
    )

# result = tadata_sdk.deploy(
#     fastapi_app=app,
#     api_key="api-key",
#     base_url="https://buku.mcp.tadata.com/mcp",
#     name="MCP FastAPI"
# )

# print(f"Deployed FastAPI app: {result.id}")