# Corpus Ingestion Guide

**For developers building RAG/semantic search systems with the Ignaria Corpus**

## Quick Start: What to Ingest

### Filter by Status

**ONLY ingest texts with `status: active`**

```python
def get_texts_for_ingestion(manifest):
    """Get texts that should be ingested for semantic search."""
    texts = manifest.get('texts', [])
    return [text for text in texts if text.get('status') == 'active']
```

### Status Values Explained

| Status | Meaning | Action |
|--------|---------|--------|
| `active` | Ready for ingestion | ✅ **Ingest for semantic search** |
| `reference` | For citation only | ❌ Do NOT ingest (keep accessible for reference) |
| `deprecated` | Being phased out | ❌ Do NOT ingest |
| `pending` | Not ready | ❌ Do NOT ingest |

## Current Corpus Breakdown (v2.2.0)

### Active Texts (FOR INGESTION)

**Biblical:**
- `bible-kjv` - King James Version (English)
  - 66 books, 31,102 verses
  - Primary biblical text for English queries

**Patristic (Church Fathers):**
- All 37 Early Church Fathers volumes (ANF, NPNF1, NPNF2)
- Ante-Nicene through 8th century
- English translations

**Total Active:** 38 texts

### Reference Texts (DO NOT INGEST)

**Greek Biblical Sources:**
- `bible-sblgnt` - Greek New Testament (27 books)
- `bible-lxx` - Greek Old Testament/Septuagint (54 books)

**Why reference-only?**
1. ❌ Greek text won't match English semantic search queries
2. ✅ Needed for verifying Church Father quotations (they quoted LXX, not Hebrew)
3. ✅ Scholarly cross-referencing and citation
4. ✅ Future multilingual capabilities

**Total Reference:** 2 texts

## Implementation Example

### Full Ingestion Pipeline

```python
import yaml
from pathlib import Path

def load_corpus_for_ingestion(corpus_path):
    """
    Load all texts ready for RAG ingestion.
    Returns documents with content and metadata.
    """
    corpus_root = Path(corpus_path)

    # Load manifest
    with open(corpus_root / 'manifest.yaml', 'r') as f:
        manifest = yaml.safe_load(f)

    documents = []

    # Filter to active texts only
    for text_entry in manifest.get('texts', []):
        if text_entry.get('status') != 'active':
            print(f"Skipping {text_entry['id']} (status: {text_entry.get('status')})")
            continue

        # Load text content
        text_path = corpus_root / text_entry['file']
        with open(text_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Load detailed metadata
        meta_path = corpus_root / text_entry['metadata']
        with open(meta_path, 'r', encoding='utf-8') as f:
            metadata = yaml.safe_load(f)

        # Create document
        doc = {
            'id': text_entry['id'],
            'content': content,
            'metadata': {
                'title': text_entry['title'],
                'author': text_entry['author'],
                'period': text_entry.get('period'),
                'genre': text_entry.get('genre'),
                'detailed_metadata': metadata
            }
        }

        documents.append(doc)
        print(f"✅ Loaded {text_entry['id']} for ingestion")

    return documents

# Usage
docs = load_corpus_for_ingestion('/path/to/ignaria-corpus')
print(f"\nReady to ingest {len(docs)} texts")
```

### Expected Output (v2.2.0)

```
✅ Loaded bible-kjv for ingestion
Skipping bible-sblgnt (status: reference)
Skipping bible-lxx (status: reference)
✅ Loaded anf-01 for ingestion
✅ Loaded anf-02 for ingestion
...
✅ Loaded npnf2-14 for ingestion

Ready to ingest 38 texts
```

## Handling Reference Texts

Even though reference texts aren't ingested, they should remain **accessible** in your system for:

1. **Citation Display** - Show Greek source when displaying quotations
2. **Verification** - Check patristic quotations against original Greek
3. **Cross-Reference** - Compare translations
4. **Future Use** - Enable multilingual search later

### Storage Strategy

```
your-app/
├── data/
│   ├── embeddings/          # Vector DB with active texts only
│   ├── corpus/              # Full corpus (active + reference)
│   └── reference/           # Symlink to reference texts
```

## Chunking Strategies

See [SYSTEM_GUIDE.md](../SYSTEM_GUIDE.md) for:
- Anthology volume handling (multi-author texts)
- Section-level attribution
- Temporal metadata usage
- Chunk size recommendations

## Validation

Before ingestion, validate your filtering:

```python
def validate_ingestion_selection(manifest):
    """Ensure you're ingesting the right texts."""
    texts = manifest.get('texts', [])

    active = [t for t in texts if t.get('status') == 'active']
    reference = [t for t in texts if t.get('status') == 'reference']
    other = [t for t in texts if t.get('status') not in ['active', 'reference']]

    print(f"Active (for ingestion): {len(active)}")
    print(f"Reference (skip ingestion): {len(reference)}")
    print(f"Other statuses: {len(other)}")

    # Verify Greek texts are reference-only
    greek_texts = ['bible-sblgnt', 'bible-lxx']
    for text_id in greek_texts:
        text = next((t for t in texts if t['id'] == text_id), None)
        if text and text.get('status') != 'reference':
            raise ValueError(f"Greek text {text_id} should have status='reference'")

    print("✅ Validation passed")
```

## Questions?

See the main [SYSTEM_GUIDE.md](../SYSTEM_GUIDE.md) for comprehensive documentation.
