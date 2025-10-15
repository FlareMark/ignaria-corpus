#!/usr/bin/env python3
"""
Update anthology volumes with section metadata.
This adds is_anthology flag and sections array to anthology .meta.yaml files.
Reads section data from anthology-sections-complete.yaml.
"""

import yaml
from pathlib import Path

def load_anthology_sections():
    """Load all anthology sections from the complete YAML file."""
    config_file = Path("anthology-sections-complete.yaml")
    if not config_file.exists():
        print(f"⚠  Configuration file not found: {config_file}")
        return {}

    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

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
    print("Updating anthology metadata from anthology-sections-complete.yaml...\n")

    anthology_sections = load_anthology_sections()

    if not anthology_sections:
        print("No anthology sections found.")
        return

    updated_count = 0
    for volume_id, section_data in anthology_sections.items():
        if update_metadata_file(volume_id, section_data):
            updated_count += 1

    print(f"\n✅ Updated {updated_count} anthology volumes")

if __name__ == "__main__":
    main()
