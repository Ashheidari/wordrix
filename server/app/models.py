# app/models.py
from typing import Optional
from sqlmodel import SQLModel, Field

class Word(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    english: str
    spanish: str