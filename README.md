# Ignaria Corpus

A curated collection of classical philosophical and theological texts for study and analysis.

## Overview

This corpus contains carefully selected works from major philosophical and theological traditions, formatted for computational analysis and scholarly research.

**This repository contains the public tier** of the Ignaria Corpus - classical works in the public domain. Additional curated collections and premium features are available through the Ignaria platform. See [docs/CORPUS_TIERS.md](docs/CORPUS_TIERS.md) for details.

## Structure

- `manifest.yaml` - Canonical list of all texts in the corpus
- `sources/` - Source text files and their metadata
- `scripts/` - Utilities for downloading, validating, and cleaning texts
- `CHANGELOG.md` - Track additions and removals

## Usage

The corpus is designed for:
- Text analysis and computational linguistics research
- Philosophical and theological study
- Educational purposes
- Academic research

## Documentation

- [SYSTEM_GUIDE.md](SYSTEM_GUIDE.md) - Technical integration guide for AI systems
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute to the corpus
- [docs/CORPUS_TIERS.md](docs/CORPUS_TIERS.md) - Information about corpus tiers
- [CHANGELOG.md](CHANGELOG.md) - Version history

## Scripts

Set up your development environment:
```bash
./setup.sh
```

Available utilities:
- `validate.py` - Validate text integrity and format
- `download.py` - Download texts from various sources
- `clean.py` - Clean and standardize text formatting

## Contributing

Contributions to the public corpus are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Text selection criteria
- Metadata requirements
- Submission process
- Review workflow

## License

This repository uses a dual license structure:
- **Texts:** Public domain (CC0)
- **Scripts:** MIT License
- **Documentation:** CC BY 4.0

See [LICENSE](LICENSE) for details.
