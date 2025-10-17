#!/usr/bin/env python3
"""
Consolidate SBLGNT Greek New Testament files into single text file.

The SBLGNT comes as 27 separate files (one per book). This script:
1. Reads all 27 files in canonical order
2. Combines them into a single BIBLE-SBLGNT.txt file
3. Preserves verse references and Greek text
4. Adds book markers for section identification
"""

import os
from pathlib import Path

# Canonical order of NT books
NT_BOOKS = [
    # Gospels
    ("Matt.txt", "Matthew", "ΚΑΤΑ ΜΑΘΘΑΙΟΝ"),
    ("Mark.txt", "Mark", "ΚΑΤΑ ΜΑΡΚΟΝ"),
    ("Luke.txt", "Luke", "ΚΑΤΑ ΛΟΥΚΑΝ"),
    ("John.txt", "John", "ΚΑΤΑ ΙΩΑΝΝΗΝ"),

    # Acts
    ("Acts.txt", "Acts", "ΠΡΑΞΕΙΣ ΑΠΟΣΤΟΛΩΝ"),

    # Paul's Epistles
    ("Rom.txt", "Romans", "ΠΡΟΣ ΡΩΜΑΙΟΥΣ"),
    ("1Cor.txt", "1 Corinthians", "ΠΡΟΣ ΚΟΡΙΝΘΙΟΥΣ Α"),
    ("2Cor.txt", "2 Corinthians", "ΠΡΟΣ ΚΟΡΙΝΘΙΟΥΣ Β"),
    ("Gal.txt", "Galatians", "ΠΡΟΣ ΓΑΛΑΤΑΣ"),
    ("Eph.txt", "Ephesians", "ΠΡΟΣ ΕΦΕΣΙΟΥΣ"),
    ("Phil.txt", "Philippians", "ΠΡΟΣ ΦΙΛΙΠΠΗΣΙΟΥΣ"),
    ("Col.txt", "Colossians", "ΠΡΟΣ ΚΟΛΟΣΣΑΕΙΣ"),
    ("1Thess.txt", "1 Thessalonians", "ΠΡΟΣ ΘΕΣΣΑΛΟΝΙΚΕΙΣ Α"),
    ("2Thess.txt", "2 Thessalonians", "ΠΡΟΣ ΘΕΣΣΑΛΟΝΙΚΕΙΣ Β"),
    ("1Tim.txt", "1 Timothy", "ΠΡΟΣ ΤΙΜΟΘΕΟΝ Α"),
    ("2Tim.txt", "2 Timothy", "ΠΡΟΣ ΤΙΜΟΘΕΟΝ Β"),
    ("Titus.txt", "Titus", "ΠΡΟΣ ΤΙΤΟΝ"),
    ("Phlm.txt", "Philemon", "ΠΡΟΣ ΦΙΛΗΜΟΝΑ"),

    # General Epistles
    ("Heb.txt", "Hebrews", "ΠΡΟΣ ΕΒΡΑΙΟΥΣ"),
    ("Jas.txt", "James", "ΙΑΚΩΒΟΥ"),
    ("1Pet.txt", "1 Peter", "ΠΕΤΡΟΥ Α"),
    ("2Pet.txt", "2 Peter", "ΠΕΤΡΟΥ Β"),
    ("1John.txt", "1 John", "ΙΩΑΝΝΟΥ Α"),
    ("2John.txt", "2 John", "ΙΩΑΝΝΟΥ Β"),
    ("3John.txt", "3 John", "ΙΩΑΝΝΟΥ Γ"),
    ("Jude.txt", "Jude", "ΙΟΥΔΑ"),

    # Revelation
    ("Rev.txt", "Revelation", "ΑΠΟΚΑΛΥΨΙΣ ΙΩΑΝΝΟΥ"),
]

def consolidate_sblgnt():
    """Consolidate all SBLGNT files into single text file."""

    sblgnt_dir = Path("sources/SBLGNT/data/sblgnt/text")
    output_file = Path("sources/BIBLE-SBLGNT.txt")

    if not sblgnt_dir.exists():
        print(f"❌ SBLGNT directory not found: {sblgnt_dir}")
        return False

    print(f"📖 Consolidating SBLGNT Greek New Testament...")
    print(f"   Source: {sblgnt_dir}")
    print(f"   Output: {output_file}")
    print()

    with open(output_file, 'w', encoding='utf-8') as outf:
        # Write header
        outf.write("THE GREEK NEW TESTAMENT\n")
        outf.write("SBL Greek New Testament (SBLGNT)\n")
        outf.write("Society of Biblical Literature\n")
        outf.write("Edited by Michael W. Holmes\n")
        outf.write("\n")
        outf.write("=" * 80 + "\n\n")

        books_processed = 0

        for filename, english_name, greek_title in NT_BOOKS:
            filepath = sblgnt_dir / filename

            if not filepath.exists():
                print(f"⚠️  Missing file: {filename}")
                continue

            print(f"   Adding: {english_name} ({filename})")

            # Add book header
            outf.write("\n" + "=" * 80 + "\n")
            outf.write(f"{greek_title}\n")
            outf.write(f"({english_name})\n")
            outf.write("=" * 80 + "\n\n")

            # Read and write book content
            with open(filepath, 'r', encoding='utf-8') as inf:
                lines = inf.readlines()

                # Skip the first line (Greek title) since we added our own header
                for line in lines[1:]:
                    line = line.strip()
                    if line:  # Only write non-empty lines
                        outf.write(line + "\n")

            outf.write("\n")  # Add blank line after each book
            books_processed += 1

    print()
    print(f"✅ Consolidated {books_processed}/27 NT books")
    print(f"📄 Output: {output_file}")

    # Get file size
    size_mb = output_file.stat().st_size / (1024 * 1024)
    print(f"📊 Size: {size_mb:.2f} MB")

    return True

if __name__ == '__main__':
    consolidate_sblgnt()
