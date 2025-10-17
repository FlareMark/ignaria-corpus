#!/usr/bin/env python3
"""
Generate metadata file for LXX Septuagint.

This script creates complete .meta.yaml file with:
- All 54 books of the LXX (including deuterocanonical books)
- Temporal metadata (composition dates from original Hebrew/Aramaic)
- Author attribution
- Geographic information
"""

import yaml
from pathlib import Path

# LXX book metadata - matches the order in consolidate-lxx.py
LXX_BOOKS = [
    # Pentateuch/Torah - Greek translation of Hebrew originals (-250 BCE)
    {"start_marker": "ΓΕΝΕΣΙΣ", "author": "Moses", "title": "Genesis", "year": -1400, "uncertainty": "high", "location": "Sinai", "genre": "Law"},
    {"start_marker": "ΕΞΟΔΟΣ", "author": "Moses", "title": "Exodus", "year": -1400, "uncertainty": "high", "location": "Sinai", "genre": "Law"},
    {"start_marker": "ΛΕΥΙΤΙΚΟΝ", "author": "Moses", "title": "Leviticus", "year": -1400, "uncertainty": "high", "location": "Sinai", "genre": "Law"},
    {"start_marker": "ΑΡΙΘΜΟΙ", "author": "Moses", "title": "Numbers", "year": -1400, "uncertainty": "high", "location": "Sinai", "genre": "Law"},
    {"start_marker": "ΔΕΥΤΕΡΟΝΟΜΙΟΝ", "author": "Moses", "title": "Deuteronomy", "year": -1400, "uncertainty": "high", "location": "Moab", "genre": "Law"},

    # Historical Books
    {"start_marker": "ΙΗΣΟΥΣ ΝΑΥΗ", "author": "Joshua", "title": "Joshua", "year": -1350, "uncertainty": "high", "location": "Canaan", "genre": "History"},
    {"start_marker": "ΚΡΙΤΑΙ", "author": "Samuel", "title": "Judges", "year": -1050, "uncertainty": "high", "location": "Israel", "genre": "History"},
    {"start_marker": "ΡΟΥΘ", "author": "Samuel", "title": "Ruth", "year": -1050, "uncertainty": "high", "location": "Israel", "genre": "History"},
    {"start_marker": "ΒΑΣΙΛΕΙΩΝ Α", "author": "Samuel", "title": "1 Samuel (1 Kingdoms)", "year": -1000, "uncertainty": "high", "location": "Israel", "genre": "History"},
    {"start_marker": "ΒΑΣΙΛΕΙΩΝ Β", "author": "Samuel", "title": "2 Samuel (2 Kingdoms)", "year": -950, "uncertainty": "high", "location": "Israel", "genre": "History"},
    {"start_marker": "ΒΑΣΙΛΕΙΩΝ Γ", "author": "Jeremiah", "title": "1 Kings (3 Kingdoms)", "year": -550, "uncertainty": "high", "location": "Jerusalem", "genre": "History"},
    {"start_marker": "ΒΑΣΙΛΕΙΩΝ Δ", "author": "Jeremiah", "title": "2 Kings (4 Kingdoms)", "year": -550, "uncertainty": "high", "location": "Jerusalem", "genre": "History"},
    {"start_marker": "ΠΑΡΑΛΕΙΠΟΜΕΝΩΝ Α", "author": "Ezra", "title": "1 Chronicles", "year": -450, "uncertainty": "medium", "location": "Jerusalem", "genre": "History"},
    {"start_marker": "ΠΑΡΑΛΕΙΠΟΜΕΝΩΝ Β", "author": "Ezra", "title": "2 Chronicles", "year": -450, "uncertainty": "medium", "location": "Jerusalem", "genre": "History"},
    {"start_marker": "ΕΣΔΡΑΣ Β", "author": "Ezra", "title": "Ezra", "year": -450, "uncertainty": "medium", "location": "Jerusalem", "genre": "History"},
    {"start_marker": "ΝΕΕΜΙΑΣ", "author": "Nehemiah", "title": "Nehemiah", "year": -430, "uncertainty": "medium", "location": "Jerusalem", "genre": "History"},
    {"start_marker": "ΕΣΔΡΑΣ Α", "author": "Unknown", "title": "1 Esdras", "year": -150, "uncertainty": "high", "location": "Alexandria", "genre": "History", "notes": "Greek composition, deuterocanonical"},
    {"start_marker": "ΤΩΒΙΤ", "author": "Unknown", "title": "Tobit", "year": -200, "uncertainty": "medium", "location": "Eastern Mediterranean", "genre": "History", "notes": "Deuterocanonical"},
    {"start_marker": "ΙΟΥΔΙΘ", "author": "Unknown", "title": "Judith", "year": -150, "uncertainty": "medium", "location": "Palestine", "genre": "History", "notes": "Deuterocanonical"},
    {"start_marker": "ΕΣΘΗΡ", "author": "Mordecai", "title": "Esther", "year": -450, "uncertainty": "medium", "location": "Persia", "genre": "History", "notes": "LXX includes additions"},

    # Wisdom Literature
    {"start_marker": "ΙΩΒ", "author": "Unknown", "title": "Job", "year": -1500, "uncertainty": "high", "location": "Unknown", "genre": "Wisdom"},
    {"start_marker": "ΨΑΛΜΟΙ", "author": "David & Others", "title": "Psalms", "year": -1000, "uncertainty": "high", "location": "Jerusalem", "genre": "Wisdom"},
    {"start_marker": "ΨΑΛΜΟΙ ΣΟΛΟΜΩΝΤΟΣ", "author": "Unknown", "title": "Psalms of Solomon", "year": -50, "uncertainty": "medium", "location": "Jerusalem", "genre": "Wisdom", "notes": "Deuterocanonical, Pharisaic composition"},
    {"start_marker": "ΠΑΡΟΙΜΙΑΙ", "author": "Solomon", "title": "Proverbs", "year": -950, "uncertainty": "medium", "location": "Jerusalem", "genre": "Wisdom"},
    {"start_marker": "ΕΚΚΛΗΣΙΑΣΤΗΣ", "author": "Solomon", "title": "Ecclesiastes", "year": -935, "uncertainty": "medium", "location": "Jerusalem", "genre": "Wisdom"},
    {"start_marker": "ΑΣΜΑ ΑΣΜΑΤΩΝ", "author": "Solomon", "title": "Song of Solomon", "year": -950, "uncertainty": "medium", "location": "Jerusalem", "genre": "Wisdom"},
    {"start_marker": "ΣΟΦΙΑ ΣΟΛΟΜΩΝΤΟΣ", "author": "Unknown", "title": "Wisdom of Solomon", "year": -50, "uncertainty": "medium", "location": "Alexandria", "genre": "Wisdom", "notes": "Deuterocanonical, Greek composition"},
    {"start_marker": "ΣΟΦΙΑ ΣΕΙΡΑΧ", "author": "Jesus ben Sirach", "title": "Wisdom of Sirach", "year": -180, "uncertainty": "low", "location": "Jerusalem", "genre": "Wisdom", "notes": "Deuterocanonical, also known as Ecclesiasticus"},

    # Major Prophets
    {"start_marker": "ΗΣΑΙΑΣ", "author": "Isaiah", "title": "Isaiah", "year": -700, "uncertainty": "medium", "location": "Jerusalem", "genre": "Prophecy"},
    {"start_marker": "ΙΕΡΕΜΙΑΣ", "author": "Jeremiah", "title": "Jeremiah", "year": -600, "uncertainty": "low", "location": "Jerusalem", "genre": "Prophecy"},
    {"start_marker": "ΘΡΗΝΟΙ", "author": "Jeremiah", "title": "Lamentations", "year": -586, "uncertainty": "low", "location": "Jerusalem", "genre": "Prophecy"},
    {"start_marker": "ΕΠΙΣΤΟΛΗ ΙΕΡΕΜΙΟΥ", "author": "Unknown", "title": "Epistle of Jeremiah", "year": -300, "uncertainty": "high", "location": "Palestine", "genre": "Prophecy", "notes": "Deuterocanonical"},
    {"start_marker": "ΒΑΡΟΥΧ", "author": "Baruch", "title": "Baruch", "year": -580, "uncertainty": "high", "location": "Babylon", "genre": "Prophecy", "notes": "Deuterocanonical"},
    {"start_marker": "ΣΟΥΣΑΝΝΑ", "author": "Unknown", "title": "Susanna", "year": -100, "uncertainty": "high", "location": "Unknown", "genre": "Prophecy", "notes": "Addition to Daniel, deuterocanonical"},
    {"start_marker": "ΙΕΖΕΚΙΗΛ", "author": "Ezekiel", "title": "Ezekiel", "year": -580, "uncertainty": "low", "location": "Babylon", "genre": "Prophecy"},
    {"start_marker": "ΔΑΝΙΗΛ", "author": "Daniel", "title": "Daniel", "year": -530, "uncertainty": "medium", "location": "Babylon", "genre": "Prophecy"},
    {"start_marker": "ΒΗΛ ΚΑΙ ΔΡΑΚΩΝ", "author": "Unknown", "title": "Bel and the Dragon", "year": -100, "uncertainty": "high", "location": "Unknown", "genre": "Prophecy", "notes": "Addition to Daniel, deuterocanonical"},

    # Minor Prophets (The Twelve)
    {"start_marker": "ΩΣΗΕ", "author": "Hosea", "title": "Hosea", "year": -750, "uncertainty": "medium", "location": "Northern Israel", "genre": "Prophecy"},
    {"start_marker": "ΙΩΗΛ", "author": "Joel", "title": "Joel", "year": -835, "uncertainty": "high", "location": "Judah", "genre": "Prophecy"},
    {"start_marker": "ΑΜΩΣ", "author": "Amos", "title": "Amos", "year": -760, "uncertainty": "medium", "location": "Tekoa", "genre": "Prophecy"},
    {"start_marker": "ΑΒΔΙΟΥ", "author": "Obadiah", "title": "Obadiah", "year": -585, "uncertainty": "high", "location": "Judah", "genre": "Prophecy"},
    {"start_marker": "ΙΩΝΑΣ", "author": "Jonah", "title": "Jonah", "year": -780, "uncertainty": "medium", "location": "Northern Israel", "genre": "Prophecy"},
    {"start_marker": "ΜΙΧΑΙΑΣ", "author": "Micah", "title": "Micah", "year": -735, "uncertainty": "medium", "location": "Moresheth", "genre": "Prophecy"},
    {"start_marker": "ΝΑΟΥΜ", "author": "Nahum", "title": "Nahum", "year": -650, "uncertainty": "medium", "location": "Judah", "genre": "Prophecy"},
    {"start_marker": "ΑΜΒΑΚΟΥΜ", "author": "Habakkuk", "title": "Habakkuk", "year": -607, "uncertainty": "medium", "location": "Judah", "genre": "Prophecy"},
    {"start_marker": "ΣΟΦΟΝΙΑΣ", "author": "Zephaniah", "title": "Zephaniah", "year": -630, "uncertainty": "medium", "location": "Judah", "genre": "Prophecy"},
    {"start_marker": "ΑΓΓΑΙΟΣ", "author": "Haggai", "title": "Haggai", "year": -520, "uncertainty": "low", "location": "Jerusalem", "genre": "Prophecy"},
    {"start_marker": "ΖΑΧΑΡΙΑΣ", "author": "Zechariah", "title": "Zechariah", "year": -520, "uncertainty": "low", "location": "Jerusalem", "genre": "Prophecy"},
    {"start_marker": "ΜΑΛΑΧΙΑΣ", "author": "Malachi", "title": "Malachi", "year": -430, "uncertainty": "medium", "location": "Jerusalem", "genre": "Prophecy"},

    # Maccabees (Historical/Deuterocanonical)
    {"start_marker": "ΜΑΚΚΑΒΑΙΩΝ Α", "author": "Unknown", "title": "1 Maccabees", "year": -100, "uncertainty": "medium", "location": "Palestine", "genre": "History", "notes": "Deuterocanonical, Hasmonean history"},
    {"start_marker": "ΜΑΚΚΑΒΑΙΩΝ Β", "author": "Jason of Cyrene", "title": "2 Maccabees", "year": -124, "uncertainty": "medium", "location": "Alexandria", "genre": "History", "notes": "Deuterocanonical"},
    {"start_marker": "ΜΑΚΚΑΒΑΙΩΝ Γ", "author": "Unknown", "title": "3 Maccabees", "year": -100, "uncertainty": "high", "location": "Alexandria", "genre": "History", "notes": "Deuterocanonical, about Egyptian Jews"},
    {"start_marker": "ΜΑΚΚΑΒΑΙΩΝ Δ", "author": "Unknown", "title": "4 Maccabees", "year": 100, "uncertainty": "medium", "location": "Alexandria", "genre": "Wisdom", "notes": "Deuterocanonical, philosophical treatise"},

    # Odes (Liturgical)
    {"start_marker": "ΩΔΑΙ", "author": "Various", "title": "Odes", "year": -200, "uncertainty": "high", "location": "Alexandria", "genre": "Liturgy", "notes": "Collection of liturgical hymns"},
]

def main():
    metadata = {
        "text_info": {
            "id": "bible-lxx",
            "title": "The Septuagint (LXX) - Greek Old Testament",
            "authors": ["Various Biblical Authors"],
            "series": "Holy Bible",
            "volume": "LXX Rahlfs 1935",
            "is_anthology": True,
            "sections": []
        },
        "publication": {
            "original_language": "Koine Greek",
            "original_date": "c. 250-50 BCE (translation); original texts c. 1500-100 BCE",
            "period": "Hellenistic Period",
            "genre": "Sacred Scripture",
            "translation_date": "c. 250-50 BCE",
            "edition": "Rahlfs 1935",
            "notes": "Greek translation of Hebrew Bible produced in Alexandria"
        },
        "content": {
            "description": "The Septuagint, the ancient Greek translation of the Hebrew Bible and deuterocanonical books",
            "format": "Complete Greek Old Testament with 54 books",
            "themes": [
                "Torah and Law",
                "History of Israel",
                "Wisdom Literature",
                "Prophetic Revelation",
                "Deuterocanonical Books"
            ]
        },
        "sources": {
            "edition": "LXX Rahlfs 1935",
            "source": "Open Scriptures LXX Project",
            "source_url": "https://github.com/sleeptillseven/LXX-Rahlfs-1935",
            "license": "Public domain",
            "technical_notes": "Rahlfs critical edition with morphological tagging"
        },
        "technical": {
            "encoding": "UTF-8",
            "format": "Plain text",
            "line_endings": "Unix (LF)",
            "created": "2025-10-17",
            "last_modified": "2025-10-17"
        },
        "cataloging": {
            "lxx_id": "rahlfs-1935",
            "series_info": "The Septuagint (LXX)",
            "historical_significance": "The earliest extant Greek translation of the Hebrew Bible, widely used by early Christians"
        },
        "notes": [
            "The Septuagint includes deuterocanonical books not found in the Hebrew Masoretic Text",
            "Translation dates vary: Pentateuch c. 250 BCE, other books through c. 50 BCE",
            "Rahlfs 1935 is a critical edition based on Codex Vaticanus, Sinaiticus, and Alexandrinus",
            "This edition includes morphological analysis for scholarly study",
            "Public domain - freely available for study and research"
        ]
    }

    # Add all book sections
    for book in LXX_BOOKS:
        section = {
            "author": book["author"],
            "title": book["title"],
            "start_marker": book["start_marker"],
            "composition_year": book["year"],
            "composition_uncertainty": book["uncertainty"],
            "author_region": "Eastern" if book["location"] not in ["Rome", "Western"] else "Western",
            "author_location": book["location"],
            "genre": book["genre"]
        }

        if "notes" in book:
            section["notes"] = book["notes"]

        metadata["text_info"]["sections"].append(section)

    # Write to file
    output_path = Path("sources/BIBLE-LXX.meta.yaml")
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(metadata, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    print(f"Generated LXX metadata: {output_path}")
    print(f"Total books: {len(LXX_BOOKS)}")
    print(f"  - Protocanonical (Hebrew Bible): 39 books")
    print(f"  - Deuterocanonical: 15 books")
    print(f"  - Total: 54 books")

if __name__ == "__main__":
    main()
