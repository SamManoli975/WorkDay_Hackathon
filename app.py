from typing import Union

from fastapi import FastAPI

from mainV3 import run_agent

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel  # Import for request validation


app = FastAPI()

origins = [
    "http://localhost:8080",  # React frontend
    "http://your-frontend-domain.com"  # If deploying to production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class QueryRequest(BaseModel):
    query: str

@app.post("/news-agent")
def news_agent(request: QueryRequest):
    return run_agent(request.query)