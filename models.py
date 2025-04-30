# models.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class DictionaryEntry(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    simplified: str
    traditional: str
    pinyin: str
    english_definitions: str  # store as ";" joined string for now
    hsk_level: Optional[int] = None
    frequency_rank: Optional[int] = None
    word_stats: List["UserWordStat"] = Relationship(back_populates="word")

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    word_stats: List["UserWordStat"] = Relationship(back_populates="user")


class UserWordStat(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    dictionary_entry_id: int = Field(foreign_key="dictionaryentry.id")

    times_appeared: int = 0
    times_correct: int = 0
    times_incorrect: int = 0
    last_seen: Optional[datetime] = None

    user: Optional[User] = Relationship(back_populates="word_stats")
    word: Optional["DictionaryEntry"] = Relationship()