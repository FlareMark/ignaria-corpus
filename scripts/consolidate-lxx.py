#!/usr/bin/env python3
"""
Consolidate LXX Rahlfs 1935 Septuagint from CSV format into single text file.
"""

import csv
import re
from pathlib import Path

# LXX book mapping (from SQLite database)
LXX_BOOKS = [
    (10, "Genesis", "ΓΕΝΕΣΙΣ"),
    (20, "Exodus", "ΕΞΟΔΟΣ"),
    (30, "Leviticus", "ΛΕΥΙΤΙΚΟΝ"),
    (40, "Numbers", "ΑΡΙΘΜΟΙ"),
    (50, "Deuteronomy", "ΔΕΥΤΕΡΟΝΟΜΙΟΝ"),
    (60, "Joshua", "ΙΗΣΟΥΣ ΝΑΥΗ"),
    (70, "Judges", "ΚΡΙΤΑΙ"),
    (80, "Ruth", "ΡΟΥΘ"),
    (90, "1 Samuel (1 Kingdoms)", "ΒΑΣΙΛΕΙΩΝ Α"),
    (100, "2 Samuel (2 Kingdoms)", "ΒΑΣΙΛΕΙΩΝ Β"),
    (110, "1 Kings (3 Kingdoms)", "ΒΑΣΙΛΕΙΩΝ Γ"),
    (120, "2 Kings (4 Kingdoms)", "ΒΑΣΙΛΕΙΩΝ Δ"),
    (130, "1 Chronicles", "ΠΑΡΑΛΕΙΠΟΜΕΝΩΝ Α"),
    (140, "2 Chronicles", "ΠΑΡΑΛΕΙΠΟΜΕΝΩΝ Β"),
    (150, "Ezra", "ΕΣΔΡΑΣ Β"),
    (160, "Nehemiah", "ΝΕΕΜΙΑΣ"),
    (165, "1 Esdras", "ΕΣΔΡΑΣ Α"),
    (170, "Tobit", "ΤΩΒΙΤ"),
    (180, "Judith", "ΙΟΥΔΙΘ"),
    (190, "Esther", "ΕΣΘΗΡ"),
    (220, "Job", "ΙΩΒ"),
    (230, "Psalms", "ΨΑΛΜΟΙ"),
    (232, "Psalms of Solomon", "ΨΑΛΜΟΙ ΣΟΛΟΜΩΝΤΟΣ"),
    (240, "Proverbs", "ΠΑΡΟΙΜΙΑΙ"),
    (250, "Ecclesiastes", "ΕΚΚΛΗΣΙΑΣΤΗΣ"),
    (260, "Song of Solomon", "ΑΣΜΑ ΑΣΜΑΤΩΝ"),
    (270, "Wisdom of Solomon", "ΣΟΦΙΑ ΣΟΛΟΜΩΝΤΟΣ"),
    (280, "Wisdom of Sirach", "ΣΟΦΙΑ ΣΕΙΡΑΧ"),
    (290, "Isaiah", "ΗΣΑΙΑΣ"),
    (300, "Jeremiah", "ΙΕΡΕΜΙΑΣ"),
    (310, "Lamentations", "ΘΡΗΝΟΙ"),
    (315, "Epistle of Jeremiah", "ΕΠΙΣΤΟΛΗ ΙΕΡΕΜΙΟΥ"),
    (320, "Baruch", "ΒΑΡΟΥΧ"),
    (325, "Susanna", "ΣΟΥΣΑΝΝΑ"),
    (330, "Ezekiel", "ΙΕΖΕΚΙΗΛ"),
    (340, "Daniel", "ΔΑΝΙΗΛ"),
    (345, "Bel and the Dragon", "ΒΗΛ ΚΑΙ ΔΡΑΚΩΝ"),
    (350, "Hosea", "ΩΣΗΕ"),
    (360, "Joel", "ΙΩΗΛ"),
    (370, "Amos", "ΑΜΩΣ"),
    (380, "Obadiah", "ΑΒΔΙΟΥ"),
    (390, "Jonah", "ΙΩΝΑΣ"),
    (400, "Micah", "ΜΙΧΑΙΑΣ"),
    (410, "Nahum", "ΝΑΟΥΜ"),
    (420, "Habakkuk", "ΑΜΒΑΚΟΥΜ"),
    (430, "Zephaniah", "ΣΟΦΟΝΙΑΣ"),
    (440, "Haggai", "ΑΓΓΑΙΟΣ"),
    (450, "Zechariah", "ΖΑΧΑΡΙΑΣ"),
    (460, "Malachi", "ΜΑΛΑΧΙΑΣ"),
    (462, "1 Maccabees", "ΜΑΚΚΑΒΑΙΩΝ Α"),
    (464, "2 Maccabees", "ΜΑΚΚΑΒΑΙΩΝ Β"),
    (466, "3 Maccabees", "ΜΑΚΚΑΒΑΙΩΝ Γ"),
    (467, "4 Maccabees", "ΜΑΚΚΑΒΑΙΩΝ Δ"),
    (800, "Odes", "ΩΔΑΙ"),
]

def strip_markup(text):
    """Remove morphological markup from Greek text, keeping only the words."""
    # Pattern: word<S>number</S><m>code</m><S>number</S><S>number</S>
    # We want to keep only the word part before the first <S>
    words = []
    parts = text.split()
    for part in parts:
        # Extract text before first <S> tag
        word = part.split('<S>')[0]
        if word:
            words.append(word)
    return ' '.join(words)

def main():
    csv_path = Path("sources/LXX-Rahlfs-1935/11_end-users_files/MyBible/Bibles/LXX_final_main.csv")
    output_path = Path("sources/BIBLE-LXX.txt")

    print(f"Reading LXX CSV from: {csv_path}")

    # Read all verses grouped by book
    book_verses = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        # Tab-delimited: book_id, chapter, verse, greek_text
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 4:
                book_id = int(parts[0])
                chapter = int(parts[1])
                verse = int(parts[2])
                greek_text = strip_markup(parts[3])

                if book_id not in book_verses:
                    book_verses[book_id] = []
                book_verses[book_id].append((chapter, verse, greek_text))

    print(f"Found {len(book_verses)} books with {sum(len(v) for v in book_verses.values())} verses")

    # Write consolidated text
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write("=" * 80 + "\n")
        out.write("THE SEPTUAGINT (LXX)\n")
        out.write("Greek Old Testament - Rahlfs 1935 Edition\n")
        out.write("=" * 80 + "\n\n")

        for book_id, english_name, greek_name in LXX_BOOKS:
            if book_id not in book_verses:
                print(f"Warning: Book {book_id} ({english_name}) not found in CSV")
                continue

            verses = book_verses[book_id]
            print(f"Processing {english_name} ({len(verses)} verses)")

            # Write book header
            out.write("\n\n")
            out.write("=" * 80 + "\n")
            out.write(f"{greek_name}\n")
            out.write(f"{english_name}\n")
            out.write("=" * 80 + "\n\n")

            # Write verses grouped by chapter
            current_chapter = 0
            for chapter, verse, text in sorted(verses):
                if chapter != current_chapter:
                    current_chapter = chapter
                    out.write(f"\n--- Chapter {chapter} ---\n\n")

                out.write(f"{chapter}:{verse} {text}\n")

    print(f"\nConsolidated LXX written to: {output_path}")
    print(f"File size: {output_path.stat().st_size / 1024 / 1024:.1f} MB")

if __name__ == "__main__":
    main()
