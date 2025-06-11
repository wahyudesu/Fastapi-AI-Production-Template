from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .routers import chatbot, predict

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(predict.router)  # ml predict
app.include_router(chatbot.router)  # llm chatbot


@app.get("/")
async def root():
    return {"message": "Hello World!"}
