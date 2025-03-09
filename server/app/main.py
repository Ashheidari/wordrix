# app/main.py
import random
from time import time
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

from .models import Word, SQLModel
from .database import engine, get_session
from .schemas import SimilarityRequest, SimilarityResponse, HintRequest, HintResponse

import gensim

app = FastAPI(root_path="/api/v1")




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
    return {
        english: random_word.english,
        foreign_word: random_word.korean
    }


@app.post("/similarity", response_model=SimilarityResponse)
def get_similarity(request: SimilarityRequest):
    guess = request.guess_word
    english_word = request.generated_word

    # Check if both words are in the model's vocabulary
    if guess not in word2vec_model.wv.key_to_index or english_word not in word2vec_model.wv.key_to_index:
        raise HTTPException(
            status_code=404, 
            detail="One or both words not in the model vocabulary"
        )
    
    similarity_score = word2vec_model.wv.similarity(guess, english_word)
    #scale the the similarity score to [-1,1]
    second_similarity_score = round(similarity_score*1.25,3)

    return {"similarity": second_similarity_score}

@app.post("/hint",response_model=HintResponse)
def get_hint(request:HintRequest):
    # scale the score to cosine similarity
    t = time()
    best_score = request.score * 0.8
    english_word = request.generated_word
    similar_words = word2vec_model.wv.most_similar(english_word, topn=2000)
    for i in range(len(similar_words) - 1, -1,-1):
        wrd,scr = similar_words[i]
        if (scr>best_score+0.06):
            print(round((time() - t), 2))
            return {"hint" : wrd, "score" : round(scr*1.25,3) }
    
    raise HTTPException(status_code=404, detail= "no hint available")
