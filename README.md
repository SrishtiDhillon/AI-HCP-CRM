# AI-First CRM HCP Module

## Project Overview

This project is an AI-first Customer Relationship Management module focused on Healthcare Professional interaction management.

It is designed for life sciences field representatives to manage HCP data, log interactions, retrieve previous engagement history, and use an AI assistant to perform CRM actions through natural language.

The system supports both:

1. Structured interaction logging through a React form.
2. Conversational interaction logging through an AI chat interface.

---

## Tech Stack

### Frontend

- React
- Redux Toolkit
- React Redux
- Axios
- Vite
- Google Inter Font

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic

### AI Layer

- LangGraph
- LangChain
- Groq LLM
- Model used: `llama-3.3-70b-versatile`

---

## Key Features

- HCP search
- HCP interaction logging
- Interaction history retrieval
- Interaction editing
- Next-best-action suggestion
- Conversational AI assistant
- Structured interaction logging screen
- FastAPI Swagger documentation
- React frontend connected with FastAPI backend
- Redux-based chat state management

---

## Assignment Requirement Coverage

The assignment required an AI-first CRM HCP module with a Log Interaction Screen.

This project covers the requirement through:

- A React frontend with Redux state management
- A structured form for logging HCP interactions
- A conversational AI chat interface
- A FastAPI backend
- PostgreSQL database integration
- A LangGraph AI agent
- Groq LLM integration
- More than five CRM tools for sales-related activities

---

## LangGraph Agent Role

The LangGraph agent acts as the reasoning layer of the CRM system.

It receives a natural language query from the user, understands the intent, selects the appropriate CRM tool, executes the tool, and returns a concise CRM-focused response.

Example flow:

```text
User Message
    ↓
React Frontend
    ↓
FastAPI /chat Endpoint
    ↓
LangGraph Agent
    ↓
Groq LLM
    ↓
CRM Tool Execution
    ↓
Final AI Response