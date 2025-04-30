# load_data.py
from cedict.parser import parse_cedict
from models import DictionaryEntry
from db import get_session, init_db

# Function to insert dictionary entries into the database
def insert_entries(entries):
    # Create a new session for database operations using the context manager
    with get_session() as session:
        # Iterate over each dictionary entry in the provided list
        for entry in entries:
            # Create a new DictionaryEntry object with the provided data
            dict_entry = DictionaryEntry(
                simplified=entry["simplified"],  # Simplified Chinese characters
                traditional=entry["traditional"],  # Traditional Chinese characters
                pinyin=entry["pinyin"],  # Pinyin representation
                english_definitions="; ".join(entry["english_definitions"])  # English definitions joined by "; "
            )
            # Add the new dictionary entry to the session
            session.add(dict_entry)
        # Commit all changes to the database
        session.commit()


# Main block to initialize the database and insert entries
if __name__ == "__main__":
    # Initialize the database (creates necessary schema/tables if not already created)
    init_db()
    # Parse the input CEDICT (Chinese-English dictionary) file to extract entries
    parsed = parse_cedict("data/cedict_ts.u8")
    # Insert the parsed entries into the database
    insert_entries(parsed)
