from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# ✅ FIXED IMPORT


app = FastAPI(title="AI Education Tutor - SDG 4")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    level: str
    subject: str
    question: str
def get_ai_answer(level: str, subject: str, question: str):
    return f"Mock answer for {subject} ({level}): {question}"
@app.get("/")
def root():
    return {"status": "Backend running successfully"}

@app.post("/ask")
def ask_ai(data: QuestionRequest):
    answer = get_ai_answer(
        level=data.level,
        subject=data.subject,
        question=data.question
    )
    return {"answer": answer}
