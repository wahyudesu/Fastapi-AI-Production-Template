"""Agents router: Generate NYT-style articles using LangChain and OpenAI."""

from fastapi import APIRouter
from typing import Annotated

from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode, tools_condition

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
    responses={404: {"description": "Not found"}}
)

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

llm = init_chat_model("llama3-8b-8192", model_provider="groq")

# Modification: tell the LLM which tools it can call
# highlight-next-line
tool = TavilySearch(max_results=2)
tools = [tool]
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

# FastAPI endpoint to get graph PNG
from fastapi.responses import Response

@router.get("/graph", response_class=Response, summary="Get LangGraph structure as PNG")
async def get_graph_png():
    """
    Returns the LangGraph structure as a PNG image.
    """
    try:
        png_bytes = graph.get_graph().draw_mermaid_png()
        return Response(content=png_bytes, media_type="image/png")
    except Exception as e:
        return Response(content=f"Gagal menyimpan gambar: {e}", media_type="text/plain", status_code=500)

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


from fastapi import Request
from pydantic import BaseModel

# Request model for chat endpoint
class ChatRequest(BaseModel):
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "tell me about president jokowi"
            }
        }

@router.post("/ask")
async def chat_endpoint(request: ChatRequest):
    """
    Chat with LangGraph agent. Send a message and get response.
    """
    user_input = request.message
    responses = []
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            responses.append(value["messages"][-1].content)
    return {"responses": responses}