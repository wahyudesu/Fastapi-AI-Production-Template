"""Chatbot router: Simple generative AI using LangChain for text-to-response."""

from fastapi import APIRouter, HTTPException
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from pydantic import BaseModel

from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="gemma2-9b-it",
    api_key = os.getenv("GROQ_API_KEY")
)

prompt = PromptTemplate(
    input_variables=["question"],
    template="Jawab pertanyaan berikut dengan jelas dan ringkas:\nPertanyaan: {question}"
)

chain = prompt | llm

router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"],
    responses={404: {"description": "Not found"}}
)

class ChatRequest(BaseModel):
    question: str
        
class ChatResponse(BaseModel):
    answer: str

@router.post("/ask", response_model=ChatResponse, summary="Ask chatbot a question")
async def ask_question(request: ChatRequest):
    """
    Ask a question to the generative AI chatbot.
    """
    try:
        result = chain.invoke({"question": request.question})
        # Extract the string content from the AIMessage object
        answer = getattr(result, "content", str(result))
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))