# app.py
from typing import List

from fastapi import FastAPI, Query
from sqlmodel import select
from db import get_session, init_db
from models import DictionaryEntry

# Import FastAPI framework
app = FastAPI()


# Event triggered when the application launches (startup phase)
@app.on_event("startup")
def startup():
    # Initialize the database
    init_db()


# Endpoint to look up a word by its simplified Chinese form
@app.get("/lookup/")
def lookup_word(simplified: str = Query(...)):
    """
    Accepts a 'simplified' word as a query parameter and looks it up in the database.
    If the word is found, it returns the corresponding DictionaryEntry object.
    If not found, it returns a default JSON response with an error message.
    """
    with get_session() as session:
        # Query to fetch the DictionaryEntry that matches the given simplified word
        statement = select(DictionaryEntry).where(DictionaryEntry.simplified == simplified)
        # Execute the query and fetch the first result
        result = session.exec(statement).first()
        # Return the result or an error message if no match is found
        return result or {"error": "Word not found"}


# Endpoint to search for words matching a query across multiple fields
@app.get("/search/")
def search_words(
        q: str = Query(..., min_length=1),  # Search term that must be at least 1 character long
        limit: int = 10  # Maximum number of results to return
) -> List[DictionaryEntry]:
    """
    Accepts a search query 'q' and a result limit as query parameters.
    Searches for words in the database that match the query in any of the following fields:
    - Simplified
    - Traditional
    - Pinyin
    Returns a list of matching DictionaryEntry objects up to the specified limit.
    """
    with get_session() as session:
        # Query to search the DictionaryEntry table for matches in specified fields
        statement = select(DictionaryEntry).where(
            (DictionaryEntry.simplified.contains(q)) |  # Match in 'simplified' field
            (DictionaryEntry.traditional.contains(q)) |  # Match in 'traditional' field
            (DictionaryEntry.pinyin.contains(q))  # Match in 'pinyin' field
        ).limit(limit)  # Limit the number of results
        # Execute the query and fetch all matching results
        results = session.exec(statement).all()
        # Return the list of results
        return results
