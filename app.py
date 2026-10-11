
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: list[str]

positive_words = {
    "love", "loved", "lovely", "great", "excellent", "amazing",
    "awesome", "good", "wonderful", "fantastic", "happy", "glad",
    "delightful", "best", "enjoy", "enjoyed", "perfect", "beautiful",
    "brilliant", "like", "liked", "positive", "pleased", "success",
    "successful", "excited", "recommend", "helpful", "impressive",
    "easy", "fun", "superb", "outstanding", "satisfied", "thank",
    "thanks", "thankful", "favorite", "win", "winning"
}

negative_words = {
    "hate", "hated", "terrible", "awful", "bad", "horrible",
    "worst", "sad", "angry", "disappointed", "disappointing",
    "poor", "boring", "annoying", "annoyed", "fail", "failed",
    "failure", "wrong", "problem", "problems", "broken", "useless",
    "slow", "hard", "difficult", "ugly", "unhappy", "upset",
    "frustrated", "frustrating", "negative", "regret", "pain",
    "painful", "sucks", "dislike", "disliked", "damage", "damaged",
    "complaint", "complaints", "bug", "bugs", "inferior", "unsafe"
}

negations = {
    "not", "no", "never", "neither", "hardly", "isn't", "wasn't",
    "don't", "doesn't", "didn't", "can't", "couldn't", "won't"
}

intensifiers = {"very", "really", "extremely", "absolutely", "so"}

def analyze(sentence: str) -> str:
    import re

    words = re.findall(r"[a-z']+", sentence.lower())
    score = 0

    for i, word in enumerate(words):
        if word in positive_words:
            value = 1
        elif word in negative_words:
            value = -1
        else:
            continue

        # Reverse sentiment when preceded by a negation.
        if any(w in negations for w in words[max(0, i - 3):i]):
            value *= -1

        # Give extra weight to common intensifiers.
        if i > 0 and words[i - 1] in intensifiers:
            value *= 1.5

        score += value

    if score > 0:
        return "happy"
    if score < 0:
        return "sad"
    return "neutral"


@app.post("/sentiment")
def batch_sentiment(request: SentimentRequest):
    return {
        "results": [
            {
                "sentence": sentence,
                "sentiment": analyze(sentence)
            }
            for sentence in request.sentences
        ]
    }
