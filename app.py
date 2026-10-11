from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = FastAPI()
analyzer = SentimentIntensityAnalyzer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: list[str]

def analyze(sentence: str) -> str:
    score = analyzer.polarity_scores(sentence)["compound"]

    if score >= 0.05:
        return "happy"
    elif score <= -0.05:
        return "sad"
    return "neutral"

@app.get("/")
def home():
    return {"message": "Sentiment API is running"}

@app.post("/sentiment")
def sentiment(request: SentimentRequest):
    return {
        "results": [
            {"sentence": sentence, "sentiment": analyze(sentence)}
            for sentence in request.sentences
        ]
    }
