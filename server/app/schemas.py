# app/schemas.py
from pydantic import BaseModel

# Existing models...
# class WordBase(...)

# New models for similarity endpoint
class SimilarityRequest(BaseModel):
    guess_word: str
    generated_word: str

class SimilarityResponse(BaseModel):
    similarity: float


#new models for hint endpoint
class HintRequest(BaseModel):
    score:float
    generated_word:str


class HintResponse(BaseModel):
    score:float
    hint:str