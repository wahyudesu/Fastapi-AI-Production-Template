"""This will be a simple generative ai using LangChain for text-to-response functionality.
"""

import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from pydantic import BaseModel


load_dotenv()

# Inisialisasi LLM dari Groq
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    api_key=os.getenv("GROQ_API_KEY")
)

# Prompt template
prompt = PromptTemplate(
    input_variables=["question"],
    template="Jawab pertanyaan berikut dengan jelas dan ringkas:\nPertanyaan: {question}"
)

chain = prompt | llm

# Router FastAPI
router = APIRouter(prefix="/chatbot", tags=["chatbot"])

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    try:
        answer = chain.run(question=request.question)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
