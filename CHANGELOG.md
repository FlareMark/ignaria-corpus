# Changelog

All notable changes to the Ignaria Corpus will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.2.0] - 2025-10-17

### Added - Complete Bible Collection
- **Septuagint (LXX)** - Greek Old Testament (Rahlfs 1935 edition)
  - 54 books including deuterocanonical texts
  - Complete Greek OT with 28,861 verses
  - Morphological analysis preserved from source
  - 6.8 MB of Greek biblical text
- Enhanced Bible coverage now includes:
  - King James Version (English OT + NT)
  - SBLGNT (Greek NT)
  - LXX Septuagint (Greek OT + deuterocanonical)
- Comprehensive metadata for all 54 LXX books with:
  - Composition dates and author attribution
  - Geographic origins
  - Genre classifications
  - Notes on deuterocanonical status

### Infrastructure
- scripts/consolidate-lxx.py: Extract and consolidate LXX from CSV format
- scripts/generate-lxx-metadata.py: Generate complete metadata for 54 books
- BIBLE-LXX.txt: Consolidated Greek Old Testament text
- BIBLE-LXX.meta.yaml: Complete anthology metadata

### Statistics
- Total texts: 40 (increased from 39)
- Bible texts: 3 complete volumes (KJV, SBLGNT, LXX)
- Total biblical books: 147 (66 KJV + 27 SBLGNT + 54 LXX)
- Greek biblical texts: 81 books (27 NT + 54 OT)

## [2.1.0] - 2025-10-17

### Added - Initial Bible Integration
- **King James Version (KJV)** - Complete English Bible
  - 66 books (39 OT + 27 NT)
  - 31,102 verses from Project Gutenberg
  - 4.1 MB of biblical text
- **SBLGNT** - Society of Biblical Literature Greek New Testament
  - 27 books of Greek NT
  - 7,957 verses with verse-level precision
  - 1.7 MB of Greek text
- Comprehensive metadata for all 93 biblical books with:
  - Composition dates and author attribution
  - Geographic origins
  - Genre classifications

### Infrastructure
- scripts/consolidate-sblgnt.py: Consolidate 27 separate SBLGNT files
- scripts/generate-bible-metadata.py: Auto-generate metadata for 93 books
- Updated manifest.yaml to version 2.1.0 with Bible entries
- New categories: biblical, old-testament, new-testament, greek-texts

### Statistics
- Total texts: 39 (increased from 37)
- Total volume: ~136 MB (increased from ~130 MB)

## [2.0.0] - 2025-10-12

### Added - Major Corpus Expansion
- Complete Early Church Fathers collection (37 volumes):
  - **Ante-Nicene Fathers** (9 volumes): Apostolic Fathers through 3rd century writers
    - Vol. I: Apostolic Fathers with Justin Martyr and Irenaeus
    - Vol. II: Fathers of the Second Century
    - Vol. III-IX: Tertullian, Origen, Cyprian, and other early Christian writers
  - **Nicene and Post-Nicene Fathers, Series I** (14 volumes):
    - Vol. I-VIII: Complete works of Augustine of Hippo
    - Vol. IX-XIV: Complete works of John Chrysostom
  - **Nicene and Post-Nicene Fathers, Series II** (14 volumes):
    - Church historians: Eusebius, Socrates, Sozomen, Theodoret
    - Greek Fathers: Athanasius, Gregory of Nyssa, Basil, Cyril of Jerusalem, Gregory Nazianzen
    - Latin Fathers: Jerome, Ambrose, Hilary of Poitiers
    - Monastic writers: John Cassian, Sulpitius Severus, Vincent of Lerins
    - Popes: Leo the Great, Gregory the Great
    - Eastern writers: Ephrem the Syrian, Aphrahat, John of Damascus
    - The Seven Ecumenical Councils
- Comprehensive metadata for all 37 volumes with detailed historical information
- Automated metadata generation script
- New category system for organizing texts by period, author, and series

### Enhanced
- Expanded manifest.yaml to v2.0.0 with all new texts
- Updated corpus description to reflect comprehensive nature
- Added series-based categories (ante-nicene, nicene-post-nicene-1, nicene-post-nicene-2)
- Added author-specific categories (augustine, chrysostom)
- Enhanced patristic category with complete early church coverage

### Infrastructure
- Created generate-church-fathers-metadata.py for automated metadata generation
- Standardized file naming conventions across all volumes
- Updated documentation to reference expanded collection

### Statistics
- Total texts: 39 (increased from 2)
- Total volume: ~130MB of theological texts
- Time period coverage: 1st century AD through 8th century AD
- Languages: Greek and Latin (English translations)
- Number of authors: 50+ early church fathers and theologians

## [1.0.0] - 2024-01-01

### Added
- Initial release of Ignaria Corpus
- README.md with project documentation
- manifest.yaml as canonical list of texts
- CHANGELOG.md for tracking changes
- Scripts directory with utility tools
- Sources directory with initial texts:
  - Augustine's Confessions (sources/augustine-confessions.txt)
  - Aquinas' Summa Theologica (sources/aquinas-summa.txt)
  - Corresponding metadata files (.meta.yaml)

### Infrastructure
- Project structure following scholarly text corpus standards
- YAML-based metadata format
- Python utilities for corpus management
