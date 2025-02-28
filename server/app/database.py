from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")


engine = create_engine(DATABASE_URL, echo=True)  # echo=True helps with debugging

def get_session():
    with Session(engine) as session:
        yield session