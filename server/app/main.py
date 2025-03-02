# app/main.py
import random
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from .models import Word, SQLModel
from .database import engine, get_session
from .schemas import SimilarityRequest, SimilarityResponse

import gensim

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


word2vec_model  = gensim.models.Word2Vec.load("./word2vec.model")

# Create database tables if they do not exist
SQLModel.metadata.create_all(engine)

@app.get("/random_word", response_model=Word)
def get_random_word(session: Session = Depends(get_session)):
    statement = select(Word)
    words = session.exec(statement).all()
    if not words:
        raise HTTPException(status_code=404, detail="No words found")
    random_word = random.choice(words)
    return random_word


@app.post("/similarity", response_model=SimilarityResponse)
def get_similarity(request: SimilarityRequest):
    guess = request.guess_word
    generated = request.generated_word

    # Check if both words are in the model's vocabulary
    if guess not in word2vec_model.wv.key_to_index or generated not in word2vec_model.wv.key_to_index:
        raise HTTPException(
            status_code=404, 
            detail="One or both words not in the model vocabulary"
        )
    
    similarity_score = word2vec_model.wv.similarity(guess, generated)
    return {"similarity": similarity_score}