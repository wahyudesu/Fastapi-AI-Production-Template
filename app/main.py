import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer  # security scheme
from .routers import agent, chatbot, predict  # import routers
from .logger import logger
from .middleware import Middleware

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

app.add_middleware(Middleware) 

# Dependency to verify Bearer Token
def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials.credentials

@app.get("/", dependencies=[Depends(verify_token)])
async def root():
    logger.info('Request to index page')
    return {"message": "Hello World!", "description": app.description}
