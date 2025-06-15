from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .logging_config import get_logger  # logging configuration
from .dependencies import get_query_token  # security dependency
from .routers import chatbot, predict  # import routers

# Create security scheme
security = HTTPBearer()

API_TOKEN = "token"  # Replace with your actual token

logger = get_logger("app.main")

app = FastAPI(
    title="FastAPI Project",
    description="Simple FastAPI boilerplate for your AI/ML projects.",
    version="1.0.0",
    dependencies=[Depends(get_query_token)]
)

app.include_router(predict.router)  # ml predict
app.include_router(chatbot.router)  # llm chatbot


# Dependency to verify Bearer Token
def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != API_TOKEN:
        logger.warning("Invalid token provided")
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials.credentials


@app.get("/", dependencies=[Depends(verify_token)])
async def root():
    return {"message": "Hello World!", "description": app.description}