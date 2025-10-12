#!/usr/bin/env python3
"""
Update manifest.yaml to include all Church Fathers volumes.
"""

import yaml
from pathlib import Path
from datetime import date

# Import the metadata from the generation script
import sys
sys.path.append(str(Path(__file__).parent))
from generate_church_fathers_metadata import CHURCH_FATHERS_METADATA

def update_manifest():
    """Add all Church Fathers volumes to manifest."""
    corpus_root = Path(__file__).parent.parent
    manifest_path = corpus_root / "manifest.yaml"

    # Load current manifest
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = yaml.safe_load(f)

    # Update version and date
    manifest['corpus']['version'] = "2.0.0"
    manifest['corpus']['last_updated'] = str(date.today())

    # Add Church Fathers volumes
    for volume_id, info in CHURCH_FATHERS_METADATA.items():
        volume_id_lower = volume_id.lower()

        # Check if already exists
        existing = any(text['id'] == volume_id_lower for text in manifest['texts'])
        if existing:
            print(f"  Skipping {volume_id} (already exists)")
            continue

        # Create text entry
        text_entry = {
            "id": volume_id_lower,
            "title": info['title'],
            "author": ", ".join(info['authors'][:3]) + (" et al." if len(info['authors']) > 3 else ""),
            "period": info['period'],
            "genre": "Patristic Collection",
            "file": f"sources/{volume_id}.txt",
            "metadata": f"sources/{volume_id}.meta.yaml",
            "status": "active",
            "added": str(date.today())
        }

        manifest['texts'].append(text_entry)
        print(f"✓ Added {volume_id}")

    # Update categories
    if 'categories' not in manifest:
        manifest['categories'] = {}

    # Add all Church Fathers to patristic category
    church_fathers_ids = [vid.lower() for vid in CHURCH_FATHERS_METADATA.keys()]

    if 'patristic' not in manifest['categories']:
        manifest['categories']['patristic'] = []

    # Add new volumes to patristic category (avoid duplicates)
    for cf_id in church_fathers_ids:
        if cf_id not in manifest['categories']['patristic']:
            manifest['categories']['patristic'].append(cf_id)

    # Add series-specific categories
    anf_ids = [vid.lower() for vid in CHURCH_FATHERS_METADATA.keys() if vid.startswith("ANF")]
    npnf1_ids = [vid.lower() for vid in CHURCH_FATHERS_METADATA.keys() if vid.startswith("NPNF1")]
    npnf2_ids = [vid.lower() for vid in CHURCH_FATHERS_METADATA.keys() if vid.startswith("NPNF2")]

    manifest['categories']['ante-nicene'] = anf_ids
    manifest['categories']['nicene-post-nicene-1'] = npnf1_ids
    manifest['categories']['nicene-post-nicene-2'] = npnf2_ids

    # Augustine-specific (NPNF1 volumes 1-8)
    manifest['categories']['augustine'] = [f"npnf1-{str(i).zfill(2)}" for i in range(1, 9)] + ["augustine-confessions"]

    # Chrysostom-specific (NPNF1 volumes 9-14)
    manifest['categories']['chrysostom'] = [f"npnf1-{str(i).zfill(2)}" for i in range(9, 15)]

    # Save updated manifest
    with open(manifest_path, 'w', encoding='utf-8') as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"\n✅ Updated manifest.yaml successfully!")
    print(f"   Version: {manifest['corpus']['version']}")
    print(f"   Total texts: {len(manifest['texts'])}")
    print(f"   Categories: {len(manifest['categories'])}")

if __name__ == "__main__":
    update_manifest()
