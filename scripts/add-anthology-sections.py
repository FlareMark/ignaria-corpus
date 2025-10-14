#!/usr/bin/env python3
"""
Add section metadata to anthology volumes.
This script adds explicit section boundaries to anthology .meta.yaml files.
"""

import yaml
from pathlib import Path
from datetime import date

# Define sections for each anthology volume
# Format: {volume_id: [{author, title, start_marker, notes}, ...]}

ANTHOLOGY_SECTIONS = {
    "ANF-01": [
        {"author": "Clement of Rome", "title": "First Epistle to the Corinthians",
         "start_marker": "The First Epistle of Clement to the Corinthians"},
        {"author": "Mathetes", "title": "Epistle to Diognetus",
         "start_marker": "The Epistle of Mathetes to Diognetus"},
        {"author": "Polycarp", "title": "Epistle to the Philippians",
         "start_marker": "The Epistle of Polycarp to the Philippians"},
        {"author": "Polycarp", "title": "Martyrdom of Polycarp",
         "start_marker": "The Encyclical Epistle of the Church at Smyrna Concerning the Martyrdom of the"},
        {"author": "Ignatius", "title": "Epistle to the Ephesians",
         "start_marker": "The Epistle of Ignatius to the Ephesians"},
        {"author": "Ignatius", "title": "Epistle to the Magnesians",
         "start_marker": "The Epistle of Ignatius to the Magnesians"},
        {"author": "Ignatius", "title": "Epistle to the Trallians",
         "start_marker": "The Epistle of Ignatius to the Trallians"},
        {"author": "Ignatius", "title": "Epistle to the Romans",
         "start_marker": "The Epistle of Ignatius to the Romans"},
        {"author": "Ignatius", "title": "Epistle to the Philadelphians",
         "start_marker": "The Epistle of Ignatius to the Philadelphians"},
        {"author": "Ignatius", "title": "Epistle to the Smyrnaeans",
         "start_marker": "The Epistle of Ignatius to the SmyrnÃ¦ans"},
        {"author": "Ignatius", "title": "Epistle to Polycarp",
         "start_marker": "The Epistle of Ignatius to Polycarp"},
        {"author": "Barnabas", "title": "Epistle of Barnabas",
         "start_marker": "The Epistle of Barnabas"},
        {"author": "Papias", "title": "Fragments of Papias",
         "start_marker": "Fragments of Papias"},
        {"author": "Justin Martyr", "title": "First Apology",
         "start_marker": "The First Apology of Justin"},
        {"author": "Justin Martyr", "title": "Second Apology",
         "start_marker": "The Second Apology of Justin for the Christians Addressed to the Roman Senate"},
        {"author": "Justin Martyr", "title": "Dialogue with Trypho",
         "start_marker": "Dialogue of Justin, Philosopher and Martyr, with Trypho, a Jew"},
        {"author": "Justin Martyr", "title": "Fragments on the Resurrection",
         "start_marker": "Fragments of the Lost Work of Justin on the Resurrection"},
        {"author": "Irenaeus", "title": "Fragments from Lost Writings",
         "start_marker": "Fragments from the Lost Writings of IrenÃ¦us"},
    ],

    # I'll add more volumes as needed - this demonstrates the pattern
}

def add_sections_to_metadata(volume_id: str, sections: list):
    """Add section metadata to a volume's .meta.yaml file."""
    meta_path = Path(f"sources/{volume_id}.meta.yaml")

    if not meta_path.exists():
        print(f"⚠ Skipping {volume_id} - metadata file not found")
        return False

    # Load existing metadata
    with open(meta_path, 'r', encoding='utf-8') as f:
        metadata = yaml.safe_load(f)

    # Add anthology flag and sections
    metadata['text_info']['is_anthology'] = True
    metadata['text_info']['sections'] = sections

    # Save updated metadata
    with open(meta_path, 'w', encoding='utf-8') as f:
        yaml.dump(metadata, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"✓ Added {len(sections)} sections to {volume_id}")
    return True

def main():
    """Process all anthology volumes."""
    print("Adding section metadata to anthology volumes...\n")

    for volume_id, sections in ANTHOLOGY_SECTIONS.items():
        add_sections_to_metadata(volume_id, sections)

    print(f"\n✅ Processed {len(ANTHOLOGY_SECTIONS)} anthology volumes")

if __name__ == "__main__":
    main()
