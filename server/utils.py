# seed.py
from app.database import engine
from app.models import Word, SQLModel
from sqlmodel import Session
from sqlalchemy import text
import pandas as pd


# Create tables if they don't exist
SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

# Define words

words_list = pd.read_csv('korean_wordlist.csv')


with Session(engine) as session:
    # Optional: clear existing data
    session.exec(text('DELETE FROM word'))
    for index,row in words_list.iterrows():
        word = Word(english=row["English"], korean=row["Korean"])
        session.add(word)
    session.commit()

print("database filled with words")
