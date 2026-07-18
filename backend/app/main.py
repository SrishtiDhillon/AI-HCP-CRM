from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.interaction import router as interaction_router
from app.routes.chat import router as chat_router

from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-First CRM HCP Module",
    description="Healthcare Professional Interaction Management System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interaction_router)
app.include_router(chat_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI-First CRM HCP Module"
    }


@app.get("/health")
def health():
    return {
        "status": "Running"
    }