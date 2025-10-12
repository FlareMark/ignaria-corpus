# Contributing to Ignaria Corpus

Thank you for your interest in contributing to the Ignaria Corpus! This document provides guidelines for contributing texts, metadata, and improvements to the corpus.

## Table of Contents

- [How to Contribute](#how-to-contribute)
- [Adding New Texts](#adding-new-texts)
- [Improving Metadata](#improving-metadata)
- [Reporting Issues](#reporting-issues)
- [Code Contributions](#code-contributions)
- [Review Process](#review-process)

## How to Contribute

### Types of Contributions

1. **Text Additions:** Propose new texts for inclusion
2. **Metadata Improvements:** Enhance existing text metadata
3. **Text Corrections:** Fix errors or improve text quality
4. **Tooling:** Improve scripts and utilities
5. **Documentation:** Improve guides and documentation

## Adding New Texts

### Selection Criteria

Texts should meet the following criteria:

- **Relevance:** Classical Christian theology or philosophy
- **Historical Significance:** Recognized importance in the tradition
- **Quality:** Reliable translation or edition
- **Licensing:** Public domain or permission obtained

### Process

1. **Check Existing Issues:** See if the text is already proposed
2. **Open an Issue:** Propose the text with justification
3. **Wait for Approval:** Curators will review the proposal
4. **Prepare the Text:**
   - Obtain a high-quality source
   - Clean and format according to guidelines
   - Create metadata file
5. **Submit Pull Request:** Include text and metadata

### Text Formatting Requirements

- **Encoding:** UTF-8 only
- **Line Endings:** Unix (LF)
- **Format:** Plain text (.txt)
- **Structure:** Preserve original structure (books, chapters, sections)
- **Cleanliness:** Remove page numbers, headers, footers
- **Attribution:** Include source information in metadata

### Required Metadata

Each text must have a `.meta.yaml` file with:

```yaml
text_info:
  id: "unique-text-id"
  title: "Full Title"
  author: "Author Name"

publication:
  original_language: "Language"
  original_date: "Date or Range"
  period: "Historical Period"
  genre: "Genre/Type"

content:
  structure: "Description of structure"
  themes: [list of major themes]

sources:
  edition: "Edition information"
  translator: "Translator name"
  license: "License or rights status"

technical:
  encoding: "UTF-8"
  format: "Plain text"
  line_endings: "Unix (LF)"
  created: "YYYY-MM-DD"
  last_modified: "YYYY-MM-DD"
```

### Pull Request Template

```markdown
## New Text Proposal

**Text:** [Title]
**Author:** [Author Name]
**Period:** [Historical Period]

### Justification
[Why this text should be included]

### Source
- Edition: [Edition details]
- Translator: [If applicable]
- Source URL: [Where obtained]
- License: [Public domain / Permission obtained]

### Checklist
- [ ] Text is properly formatted (UTF-8, LF line endings)
- [ ] Metadata file created
- [ ] manifest.yaml updated
- [ ] CHANGELOG.md updated
- [ ] Scripts validated (`python scripts/validate.py`)
- [ ] No validation errors
```

## Improving Metadata

### What to Improve

- Add missing cataloging identifiers (ISBN, LOC, etc.)
- Enhance thematic analysis
- Add cross-references to related texts
- Improve source attribution
- Add translator information
- Include more contextual notes

### Process

1. **Fork the repository**
2. **Edit the .meta.yaml file** for the text
3. **Validate:** Run `python scripts/validate.py`
4. **Submit Pull Request** with clear description

## Reporting Issues

### What to Report

- Text encoding errors
- Validation failures
- Missing or incorrect metadata
- Broken scripts
- Documentation errors

### How to Report

Open an issue with:
- **Clear title**
- **Description of the problem**
- **Steps to reproduce** (if applicable)
- **Expected vs. actual behavior**
- **Validation report** (if relevant)

## Code Contributions

### Script Improvements

Contributions to scripts are welcome:

- Bug fixes
- Performance improvements
- New features
- Better error handling
- Additional validation checks

### Development Setup

```bash
# Clone the repository
git clone https://github.com/flaremark/ignaria-corpus
cd ignaria-corpus

# Install dependencies
pip install -r requirements.txt

# Run validation
python scripts/validate.py
```

### Code Style

- Python 3.8+ compatibility
- PEP 8 style guidelines
- Type hints where appropriate
- Comprehensive docstrings
- Error handling

### Testing

Before submitting:

```bash
# Validate the corpus
python scripts/validate.py

# Test on sample data
python scripts/clean.py --file sources/sample.txt --preview
python scripts/download.py --list-sources
```

## Review Process

### Timeline

- **Initial Response:** Within 1 week
- **Text Review:** 2-4 weeks (involves scholarly review)
- **Code Review:** 1-2 weeks
- **Metadata Updates:** 1 week

### Reviewers

- **Text Curation:** Theologians and scholars
- **Code Changes:** Repository maintainers
- **Metadata:** Subject matter experts

### Approval Criteria

**For Texts:**
- Meets selection criteria
- Proper licensing/permissions
- High-quality source
- Complete metadata
- Passes validation

**For Code:**
- Functionality works as intended
- No breaking changes (or properly documented)
- Follows code style
- Includes tests if applicable

**For Metadata:**
- Accurate information
- Follows schema
- Enhances usability

## Communication

### Where to Discuss

- **GitHub Issues:** For specific problems or proposals
- **Pull Requests:** For code/content review
- **Discussions:** For general questions and ideas

### Code of Conduct

- Be respectful and constructive
- Focus on the content, not the person
- Acknowledge different perspectives
- Scholarly disagreement is welcome

## License Agreement

By contributing, you agree that:

- Text contributions will be in the public domain (CC0) or clearly licensed
- Code contributions will be licensed under MIT
- Documentation contributions will be licensed under CC BY 4.0

## Questions?

If you have questions about contributing, please:

1. Check existing documentation
2. Search closed issues
3. Open a new issue with the `question` label

Thank you for helping build a valuable resource for theological research and AI!
