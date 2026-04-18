# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from orchestrator import run_orchestrator

app = FastAPI(title="Campus Co-Pilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    agents_called: list
    raw_results: dict

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    result = await run_orchestrator(req.message)
    return ChatResponse(
        response=result["response"],
        agents_called=result["agents_called"],
        raw_results=result["raw_results"]
    )
