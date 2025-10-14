#!/usr/bin/env python3
"""
Extract section boundaries from anthology volumes.
This script analyzes text files to identify work boundaries and authors.
"""

import re
from pathlib import Path
from typing import List, Dict
import yaml

# Section patterns for different types of works
SECTION_PATTERNS = [
    # Epistles
    r'^(?:THE\s+)?(?:FIRST|SECOND|THIRD)?\s*EPISTLE\s+OF\s+\w+(?:\s+TO\s+THE\s+\w+)?',
    # Apologies/Apologies
    r'^(?:THE\s+)?(?:FIRST|SECOND)?\s*APOLOG[YI](?:A|ES)?\s+OF\s+\w+',
    # Dialogues
    r'^DIALOGUE\s+(?:OF|WITH|BETWEEN)\s+\w+',
    # Against/Adversus works
    r'^(?:\w+\s+)?AGAINST\s+(?:HERESIES|THE|MARCION)',
    # Fragments
    r'^FRAGMENTS?\s+OF\s+\w+',
    # Martyrdom accounts
    r'^(?:THE\s+)?MARTYRDOM\s+OF\s+\w+',
    # Treatises
    r'^(?:ON|CONCERNING|OF)\s+THE\s+\w+',
    # Homilies
    r'^HOM(?:I|E)L(?:Y|IES)\s+(?:ON|OF)',
    # Church History
    r'^(?:THE\s+)?(?:CHURCH|ECCLESIASTICAL)\s+HISTORY',
    # Letters collection
    r'^(?:THE\s+)?LETTERS?\s+OF\s+\w+',
]

def find_section_markers(text_file: Path, num_lines: int = 100000) -> List[Dict]:
    """Find potential section markers in a text file."""
    sections = []

    with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line_num, line in enumerate(f, 1):
            if line_num > num_lines:
                break

            line_stripped = line.strip()

            # Skip empty lines and very short lines
            if len(line_stripped) < 10:
                continue

            # Check if line matches any section pattern
            for pattern in SECTION_PATTERNS:
                if re.match(pattern, line_stripped, re.IGNORECASE):
                    sections.append({
                        'line_num': line_num,
                        'text': line_stripped,
                        'pattern': pattern
                    })
                    break

    return sections

def extract_author_from_title(title: str, known_authors: List[str]) -> str:
    """Try to extract author name from a work title."""
    title_lower = title.lower()

    for author in known_authors:
        author_parts = author.lower().split()
        # Check if any part of the author name appears in title
        for part in author_parts:
            if len(part) > 3 and part in title_lower:
                return author

    return "Unknown"

def main():
    """Main processing function."""
    sources_dir = Path("sources")

    # Define anthology volumes manually for now
    anthologies = [
        "ANF-01", "ANF-02", "ANF-04", "ANF-05", "ANF-06", "ANF-07", "ANF-09",
        "NPNF2-02", "NPNF2-03", "NPNF2-07", "NPNF2-09", "NPNF2-11", "NPNF2-12", "NPNF2-13"
    ]

    for vol_id in anthologies:
        text_file = sources_dir / f"{vol_id}.txt"
        meta_file = sources_dir / f"{vol_id}.meta.yaml"

        if not text_file.exists() or not meta_file.exists():
            print(f"⚠ Skipping {vol_id} - files not found")
            continue

        # Load metadata to get known authors
        with open(meta_file) as f:
            metadata = yaml.safe_load(f)

        authors = metadata.get('text_info', {}).get('authors', [])

        print(f"\n{'='*60}")
        print(f"Processing: {vol_id}")
        print(f"Authors: {', '.join(authors)}")
        print(f"{'='*60}")

        # Find section markers
        sections = find_section_markers(text_file)

        print(f"\nFound {len(sections)} potential section markers:\n")

        for i, section in enumerate(sections[:30], 1):  # Show first 30
            # Try to identify author
            author = extract_author_from_title(section['text'], authors)
            print(f"{i:2}. Line {section['line_num']:6}: {section['text'][:80]}")
            print(f"    → Likely author: {author}")

        if len(sections) > 30:
            print(f"\n... and {len(sections) - 30} more sections")

if __name__ == "__main__":
    main()
