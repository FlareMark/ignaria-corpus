# Ignaria Corpus - System Integration Guide

**For: Ignaria RAG System and AI Agents**

This document provides a structured overview of the ignaria-corpus repository for automated systems that need to understand and work with this corpus.

---

## Repository Purpose

The ignaria-corpus is a curated collection of classical Christian philosophical and theological texts designed for:
- Retrieval-Augmented Generation (RAG) systems
- Theological research and analysis
- Academic study and computational linguistics
- AI agent knowledge bases

**Repository Type:** Text corpus (separate from application code)
**Primary Use Case:** Source material for Ignaria theological AI system
**Governance:** Curated by scholars and theologians

---

## Repository Structure

```
ignaria-corpus/
├── manifest.yaml              # CANONICAL SOURCE OF TRUTH
├── CHANGELOG.md              # Version history
├── README.md                 # Human documentation
├── SYSTEM_GUIDE.md           # This file - for AI systems
├── sources/                  # All text files and metadata
│   ├── {text-id}.txt        # Plain text source files
│   └── {text-id}.meta.yaml  # Detailed metadata per text
└── scripts/                  # Maintenance utilities
    ├── validate.py          # Corpus validation
    ├── download.py          # Text acquisition
    └── clean.py             # Text normalization
```

---

## Key Concepts

### 1. Manifest-Based Architecture

**The `manifest.yaml` file is the single source of truth.**

- Lists all texts in the corpus
- Provides core metadata for each text
- Defines categorization and organization
- Tracks text status (active, deprecated, pending)

**Important:** Always read the manifest first before processing any texts.

### 2. Text Identification

Each text has a unique `id` (e.g., `augustine-confessions`):
- Used to reference texts across systems
- Maps to files: `sources/{id}.txt` and `sources/{id}.meta.yaml`
- Stable across versions (IDs should not change)

### 3. Metadata Schema

Each text has two metadata layers:

**Layer 1: Manifest Entry (manifest.yaml)**
- Basic identification (id, title, author)
- File paths
- Status and dates
- High-level categorization

**Layer 2: Detailed Metadata ({id}.meta.yaml)**
- Publication information
- Content structure
- Source and licensing
- Technical specifications
- Cataloging identifiers
- Thematic analysis

---

## How to Consume This Corpus

### Step 1: Clone or Reference the Repository

```bash
# Clone as standalone
git clone https://github.com/flaremark/ignaria-corpus

# Or add as submodule to your application
git submodule add https://github.com/flaremark/ignaria-corpus data/corpus
```

### Step 2: Load the Manifest

```python
import yaml
from pathlib import Path

def load_corpus_manifest(corpus_path):
    """Load the canonical manifest."""
    manifest_path = Path(corpus_path) / "manifest.yaml"
    with open(manifest_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

manifest = load_corpus_manifest('/path/to/ignaria-corpus')
```

### Step 3: Iterate Through Active Texts

```python
def get_active_texts(manifest):
    """Get all active texts from the corpus."""
    texts = manifest.get('texts', [])
    return [text for text in texts if text.get('status') == 'active']

active_texts = get_active_texts(manifest)
```

### Step 4: Load Text Content and Metadata

```python
def load_text_with_metadata(corpus_path, text_entry):
    """Load a text file and its metadata."""
    corpus_root = Path(corpus_path)

    # Load text content
    text_path = corpus_root / text_entry['file']
    with open(text_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Load detailed metadata
    meta_path = corpus_root / text_entry['metadata']
    with open(meta_path, 'r', encoding='utf-8') as f:
        metadata = yaml.safe_load(f)

    return {
        'id': text_entry['id'],
        'content': content,
        'manifest_entry': text_entry,
        'detailed_metadata': metadata
    }
```

### Step 5: Process for RAG/Embedding

```python
def prepare_for_rag(corpus_path, manifest):
    """Prepare all texts for RAG ingestion."""
    texts = get_active_texts(manifest)
    documents = []

    for text_entry in texts:
        text_data = load_text_with_metadata(corpus_path, text_entry)

        # Create document with metadata for retrieval
        doc = {
            'id': text_data['id'],
            'content': text_data['content'],
            'metadata': {
                'title': text_entry['title'],
                'author': text_entry['author'],
                'period': text_entry.get('period'),
                'genre': text_entry.get('genre'),
                'language': text_entry.get('language'),
                # Add more fields as needed
            }
        }
        documents.append(doc)

    return documents
```

---

## Manifest Structure Reference

### Top-Level Fields

```yaml
corpus:
  name: "Ignaria Corpus"
  version: "1.0.0"
  description: "A curated collection..."
  last_updated: "2024-01-01"

texts:
  - [list of text entries]

categories:
  [category-name]:
    - [text-id]
    - [text-id]
```

### Text Entry Fields

**Required:**
- `id` (string): Unique identifier
- `title` (string): Work title
- `author` (string): Author name
- `file` (string): Path to text file
- `metadata` (string): Path to metadata file
- `status` (enum): active | deprecated | pending
- `added` (date): Date added to corpus

**Optional:**
- `original_author` (string): Original language name
- `language` (string): Original language
- `period` (string): Historical period
- `genre` (string): Text genre/type

---

## Metadata File Structure

### Required Sections

```yaml
text_info:
  id: "text-id"
  title: "Full Title"
  author: "Author Name"

publication:
  original_language: "Latin"
  original_date: "397-400 AD"
  period: "Late Antiquity"
  genre: "Category"

technical:
  encoding: "UTF-8"
  format: "Plain text"
  line_endings: "Unix (LF)"
```

### Optional Sections

- `content`: Structure, themes, word count
- `sources`: Edition, translator, license
- `cataloging`: ISBN, Library of Congress, etc.
- `philosophical_context`: Method, influences
- `notes`: Additional context

### Anthology Volumes (NEW in v2.0+)

For multi-author anthology volumes, the metadata includes section markers:

```yaml
text_info:
  id: "anf-02"
  title: "Ante-Nicene Fathers, Vol. II"
  authors:
    - Hermas
    - Tatian
    - Theophilus
    - Athenagoras
    - Clement of Alexandria
  is_anthology: true
  sections:
    - author: "Hermas"
      title: "The Pastor of Hermas"
      start_marker: "                              The Pastor of Hermas"
    - author: "Tatian"
      title: "Address to the Greeks"
      start_marker: "                         Tatian's Address to the Greeks"
    # ... more sections
```

**Key Fields:**
- `is_anthology` (boolean): Indicates multi-author volume
- `sections` (array): List of major works within the volume
  - `author` (string): Author of this section
  - `title` (string): Work title
  - `start_marker` (string): **Exact text** that marks the beginning of this section
  - `notes` (string, optional): Additional context

**Purpose:** Enables precise attribution of text chunks to specific authors within anthology volumes, critical for multi-source corroboration in RAG systems.

---

## Validation and Quality Assurance

### Before Using the Corpus

Always validate the corpus integrity:

```bash
# Validate corpus structure and content
python scripts/validate.py --corpus-root /path/to/corpus

# Generate validation report
python scripts/validate.py --report validation_report.yaml
```

### What Validation Checks

- Manifest YAML structure
- All referenced files exist
- UTF-8 encoding validity
- Metadata completeness
- Orphaned files detection
- Line ending consistency

---

## Text Format Specifications

### Encoding
- **Always UTF-8** (no other encodings)
- NFC Unicode normalization applied

### Line Endings
- Unix format (LF / `\n`)
- Consistent throughout each file

### Structure
- Plain text format
- No special formatting codes
- Paragraph breaks: double newline (`\n\n`)
- Cleaned of headers/footers/page numbers

### Content Notes
- Some texts may be excerpts (noted in metadata)
- Full texts available when licensing permits
- Editorial notes marked clearly

---

## Categorization System

### Current Categories (Expandable)

**Historical Periods:**
- `patristic`: Early Church Fathers (c. 100-700 AD)
- `scholastic`: Medieval scholastic philosophy (c. 1000-1500 AD)

**Topical:**
- `theology`: Systematic theological works
- `philosophy`: Philosophical treatises
- `biblical_commentary`: Scripture interpretation

**Usage:**
Categories are defined in manifest and are many-to-many (one text can belong to multiple categories).

---

## Version Pinning and Updates

### Semantic Versioning

The corpus follows semantic versioning (major.minor.patch):

- **Major:** Breaking changes (text removal, ID changes, structure changes)
- **Minor:** New texts added, new categories
- **Patch:** Corrections, metadata improvements, text cleaning

### Recommended Integration Pattern

```yaml
# In your application config
corpus:
  repository: "https://github.com/flaremark/ignaria-corpus"
  version: "1.0.0"  # Pin to specific version
  # or
  commit: "abc123def"  # Pin to specific commit
  # NOT
  branch: "main"  # Don't use floating reference in production
```

### Checking for Updates

```bash
# Check current version
cat manifest.yaml | grep "version:"

# See what's changed
cat CHANGELOG.md
```

---

## Licensing and Attribution

### Corpus Texts
- Public domain texts: No restrictions
- Licensed texts: Check individual metadata files
- Always preserve attribution information

### Scripts and Tooling
- MIT License (or as specified in LICENSE file)
- Free to use, modify, distribute

### How to Attribute

When using texts from this corpus:

```
Source: Ignaria Corpus
Text: [Title] by [Author]
Corpus Version: [version]
Repository: https://github.com/flaremark/ignaria-corpus
```

---

## Error Handling

### Missing or Invalid Files

```python
def safe_load_text(corpus_path, text_entry):
    """Load text with error handling."""
    try:
        return load_text_with_metadata(corpus_path, text_entry)
    except FileNotFoundError:
        # Log error and skip
        print(f"Warning: Text file not found: {text_entry['id']}")
        return None
    except yaml.YAMLError as e:
        # Log YAML parsing error
        print(f"Error parsing metadata for {text_entry['id']}: {e}")
        return None
```

### Validation Failures

If validation fails, the corpus may be corrupted or incomplete:
1. Check the validation report
2. Re-clone the repository
3. Verify you're using a stable release tag

---

## Programmatic Access Examples

### Example 1: Build Text Index

```python
def build_text_index(corpus_path):
    """Create searchable index of all texts."""
    manifest = load_corpus_manifest(corpus_path)
    index = {}

    for text in get_active_texts(manifest):
        index[text['id']] = {
            'title': text['title'],
            'author': text['author'],
            'file_path': str(Path(corpus_path) / text['file']),
            'metadata_path': str(Path(corpus_path) / text['metadata'])
        }

    return index
```

### Example 2: Filter by Category

```python
def get_texts_by_category(manifest, category_name):
    """Get all text IDs in a category."""
    categories = manifest.get('categories', {})
    return categories.get(category_name, [])

# Usage
patristic_ids = get_texts_by_category(manifest, 'patristic')
```

### Example 3: Search by Author

```python
def find_by_author(manifest, author_name):
    """Find all texts by an author."""
    results = []
    for text in manifest.get('texts', []):
        if author_name.lower() in text.get('author', '').lower():
            results.append(text)
    return results
```

### Example 4: Process Anthology Sections (NEW)

```python
def chunk_anthology_volume(corpus_path, text_entry, metadata):
    """
    Split anthology volume into sections by author.
    Enables precise attribution for RAG systems.
    """
    # Load text content
    text_path = Path(corpus_path) / text_entry['file']
    with open(text_path, 'r', encoding='utf-8') as f:
        full_text = f.read()

    # Check if this is an anthology
    text_info = metadata.get('text_info', {})
    if not text_info.get('is_anthology'):
        # Single author - treat as one chunk
        return [{
            'author': text_entry['author'],
            'title': text_entry['title'],
            'content': full_text,
            'text_id': text_entry['id']
        }]

    # Multi-author anthology - split by sections
    sections = text_info.get('sections', [])
    chunks = []

    for i, section in enumerate(sections):
        # Find where this section starts
        start_marker = section['start_marker']
        start_pos = full_text.find(start_marker)

        if start_pos == -1:
            print(f"Warning: start_marker not found for {section['title']}")
            continue

        # Find where next section starts (or end of file)
        if i + 1 < len(sections):
            next_marker = sections[i + 1]['start_marker']
            end_pos = full_text.find(next_marker)
        else:
            end_pos = len(full_text)

        # Extract section content
        section_content = full_text[start_pos:end_pos]

        chunks.append({
            'author': section['author'],
            'title': section['title'],
            'content': section_content,
            'text_id': text_entry['id'],
            'volume_title': text_entry['title'],
            'section_notes': section.get('notes', '')
        })

    return chunks

# Usage example
def prepare_corpus_with_sections(corpus_path, manifest):
    """Prepare corpus with anthology sections properly split."""
    all_chunks = []

    for text_entry in get_active_texts(manifest):
        # Load detailed metadata
        meta_path = Path(corpus_path) / text_entry['metadata']
        with open(meta_path, 'r', encoding='utf-8') as f:
            metadata = yaml.safe_load(f)

        # Get chunks (either one for single-author, or many for anthology)
        chunks = chunk_anthology_volume(corpus_path, text_entry, metadata)
        all_chunks.extend(chunks)

    return all_chunks
```

**Benefits of Anthology Sections:**
1. **Precise Attribution**: Know which Church Father wrote each passage
2. **Multi-Source Corroboration**: Track when multiple authors address the same topic
3. **Filtered Search**: Query by specific author within anthology volumes
4. **Proper Citations**: Generate accurate references with author and work title

**Anthology Volumes in Corpus (14 total):**
- ANF-01, ANF-02, ANF-04, ANF-05, ANF-06, ANF-07, ANF-09
- NPNF2-02, NPNF2-03, NPNF2-07, NPNF2-09, NPNF2-11, NPNF2-12, NPNF2-13

---

## Best Practices for AI Systems

### DO:
- Always validate the corpus before use
- Read manifest before processing texts
- Handle missing files gracefully
- Preserve metadata when chunking texts
- Use text IDs for stable references
- Pin to specific versions in production
- Check CHANGELOG when updating

### DON'T:
- Don't assume all texts are complete works (check metadata)
- Don't modify source files (use copies for processing)
- Don't ignore license information in metadata
- Don't use floating references to `main` branch in production
- Don't skip validation step
- Don't assume uniform text structure across all works

---

## Integration with Ignaria System

### Corpus Role in Ignaria Architecture

```
Ignaria Application
├── Agent Layer (reasoning, response generation)
├── Policy Layer (theological guardrails)
└── Retrieval Layer (RAG)
    └── Ignaria Corpus ← This repository
```

### Typical RAG Workflow

1. **Ingestion:** Load corpus, chunk texts, create embeddings
2. **Retrieval:** Query embeddings, retrieve relevant passages
3. **Context:** Augment prompts with retrieved text + metadata
4. **Attribution:** Track sources back to corpus IDs

### Metadata in RAG Context

Include in retrieved chunks:
- Text ID
- Author name (precise attribution for anthology sections)
- Work title
- Historical period
- Genre/category
- Volume title (for anthology sections)
- Section notes (if applicable)

This enables:
- Precise source attribution (including multi-author volumes)
- Multi-source corroboration across Church Fathers
- Filtering by type/period/author
- Theological context awareness
- Accurate citations for anthology works

---

## Maintenance and Updates

### When Corpus Updates

The application should:
1. Check CHANGELOG for breaking changes
2. Re-validate the corpus
3. Regenerate embeddings if texts changed
4. Update text index

### Reporting Issues

If you detect issues programmatically:
- Orphaned files
- Validation failures
- Encoding errors
- Missing metadata

Report via GitHub Issues with details from validation report.

---

## Quick Reference: Essential Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `manifest.yaml` | Canonical text list | Always, first |
| `sources/{id}.txt` | Text content | When processing texts |
| `sources/{id}.meta.yaml` | Detailed metadata | For rich context |
| `CHANGELOG.md` | Version history | Before updating |
| `scripts/validate.py` | Validation tool | Before use, after updates |

---

## Support and Documentation

- **Repository:** https://github.com/flaremark/ignaria-corpus
- **Issues:** https://github.com/flaremark/ignaria-corpus/issues
- **Human Documentation:** See README.md
- **Validation:** Run `python scripts/validate.py --help`

---

## Changelog Summary

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

**Current Version:** 2.0.0
**Last Updated:** 2025-10-15
**Text Count:** 37 active texts (Church Fathers collection)
**NEW in v2.0:** Anthology section metadata for 14 multi-author volumes (completion in progress)

---

*This guide is maintained for automated systems. For human-readable documentation, see README.md*
