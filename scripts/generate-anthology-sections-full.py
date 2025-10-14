#!/usr/bin/env python3
"""
Generate complete section metadata for all anthology volumes by analyzing text files.
"""

import re
import yaml
from pathlib import Path
from typing import List, Dict, Tuple

def find_major_sections(text_file: Path) -> List[Tuple[int, str]]:
    """Find major section headers in a text file."""
    sections = []

    # Patterns for major work boundaries
    patterns = [
        r'^The (?:First|Second|Third|Fourth|Fifth) (?:Epistle|Apology|Book)',
        r'^The Epistle of \w+',
        r'^The (?:Encyclical )?Epistle',
        r'^Dialogue of \w+',
        r'^Fragments? of \w+',
        r'^(?:The )?Martyrdom of \w+',
        r'^(?:The )?Church History',
        r'^(?:The )?(?:Ecclesiastical )?History',
        r'^Book [IVX]+\.',
        r'^(?:The )?Letters? of \w+',
        r'^(?:The )?Catechetical Lectures?',
        r'^(?:The )?Orations? of \w+',
        r'^Against (?:Heresies|the|Marcion)',
        r'^On the \w+',
        r'^Concerning the \w+',
    ]

    with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line_num, line in enumerate(f, 1):
            line_stripped = line.strip()

            # Check each pattern
            for pattern in patterns:
                if re.match(pattern, line_stripped, re.IGNORECASE):
                    # Make sure it's a substantial header (not just in body text)
                    if 10 < len(line_stripped) < 150:
                        sections.append((line_num, line_stripped))
                        break

    return sections

def match_section_to_author(section_title: str, authors: List[str]) -> str:
    """Try to match a section title to a known author."""
    section_lower = section_title.lower()

    # Direct name matching
    for author in authors:
        author_parts = author.lower().split()
        for part in author_parts:
            if len(part) > 3 and part in section_lower:
                return author

    # Special cases
    if 'clement' in section_lower:
        return next((a for a in authors if 'Clement' in a), authors[0])
    if 'ignatius' in section_lower:
        return next((a for a in authors if 'Ignatius' in a), authors[0])
    if 'polycarp' in section_lower:
        return next((a for a in authors if 'Polycarp' in a), authors[0])
    if 'justin' in section_lower:
        return next((a for a in authors if 'Justin' in a), authors[0])
    if 'irenaeus' or 'irenæus' in section_lower:
        return next((a for a in authors if 'Irenaeus' in a or 'Irenæus' in a), authors[0])
    if 'barnabas' in section_lower:
        return next((a for a in authors if 'Barnabas' in a), authors[0])
    if 'hermas' in section_lower:
        return next((a for a in authors if 'Hermas' in a), authors[0])
    if 'tatian' in section_lower:
        return next((a for a in authors if 'Tatian' in a), authors[0])
    if 'athenagoras' in section_lower:
        return next((a for a in authors if 'Athenagoras' in a), authors[0])
    if 'theophilus' in section_lower:
        return next((a for a in authors if 'Theophilus' in a), authors[0])
    if 'cyprian' in section_lower:
        return next((a for a in authors if 'Cyprian' in a), authors[0])
    if 'origen' in section_lower:
        return next((a for a in authors if 'Origen' in a), authors[0])
    if 'tertullian' in section_lower:
        return next((a for a in authors if 'Tertullian' in a), authors[0])
    if 'hippolytus' in section_lower:
        return next((a for a in authors if 'Hippolytus' in a), authors[0])
    if 'lactantius' in section_lower:
        return next((a for a in authors if 'Lactantius' in a), authors[0])
    if 'eusebius' in section_lower:
        return next((a for a in authors if 'Eusebius' in a), authors[0])
    if 'socrates' in section_lower:
        return next((a for a in authors if 'Socrates' in a), authors[0])
    if 'sozomen' in section_lower:
        return next((a for a in authors if 'Sozomen' in a), authors[0])
    if 'theodoret' in section_lower:
        return next((a for a in authors if 'Theodoret' in a), authors[0])
    if 'jerome' in section_lower:
        return next((a for a in authors if 'Jerome' in a), authors[0])
    if 'cyril' in section_lower:
        return next((a for a in authors if 'Cyril' in a), authors[0])
    if 'gregory' in section_lower:
        # Be more specific for Gregory
        if 'nazianzen' in section_lower or 'nazianzus' in section_lower:
            return next((a for a in authors if 'Nazian' in a), authors[0])
        return next((a for a in authors if 'Gregory' in a), authors[0])
    if 'hilary' in section_lower:
        return next((a for a in authors if 'Hilary' in a), authors[0])
    if 'john of damascus' in section_lower or 'damascene' in section_lower:
        return next((a for a in authors if 'Damascus' in a), authors[0])
    if 'cassian' in section_lower:
        return next((a for a in authors if 'Cassian' in a), authors[0])
    if 'sulpitius' in section_lower or 'severus' in section_lower:
        return next((a for a in authors if 'Sulp' in a or 'Severus' in a), authors[0])
    if 'vincent' in section_lower:
        return next((a for a in authors if 'Vincent' in a), authors[0])
    if 'leo' in section_lower:
        return next((a for a in authors if 'Leo' in a), authors[0])
    if 'ephrem' in section_lower or 'ephraim' in section_lower:
        return next((a for a in authors if 'Ephrem' in a or 'Ephraim' in a), authors[0])
    if 'aphrahat' in section_lower:
        return next((a for a in authors if 'Aphrahat' in a), authors[0])

    # Default to first author if no match
    return authors[0] if authors else "Unknown"

def extract_work_title(section_marker: str) -> str:
    """Extract a clean work title from section marker."""
    # Remove common prefixes
    title = section_marker
    title = re.sub(r'^The\s+', '', title)
    title = re.sub(r'\s*\[.*?\]\s*$', '', title)  # Remove footnote markers
    title = re.sub(r'\s+http://.*$', '', title)  # Remove URLs

    return title.strip()

def process_anthology(volume_id: str):
    """Process a single anthology volume."""
    text_file = Path(f"sources/{volume_id}.txt")
    meta_file = Path(f"sources/{volume_id}.meta.yaml")

    if not text_file.exists() or not meta_file.exists():
        print(f"⚠ Skipping {volume_id} - files not found")
        return

    # Load metadata
    with open(meta_file, 'r', encoding='utf-8') as f:
        metadata = yaml.safe_load(f)

    authors = metadata.get('text_info', {}).get('authors', [])

    print(f"\n{'='*70}")
    print(f"Processing: {volume_id}")
    print(f"Authors: {', '.join(authors)}")
    print(f"{'='*70}\n")

    # Find sections
    raw_sections = find_major_sections(text_file)

    # Filter and deduplicate
    sections = []
    seen_markers = set()

    for line_num, marker in raw_sections:
        if marker not in seen_markers:
            author = match_section_to_author(marker, authors)
            title = extract_work_title(marker)

            sections.append({
                'author': author,
                'title': title,
                'start_marker': marker,
                'line_num': line_num
            })

            seen_markers.add(marker)

    # Display results
    print(f"Found {len(sections)} unique sections:\n")
    for i, section in enumerate(sections, 1):
        print(f"{i:2}. {section['author']:<25} | {section['title'][:45]}")
        print(f"    Line {section['line_num']:6}: {section['start_marker'][:70]}")
        print()

    # Generate YAML output
    print("\n" + "="*70)
    print("YAML Output for sections array:")
    print("="*70 + "\n")

    yaml_sections = []
    for section in sections:
        yaml_section = {
            'author': section['author'],
            'title': section['title'],
            'start_marker': section['start_marker']
        }
        yaml_sections.append(yaml_section)

    print(yaml.dump({'sections': yaml_sections}, default_flow_style=False, sort_keys=False, allow_unicode=True))

def main():
    """Process all anthology volumes."""
    anthologies = [
        "ANF-01", "ANF-02", "ANF-04", "ANF-05", "ANF-06", "ANF-07", "ANF-09",
        "NPNF2-02", "NPNF2-03", "NPNF2-07", "NPNF2-09", "NPNF2-11", "NPNF2-12", "NPNF2-13"
    ]

    for vol_id in anthologies:
        process_anthology(vol_id)
        input("\nPress Enter to continue to next volume...")

if __name__ == "__main__":
    main()
