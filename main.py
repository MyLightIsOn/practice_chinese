from cedict.parser import parse_cedict

if __name__ == "__main__":
    entries = parse_cedict("data/cedict_ts.u8")
    print(f"Parsed {len(entries)} entries.\n")

    for entry in entries[:5]:  # Show first 5 entries
        print(entry)
