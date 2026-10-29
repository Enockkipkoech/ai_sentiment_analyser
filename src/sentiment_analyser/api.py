'''
Backend: Sentiment Analysis API
Run: uv run uvicorn sentiment_analyser.api:app --reload --app-dir src
'''

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from google.genai import types, Client

load_dotenv()
client = Client()

app = FastAPI()

# pydantic models
class Review(BaseModel):
    text: str

class AnalysisResult(BaseModel):
    sentiment: str #postive, negative, neutral
    score: float
    theme: str

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Sentiment Analysis API!"}

@app.post("/analyze", response_model=AnalysisResult)
def analyze_review(review: Review):
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=(            
                """
                Analyze the following review and provide a sentiment label (positive, negative, neutral), a score between 0 and 5, and a theme for the review must be ONE lette word  for the main topic. e.g service, delivery, quality, price. \n
                """ 
                f"Here is the review: {review.text}"            
        )
    )
    return response.parsed
