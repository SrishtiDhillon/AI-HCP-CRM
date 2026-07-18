from fastapi import APIRouter
from pydantic import BaseModel

from app.agent.graph import run_agent


router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = run_agent(request.message)

    return {
        "response": answer
    }
