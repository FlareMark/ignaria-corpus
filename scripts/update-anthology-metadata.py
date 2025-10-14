#!/usr/bin/env python3
"""
Update anthology volumes with section metadata.
This adds is_anthology flag and sections array to anthology .meta.yaml files.
"""

import yaml
from pathlib import Path

# Curated section data for each anthology volume
# Only including the main/canonical sections, not spurious letters

ANTHOLOGY_SECTIONS = {
    "ANF-01": {
        "is_anthology": True,
        "sections": [
            {
                "author": "Clement of Rome",
                "title": "First Epistle to the Corinthians",
                "start_marker": "The First Epistle of Clement to the Corinthians"
            },
            {
                "author": "Mathetes",
                "title": "Epistle to Diognetus",
                "start_marker": "The Epistle of Mathetes to Diognetus"
            },
            {
                "author": "Polycarp",
                "title": "Epistle to the Philippians",
                "start_marker": "The Epistle of Polycarp to the Philippians"
            },
            {
                "author": "Polycarp",
                "title": "Martyrdom of Polycarp",
                "start_marker": "The Encyclical Epistle of the Church at Smyrna Concerning the Martyrdom of the"
            },
            {
                "author": "Ignatius",
                "title": "Epistle to the Ephesians",
                "start_marker": "The Epistle of Ignatius to the Ephesians"
            },
            {
                "author": "Ignatius",
                "title": "Epistle to the Magnesians",
                "start_marker": "The Epistle of Ignatius to the Magnesians"
            },
            {
                "author": "Ignatius",
                "title": "Epistle to the Trallians",
                "start_marker": "The Epistle of Ignatius to the Trallians"
            },
            {
                "author": "Ignatius",
                "title": "Epistle to the Romans",
                "start_marker": "The Epistle of Ignatius to the Romans"
            },
            {
                "author": "Ignatius",
                "title": "Epistle to the Philadelphians",
                "start_marker": "The Epistle of Ignatius to the Philadelphians"
            },
            {
                "author": "Ignatius",
                "title": "Epistle to the Smyrnaeans",
                "start_marker": "The Epistle of Ignatius to the SmyrnÃ¦ans"
            },
            {
                "author": "Ignatius",
                "title": "Epistle to Polycarp",
                "start_marker": "The Epistle of Ignatius to Polycarp"
            },
            {
                "author": "Ignatius",
                "title": "Martyrdom of Ignatius",
                "start_marker": "The Martyrdom of Ignatius"
            },
            {
                "author": "Barnabas",
                "title": "Epistle of Barnabas",
                "start_marker": "The Epistle of Barnabas"
            },
            {
                "author": "Papias",
                "title": "Fragments of Papias",
                "start_marker": "Fragments of Papias"
            },
            {
                "author": "Justin Martyr",
                "title": "First Apology",
                "start_marker": "The First Apology of Justin"
            },
            {
                "author": "Justin Martyr",
                "title": "Second Apology",
                "start_marker": "The Second Apology of Justin for the Christians Addressed to the Roman Senate"
            },
            {
                "author": "Justin Martyr",
                "title": "Dialogue with Trypho",
                "start_marker": "Dialogue of Justin, Philosopher and Martyr, with Trypho, a Jew"
            },
            {
                "author": "Justin Martyr",
                "title": "Fragments on the Resurrection",
                "start_marker": "Fragments of the Lost Work of Justin on the Resurrection"
            },
            {
                "author": "Justin Martyr",
                "title": "Martyrdom of Justin and Companions",
                "start_marker": "The Martyrdom of the Holy Martyrs Justin, Chariton, Charites, PÃ¦on, and"
            }
        ]
    },

    # More volumes will be added progressively
    # For now, this demonstrates the structure
}

def update_metadata_file(volume_id: str, section_data: dict):
    """Add section metadata to a volume's .meta.yaml file."""
    meta_path = Path(f"sources/{volume_id}.meta.yaml")

    if not meta_path.exists():
        print(f"⚠  {volume_id}: Metadata file not found")
        return False

    # Load existing metadata
    with open(meta_path, 'r', encoding='utf-8') as f:
        metadata = yaml.safe_load(f)

    # Add anthology metadata
    metadata['text_info']['is_anthology'] = section_data['is_anthology']
    metadata['text_info']['sections'] = section_data['sections']

    # Save updated metadata
    with open(meta_path, 'w', encoding='utf-8') as f:
        yaml.dump(metadata, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"✓  {volume_id}: Added {len(section_data['sections'])} sections")
    return True

def main():
    """Update all configured anthology volumes."""
    print("Updating anthology metadata...\n")

    for volume_id, section_data in ANTHOLOGY_SECTIONS.items():
        update_metadata_file(volume_id, section_data)

    print(f"\n✅ Updated {len(ANTHOLOGY_SECTIONS)} anthology volumes")

if __name__ == "__main__":
    main()
