"""ini bakal jadi ai agent sederhana yang menggunakan langchain untuk text to response
"""

import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from langchain.chains import LLMChain
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

# Chain sederhana
chain = LLMChain(llm=llm, prompt=prompt)

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
