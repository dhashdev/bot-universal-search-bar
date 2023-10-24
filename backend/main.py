from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.llm import AnswerPredictor

app = FastAPI()

# Set up CORS
origins = [
    "http://localhost:3000",  # React frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    message: str


@app.post("/get-response/")
def get_response(question: str, history: List[Tuple[str, str]] = []):
    # response = "Received: " + data.message
    # return {"response": response}
    llm_chain = AnswerPredictor()
    response, sources = llm_chain.predict(question, history)

    history.append((question, response))
    result = {"answer": response, "sources": sources, "history": history}

    return result
