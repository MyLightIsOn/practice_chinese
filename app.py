# app.py
from typing import List

from fastapi import FastAPI, Query
from sqlmodel import select
from db import get_session, init_db
from models import DictionaryEntry

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

@app.get("/lookup/")
def lookup_word(simplified: str = Query(...)):
    with get_session() as session:
        statement = select(DictionaryEntry).where(DictionaryEntry.simplified == simplified)
        result = session.exec(statement).first()
        return result or {"error": "Word not found"}

@app.get("/search/")
def search_words(
    q: str = Query(..., min_length=1),
    limit: int = 10
) -> List[DictionaryEntry]:
    with get_session() as session:
        statement = select(DictionaryEntry).where((DictionaryEntry.simplified.contains(q)) | (DictionaryEntry.traditional.contains(q)) | (DictionaryEntry.pinyin.contains(q))).limit(limit)
        results = session.exec(statement).all()
        return results