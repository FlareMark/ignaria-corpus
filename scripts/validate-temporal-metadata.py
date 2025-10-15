#!/usr/bin/env python3
"""
Validate temporal metadata in anthology volumes.
Checks for composition_year, author_region, and author_location fields.
"""

import yaml
from pathlib import Path
import sys

def load_meta_file(file_path):
    """Load a .meta.yaml file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def validate_temporal_metadata(meta_path):
    """Validate temporal metadata for an anthology volume."""
    metadata = load_meta_file(meta_path)
    text_info = metadata.get('text_info', {})

    volume_id = text_info.get('id', 'unknown')
    is_anthology = text_info.get('is_anthology', False)

    if not is_anthology:
        return {
            'volume_id': volume_id,
            'is_anthology': False,
            'skipped': True
        }

    sections = text_info.get('sections', [])

    results = {
        'volume_id': volume_id,
        'is_anthology': True,
        'total_sections': len(sections),
        'sections_with_temporal': 0,
        'sections_missing_temporal': 0,
        'missing_sections': []
    }

    for section in sections:
        author = section.get('author', 'Unknown')
        title = section.get('title', 'Unknown')

        has_year = 'composition_year' in section
        has_region = 'author_region' in section
        has_location = 'author_location' in section

        if has_year and has_region and has_location:
            results['sections_with_temporal'] += 1
        else:
            results['sections_missing_temporal'] += 1
            results['missing_sections'].append({
                'author': author,
                'title': title,
                'has_composition_year': has_year,
                'has_author_region': has_region,
                'has_author_location': has_location
            })

    return results

def main():
    """Main validation routine."""
    sources_dir = Path('sources')

    if not sources_dir.exists():
        print("❌ 'sources/' directory not found")
        print("   Run this script from the corpus root directory")
        sys.exit(1)

    # Find all anthology metadata files
    anthology_files = []
    for meta_file in sources_dir.glob('*.meta.yaml'):
        metadata = load_meta_file(meta_file)
        if metadata.get('text_info', {}).get('is_anthology', False):
            anthology_files.append(meta_file)

    print(f"\n📚 Found {len(anthology_files)} anthology volumes\n")

    # Validate each anthology
    all_results = []
    for meta_file in sorted(anthology_files):
        results = validate_temporal_metadata(meta_file)
        all_results.append(results)

    # Print summary
    print("=" * 80)
    print(" TEMPORAL METADATA VALIDATION REPORT")
    print("=" * 80)
    print()

    complete_volumes = []
    incomplete_volumes = []

    for results in all_results:
        volume_id = results['volume_id']
        total = results['total_sections']
        with_temporal = results['sections_with_temporal']
        missing = results['sections_missing_temporal']

        if missing == 0:
            complete_volumes.append(volume_id)
            status = "✅ COMPLETE"
        else:
            incomplete_volumes.append((volume_id, results))
            status = f"⚠️  INCOMPLETE ({missing}/{total} missing)"

        print(f"{volume_id:15} {status}")

    print()
    print("=" * 80)
    print()

    # Print detailed info for incomplete volumes
    if incomplete_volumes:
        print("📋 INCOMPLETE VOLUMES - MISSING METADATA:")
        print()

        for volume_id, results in incomplete_volumes:
            print(f"\n{volume_id}:")
            print(f"  Total sections: {results['total_sections']}")
            print(f"  Complete: {results['sections_with_temporal']}")
            print(f"  Missing: {results['sections_missing_temporal']}")
            print()
            print("  Sections missing temporal metadata:")

            for section in results['missing_sections']:
                print(f"    - {section['author']}: {section['title']}")
                missing_fields = []
                if not section['has_composition_year']:
                    missing_fields.append('composition_year')
                if not section['has_author_region']:
                    missing_fields.append('author_region')
                if not section['has_author_location']:
                    missing_fields.append('author_location')
                print(f"      Missing: {', '.join(missing_fields)}")

    # Print summary stats
    print()
    print("=" * 80)
    print(" SUMMARY")
    print("=" * 80)
    print()
    print(f"  Total anthology volumes: {len(all_results)}")
    print(f"  Complete volumes: {len(complete_volumes)}")
    print(f"  Incomplete volumes: {len(incomplete_volumes)}")
    print()

    total_sections = sum(r['total_sections'] for r in all_results)
    complete_sections = sum(r['sections_with_temporal'] for r in all_results)

    completion_pct = (complete_sections / total_sections * 100) if total_sections > 0 else 0

    print(f"  Total sections: {total_sections}")
    print(f"  Sections with temporal metadata: {complete_sections}")
    print(f"  Completion: {completion_pct:.1f}%")
    print()

    if incomplete_volumes:
        print("⚠️  Action needed: Add temporal metadata to incomplete volumes")
        sys.exit(1)
    else:
        print("✅ All anthology volumes have complete temporal metadata!")
        sys.exit(0)

if __name__ == '__main__':
    main()
