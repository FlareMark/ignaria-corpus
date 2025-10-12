# Changelog

All notable changes to the Ignaria Corpus will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
