import logging
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter(prefix='/chat', tags=['AI Chat'])
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    message: str = Field(min_length=1, max_length=10000)


class ChatResponse(BaseModel):
    response: str


def run_agent(message: str) -> str:
    # Import only when chat is used: CRUD, health and tests need no AI credentials.
    from app.agent.graph import run_agent as invoke_agent
    return invoke_agent(message)


@router.post('/', response_model=ChatResponse)
def chat(request: ChatRequest):
    if not os.getenv('GROQ_API_KEY', '').strip():
        raise HTTPException(status_code=503, detail='AI chat is not configured. Structured logging is still available.')
    try:
        return {'response': run_agent(request.message)}
    except Exception:
        logger.exception('AI chat request failed')
        raise HTTPException(status_code=503, detail='AI service is unavailable. Please try again later.') from None
