# Importing required modules
import re  # Used for regular expressions to parse the file content
from pathlib import Path  # Provides functionalities for dealing with file paths
from typing import List, Dict  # Type hinting for better code clarity


# Function to parse a CEDICT (Chinese-English Dictionary) formatted file
def parse_cedict(file_path: str) -> List[Dict]:
    """
    Parses the CEDICT file and extracts relevant information.

    Args:
        file_path (str): The path to the CEDICT file.

    Returns:
        List[Dict]: A list of dictionary entries, where each entry contains:
            - "simplified": Simplified Chinese characters
            - "traditional": Traditional Chinese characters
            - "pinyin": The pronunciation written in Pinyin
            - "english_definitions": A list of English definitions
    """
    entries = []  # Initialize a list to store parsed dictionary entries

    # Open the file in read mode and ensure the proper encoding is applied
    with open(file_path, 'r', encoding='utf-8') as file:
        # Read the file line by line
        for line in file:
            # Skip lines that are comments (start with '#')
            if line.startswith('#'):
                continue

            # Use a regular expression to match the structure of the dictionary entries
            match = re.match(r'(\S+)\s+(\S+)\s+\[(.+?)]\s+/(.+)/', line)
            if match:
                # Extract traditional, simplified, pinyin, and English definitions from the line
                traditional, simplified, pinyin, english = match.groups()

                # Split the English definitions into a list using '/' as the delimiter
                english_definitions = english.strip().split('/')

                # Append the structured data to the entries list
                entries.append({
                    "simplified": simplified,  # Simplified Chinese
                    "traditional": traditional,  # Traditional Chinese
                    "pinyin": pinyin,  # Pinyin representation
                    "english_definitions": english_definitions  # List of English definitions
                })

    # Return the list of parsed dictionary entries
    return entries
