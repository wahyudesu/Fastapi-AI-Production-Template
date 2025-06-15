from typing import Annotated
import os
from dotenv import load_dotenv

from fastapi import Header, HTTPException

load_dotenv()

# X_TOKEN_SECRET = os.getenv("X_TOKEN_SECRET")
QUERY_TOKEN_SECRET = os.getenv("QUERY_TOKEN_SECRET")

# Admin token
# async def get_token_header(x_token: Annotated[str, Header()]):
#     if x_token != X_TOKEN_SECRET:
#         raise HTTPException(status_code=400, detail="X-Token header invalid")

async def get_query_token(token: str):
    if token != QUERY_TOKEN_SECRET:
        raise HTTPException(status_code=400, detail="Use token for security!")
