from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llmcore import get_response  # your improved llmcore.py

app = FastAPI(title="Soul AI Chatbot")

# Allow requests from your frontend (adjust origin if deploying)
origins = [
    "http://localhost:5500",  # your frontend local URL
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class UserMessage(BaseModel):
    message: str

# Root endpoint
@app.get("/")
def read_root():
    return {"status": "Soul AI backend is running!"}

# Chat endpoint
@app.post("/chat")
async def chat(user_message: UserMessage):
    user_text = user_message.message
    bot_response = get_response(user_text)
    return {"response": bot_response}
