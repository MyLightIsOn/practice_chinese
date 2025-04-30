# load_data.py
from cedict.parser import parse_cedict
from models import DictionaryEntry
from db import get_session, init_db

def insert_entries(entries):
    with get_session() as session:
        for entry in entries:
            dict_entry = DictionaryEntry(
                simplified=entry["simplified"],
                traditional=entry["traditional"],
                pinyin=entry["pinyin"],
                english_definitions="; ".join(entry["english_definitions"])
            )
            session.add(dict_entry)
        session.commit()

if __name__ == "__main__":
    init_db()
    parsed = parse_cedict("data/cedict_ts.u8")
    insert_entries(parsed)
