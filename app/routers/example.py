import os
import getpass
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from typing_extensions import TypedDict

from ..dependencies import get_query_token

# --- Konfigurasi API Key Groq (bisa lewat environment variable) ---
load_dotenv()


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


# _set_env("GROQ_API_KEY")  # uncomment jika perlu input manual

# Inisialisasi LLM dari Groq dengan error handling
try:
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("⚠️ GROQ_API_KEY not found in environment variables")
        llm = None
    else:
        llm = ChatGroq(model="gemma2-9b-it", api_key=groq_api_key)
        print("✅ ChatGroq initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize ChatGroq: {e}")
    llm = None


# --- Tipe Data State ---
class AssignmentMeta(TypedDict):
    title: str
    description: str


class State(TypedDict):
    assignment_meta: AssignmentMeta
    assignment_content: str
    persona: str
    summary: str
    relevance_analysis: str
    feedback_analysis: str
    personalized_feedback: str
    combined_output: str


# --- Node Agent Functions ---
def input_meta(state: State) -> dict:
    return {"assignment_meta": state["assignment_meta"]}


def input_content(state: State) -> dict:
    return {"assignment_content": state["assignment_content"]}


def summarizer_agent(state: State) -> dict:
    if llm is None:
        raise HTTPException(status_code=500, detail="LLM not properly initialized")

    content = state["assignment_content"]
    msg = llm.invoke(f"Summarize the following assignment content:\n\n{content}")
    return {"summary": msg.content}


def relevance_agent(state: State) -> dict:
    if llm is None:
        raise HTTPException(status_code=500, detail="LLM not properly initialized")

    title = state["assignment_meta"]["title"]
    desc = state["assignment_meta"]["description"]
    prompt = f"""Analyze the relevance between the following title and description of an assignment:

Title: {title}
Description: {desc}

Does the title appropriately reflect the content described? Provide analysis."""
    msg = llm.invoke(prompt)
    return {"relevance_analysis": msg.content}


def aggregator(state: State) -> dict:
    if llm is None:
        raise HTTPException(status_code=500, detail="LLM not properly initialized")

    summary = state["summary"]
    relevance = state["relevance_analysis"]
    persona = state["persona"]

    feedback_prompt = f"""You are an academic evaluator. Provide constructive feedback based on the following:

SUMMARY:
{summary}

RELEVANCE ANALYSIS:
{relevance}"""
    feedback = llm.invoke(feedback_prompt).content

    personalization_prompt = f"""Personalize the following academic feedback based on the following style or instruction:

INSTRUCTION:
{persona}

FEEDBACK:
{feedback}"""
    personalized = llm.invoke(personalization_prompt).content

    combined = f"🎓 Final Personalized Feedback:\n\n{personalized}"
    return {"feedback_analysis": feedback, "personalized_feedback": personalized, "combined_output": combined}


# --- Bangun Workflow ---
builder = StateGraph(State)
builder.add_node("input_meta", input_meta)
builder.add_node("input_content", input_content)
builder.add_node("relevance_agent", relevance_agent)
builder.add_node("summarizer_agent", summarizer_agent)
builder.add_node("aggregator", aggregator)

builder.add_edge(START, "input_meta")
builder.add_edge(START, "input_content")
builder.add_edge("input_meta", "relevance_agent")
builder.add_edge("input_content", "summarizer_agent")
builder.add_edge("relevance_agent", "aggregator")
builder.add_edge("summarizer_agent", "aggregator")
builder.add_edge("aggregator", END)

workflow = builder.compile()

# --- FastAPI Router Setup ---
router = APIRouter(prefix="/feedback", tags=["feedback"], dependencies=[Depends(get_query_token)])


class AssignmentRequest(BaseModel):
    title: str
    description: str
    content: str
    persona: str


class AssignmentResponse(BaseModel):
    summary: str
    relevance_analysis: str
    feedback_analysis: str
    personalized_feedback: str
    combined_output: str


@router.post("/", response_model=AssignmentResponse)
def generate_feedback(payload: AssignmentRequest):
    """
    Generate AI-powered feedback for academic assignments.

    This endpoint analyzes assignment content and provides:
    - Content summary
    - Relevance analysis between title and description
    - Academic feedback
    - Personalized feedback based on specified persona
    """
    if llm is None:
        raise HTTPException(status_code=500, detail="AI service not available")

    initial_state: State = {
        "assignment_meta": {
            "title": payload.title,
            "description": payload.description,
        },
        "assignment_content": payload.content,
        "persona": payload.persona,
        "summary": "",
        "relevance_analysis": "",
        "feedback_analysis": "",
        "personalized_feedback": "",
        "combined_output": "",
    }

    try:
        result = workflow.invoke(initial_state)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate feedback: {str(e)}")


@router.get("/debug")
async def debug_status():
    """Debug endpoint to check API key and services"""
    groq_key = os.getenv("GROQ_API_KEY")

    return {
        "groq": {
            "api_key_exists": bool(groq_key),
            "key_length": len(groq_key) if groq_key else 0,
            "format_valid": groq_key.startswith("gsk_") if groq_key else False,
            "llm_initialized": llm is not None,
        },
        "environment": os.getenv("ENVIRONMENT"),
        "debug_mode": os.getenv("DEBUG"),
    }
