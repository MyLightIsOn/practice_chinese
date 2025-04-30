# models.py
from sqlmodel import SQLModel, Field
from typing import Optional

class DictionaryEntry(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    simplified: str
    traditional: str
    pinyin: str
    english_definitions: str  # store as ";" joined string for now
    hsk_level: Optional[int] = None
    frequency_rank: Optional[int] = None
