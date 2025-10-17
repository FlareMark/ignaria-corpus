#!/usr/bin/env python3
"""
Generate metadata files for Bible volumes (KJV and SBLGNT).

This script creates complete .meta.yaml files with:
- All 66 books for KJV (OT + NT)
- All 27 books for SBLGNT (NT only)
- Temporal metadata (composition dates)
- Author attribution
- Geographic information
"""

import yaml
from pathlib import Path

# Biblical book metadata with authors, dates, and locations
KJV_BOOKS = [
    # OLD TESTAMENT
    # Torah/Pentateuch
    {"file_marker": "The First Book of Moses: Called Genesis", "author": "Moses", "title": "Genesis", "year": -1400, "uncertainty": "high", "location": "Sinai", "testament": "OT", "genre": "Law"},
    {"file_marker": "The Second Book of Moses: Called Exodus", "author": "Moses", "title": "Exodus", "year": -1400, "uncertainty": "high", "location": "Sinai", "testament": "OT", "genre": "Law"},
    {"file_marker": "The Third Book of Moses: Called Leviticus", "author": "Moses", "title": "Leviticus", "year": -1400, "uncertainty": "high", "location": "Sinai", "testament": "OT", "genre": "Law"},
    {"file_marker": "The Fourth Book of Moses: Called Numbers", "author": "Moses", "title": "Numbers", "year": -1400, "uncertainty": "high", "location": "Sinai", "testament": "OT", "genre": "Law"},
    {"file_marker": "The Fifth Book of Moses: Called Deuteronomy", "author": "Moses", "title": "Deuteronomy", "year": -1400, "uncertainty": "high", "location": "Moab", "testament": "OT", "genre": "Law"},

    # Historical Books
    {"file_marker": "The Book of Joshua", "author": "Joshua", "title": "Joshua", "year": -1350, "uncertainty": "high", "location": "Canaan", "testament": "OT", "genre": "History"},
    {"file_marker": "The Book of Judges", "author": "Samuel", "title": "Judges", "year": -1050, "uncertainty": "high", "location": "Israel", "testament": "OT", "genre": "History"},
    {"file_marker": "The Book of Ruth", "author": "Samuel", "title": "Ruth", "year": -1050, "uncertainty": "high", "location": "Israel", "testament": "OT", "genre": "History"},
    {"file_marker": "The First Book of Samuel", "author": "Samuel", "title": "1 Samuel", "year": -1000, "uncertainty": "high", "location": "Israel", "testament": "OT", "genre": "History"},
    {"file_marker": "The Second Book of Samuel", "author": "Samuel", "title": "2 Samuel", "year": -950, "uncertainty": "high", "location": "Israel", "testament": "OT", "genre": "History"},
    {"file_marker": "The First Book of the Kings", "author": "Jeremiah", "title": "1 Kings", "year": -550, "uncertainty": "high", "location": "Jerusalem", "testament": "OT", "genre": "History"},
    {"file_marker": "The Second Book of the Kings", "author": "Jeremiah", "title": "2 Kings", "year": -550, "uncertainty": "high", "location": "Jerusalem", "testament": "OT", "genre": "History"},
    {"file_marker": "The First Book of the Chronicles", "author": "Ezra", "title": "1 Chronicles", "year": -450, "uncertainty": "medium", "location": "Jerusalem", "testament": "OT", "genre": "History"},
    {"file_marker": "The Second Book of the Chronicles", "author": "Ezra", "title": "2 Chronicles", "year": -450, "uncertainty": "medium", "location": "Jerusalem", "testament": "OT", "genre": "History"},
    {"file_marker": "Ezra", "author": "Ezra", "title": "Ezra", "year": -450, "uncertainty": "medium", "location": "Jerusalem", "testament": "OT", "genre": "History"},
    {"file_marker": "The Book of Nehemiah", "author": "Nehemiah", "title": "Nehemiah", "year": -430, "uncertainty": "medium", "location": "Jerusalem", "testament": "OT", "genre": "History"},
    {"file_marker": "The Book of Esther", "author": "Mordecai", "title": "Esther", "year": -450, "uncertainty": "medium", "location": "Persia", "testament": "OT", "genre": "History"},

    # Wisdom Literature
    {"file_marker": "The Book of Job", "author": "Unknown", "title": "Job", "year": -1500, "uncertainty": "high", "location": "Unknown", "testament": "OT", "genre": "Wisdom"},
    {"file_marker": "The Book of Psalms", "author": "David & Others", "title": "Psalms", "year": -1000, "uncertainty": "high", "location": "Jerusalem", "testament": "OT", "genre": "Wisdom"},
    {"file_marker": "The Proverbs", "author": "Solomon", "title": "Proverbs", "year": -950, "uncertainty": "medium", "location": "Jerusalem", "testament": "OT", "genre": "Wisdom"},
    {"file_marker": "Ecclesiastes", "author": "Solomon", "title": "Ecclesiastes", "year": -935, "uncertainty": "medium", "location": "Jerusalem", "testament": "OT", "genre": "Wisdom"},
    {"file_marker": "The Song of Solomon", "author": "Solomon", "title": "Song of Solomon", "year": -950, "uncertainty": "medium", "location": "Jerusalem", "testament": "OT", "genre": "Wisdom"},

    # Major Prophets
    {"file_marker": "The Book of the Prophet Isaiah", "author": "Isaiah", "title": "Isaiah", "year": -700, "uncertainty": "medium", "location": "Jerusalem", "testament": "OT", "genre": "Prophecy"},
    {"file_marker": "The Book of the Prophet Jeremiah", "author": "Jeremiah", "title": "Jeremiah", "year": -600, "uncertainty": "low", "location": "Jerusalem", "testament": "OT", "genre": "Prophecy"},
    {"file_marker": "The Lamentations of Jeremiah", "author": "Jeremiah", "title": "Lamentations", "year": -586, "uncertainty": "low", "location": "Jerusalem", "testament": "OT", "genre": "Prophecy"},
    {"file_marker": "The Book of the Prophet Ezekiel", "author": "Ezekiel", "title": "Ezekiel", "year": -580, "uncertainty": "low", "location": "Babylon", "testament": "OT", "genre": "Prophecy"},
    {"file_marker": "The Book of Daniel", "author": "Daniel", "title": "Daniel", "year": -530, "uncertainty": "high", "location": "Babylon", "testament": "OT", "genre": "Prophecy"},

    # Minor Prophets
    {"file_marker": "Hosea", "author": "Hosea", "title": "Hosea", "year": -750, "uncertainty": "medium", "location": "Israel", "testament": "OT", "genre": "Prophecy"},
    {"file_marker": "Joel", "author": "Joel", "title": "Joel", "year": -830, "uncertainty": "high", "location": "Judah", "testament": "OT", "genre": "Prophecy"},
    {"file_marker": "Amos", "author": "Amos", "title": "Amos", "year": -760, "uncertainty": "low", "location": "Israel", "testament": "OT", "genre": "Prophecy"},
    {"file_marker": "Obadiah", "author": "Obadiah", "title": "Obadiah", "year": -840, "uncertainty": "high", "location": "Judah", "testament": "OT", "genre": "Prophecy"},
    {"file_marker": "Jonah", "author": "Jonah", "title": "Jonah", "year": -760, "uncertainty": "medium", "location": "Israel", "testament": "OT", "genre": "Prophecy"},
    {"file_marker": "Micah", "author": "Micah", "title": "Micah", "year": -700, "uncertainty": "medium", "location": "Judah", "testament": "OT", "genre": "Prophecy"},
    {"file_marker": "Nahum", "author": "Nahum", "title": "Nahum", "year": -650, "uncertainty": "medium", "location": "Judah", "testament": "OT", "genre": "Prophecy"},
    {"file_marker": "Habakkuk", "author": "Habakkuk", "title": "Habakkuk", "year": -607, "uncertainty": "medium", "location": "Judah", "testament": "OT", "genre": "Prophecy"},
    {"file_marker": "Zephaniah", "author": "Zephaniah", "title": "Zephaniah", "year": -630, "uncertainty": "medium", "location": "Judah", "testament": "OT", "genre": "Prophecy"},
    {"file_marker": "Haggai", "author": "Haggai", "title": "Haggai", "year": -520, "uncertainty": "low", "location": "Jerusalem", "testament": "OT", "genre": "Prophecy"},
    {"file_marker": "Zechariah", "author": "Zechariah", "title": "Zechariah", "year": -520, "uncertainty": "low", "location": "Jerusalem", "testament": "OT", "genre": "Prophecy"},
    {"file_marker": "Malachi", "author": "Malachi", "title": "Malachi", "year": -430, "uncertainty": "medium", "location": "Jerusalem", "testament": "OT", "genre": "Prophecy"},

    # NEW TESTAMENT
    # Gospels
    {"file_marker": "The Gospel According to Saint Matthew", "author": "Matthew", "title": "Matthew", "year": 70, "uncertainty": "medium", "location": "Palestine", "testament": "NT", "genre": "Gospel"},
    {"file_marker": "The Gospel According to Saint Mark", "author": "Mark", "title": "Mark", "year": 68, "uncertainty": "medium", "location": "Rome", "testament": "NT", "genre": "Gospel"},
    {"file_marker": "The Gospel According to Saint Luke", "author": "Luke", "title": "Luke", "year": 62, "uncertainty": "medium", "location": "Rome", "testament": "NT", "genre": "Gospel"},
    {"file_marker": "The Gospel According to Saint John", "author": "John", "title": "John", "year": 90, "uncertainty": "low", "location": "Ephesus", "testament": "NT", "genre": "Gospel"},

    # Acts
    {"file_marker": "The Acts of the Apostles", "author": "Luke", "title": "Acts", "year": 62, "uncertainty": "medium", "location": "Rome", "testament": "NT", "genre": "History"},

    # Paul's Epistles
    {"file_marker": "The Epistle of Paul the Apostle to the Romans", "author": "Paul", "title": "Romans", "year": 57, "uncertainty": "low", "location": "Corinth", "testament": "NT", "genre": "Epistle"},
    {"file_marker": "The First Epistle of Paul the Apostle to the Corinthians", "author": "Paul", "title": "1 Corinthians", "year": 55, "uncertainty": "low", "location": "Ephesus", "testament": "NT", "genre": "Epistle"},
    {"file_marker": "The Second Epistle of Paul the Apostle to the Corinthians", "author": "Paul", "title": "2 Corinthians", "year": 56, "uncertainty": "low", "location": "Macedonia", "testament": "NT", "genre": "Epistle"},
    {"file_marker": "The Epistle of Paul the Apostle to the Galatians", "author": "Paul", "title": "Galatians", "year": 49, "uncertainty": "medium", "location": "Antioch", "testament": "NT", "genre": "Epistle"},
    {"file_marker": "The Epistle of Paul the Apostle to the Ephesians", "author": "Paul", "title": "Ephesians", "year": 60, "uncertainty": "low", "location": "Rome", "testament": "NT", "genre": "Epistle"},
    {"file_marker": "The Epistle of Paul the Apostle to the Philippians", "author": "Paul", "title": "Philippians", "year": 62, "uncertainty": "low", "location": "Rome", "testament": "NT", "genre": "Epistle"},
    {"file_marker": "The Epistle of Paul the Apostle to the Colossians", "author": "Paul", "title": "Colossians", "year": 60, "uncertainty": "low", "location": "Rome", "testament": "NT", "genre": "Epistle"},
    {"file_marker": "The First Epistle of Paul the Apostle to the Thessalonians", "author": "Paul", "title": "1 Thessalonians", "year": 51, "uncertainty": "low", "location": "Corinth", "testament": "NT", "genre": "Epistle"},
    {"file_marker": "The Second Epistle of Paul the Apostle to the Thessalonians", "author": "Paul", "title": "2 Thessalonians", "year": 51, "uncertainty": "low", "location": "Corinth", "testament": "NT", "genre": "Epistle"},
    {"file_marker": "The First Epistle of Paul the Apostle to Timothy", "author": "Paul", "title": "1 Timothy", "year": 64, "uncertainty": "medium", "location": "Macedonia", "testament": "NT", "genre": "Epistle"},
    {"file_marker": "The Second Epistle of Paul the Apostle to Timothy", "author": "Paul", "title": "2 Timothy", "year": 67, "uncertainty": "medium", "location": "Rome", "testament": "NT", "genre": "Epistle"},
    {"file_marker": "The Epistle of Paul the Apostle to Titus", "author": "Paul", "title": "Titus", "year": 64, "uncertainty": "medium", "location": "Macedonia", "testament": "NT", "genre": "Epistle"},
    {"file_marker": "The Epistle of Paul the Apostle to Philemon", "author": "Paul", "title": "Philemon", "year": 60, "uncertainty": "low", "location": "Rome", "testament": "NT", "genre": "Epistle"},

    # General Epistles
    {"file_marker": "The Epistle of Paul the Apostle to the Hebrews", "author": "Unknown", "title": "Hebrews", "year": 68, "uncertainty": "medium", "location": "Unknown", "testament": "NT", "genre": "Epistle"},
    {"file_marker": "The General Epistle of James", "author": "James", "title": "James", "year": 48, "uncertainty": "medium", "location": "Jerusalem", "testament": "NT", "genre": "Epistle"},
    {"file_marker": "The First Epistle General of Peter", "author": "Peter", "title": "1 Peter", "year": 64, "uncertainty": "medium", "location": "Rome", "testament": "NT", "genre": "Epistle"},
    {"file_marker": "The Second Epistle General of Peter", "author": "Peter", "title": "2 Peter", "year": 66, "uncertainty": "medium", "location": "Rome", "testament": "NT", "genre": "Epistle"},
    {"file_marker": "The First Epistle General of John", "author": "John", "title": "1 John", "year": 90, "uncertainty": "low", "location": "Ephesus", "testament": "NT", "genre": "Epistle"},
    {"file_marker": "The Second Epistle General of John", "author": "John", "title": "2 John", "year": 90, "uncertainty": "low", "location": "Ephesus", "testament": "NT", "genre": "Epistle"},
    {"file_marker": "The Third Epistle General of John", "author": "John", "title": "3 John", "year": 90, "uncertainty": "low", "location": "Ephesus", "testament": "NT", "genre": "Epistle"},
    {"file_marker": "The General Epistle of Jude", "author": "Jude", "title": "Jude", "year": 70, "uncertainty": "medium", "location": "Unknown", "testament": "NT", "genre": "Epistle"},

    # Revelation
    {"file_marker": "The Revelation of Saint John the Divine", "author": "John", "title": "Revelation", "year": 95, "uncertainty": "low", "location": "Patmos", "testament": "NT", "genre": "Apocalyptic"},
]

# SBLGNT books (Greek NT only)
SBLGNT_BOOKS = [
    {"greek_marker": "ΚΑΤΑ ΜΑΘΘΑΙΟΝ", "author": "Matthew", "title": "Matthew", "year": 70, "uncertainty": "medium", "location": "Palestine"},
    {"greek_marker": "ΚΑΤΑ ΜΑΡΚΟΝ", "author": "Mark", "title": "Mark", "year": 68, "uncertainty": "medium", "location": "Rome"},
    {"greek_marker": "ΚΑΤΑ ΛΟΥΚΑΝ", "author": "Luke", "title": "Luke", "year": 62, "uncertainty": "medium", "location": "Rome"},
    {"greek_marker": "ΚΑΤΑ ΙΩΑΝΝΗΝ", "author": "John", "title": "John", "year": 90, "uncertainty": "low", "location": "Ephesus"},
    {"greek_marker": "ΠΡΑΞΕΙΣ ΑΠΟΣΤΟΛΩΝ", "author": "Luke", "title": "Acts", "year": 62, "uncertainty": "medium", "location": "Rome"},
    {"greek_marker": "ΠΡΟΣ ΡΩΜΑΙΟΥΣ", "author": "Paul", "title": "Romans", "year": 57, "uncertainty": "low", "location": "Corinth"},
    {"greek_marker": "ΠΡΟΣ ΚΟΡΙΝΘΙΟΥΣ Α", "author": "Paul", "title": "1 Corinthians", "year": 55, "uncertainty": "low", "location": "Ephesus"},
    {"greek_marker": "ΠΡΟΣ ΚΟΡΙΝΘΙΟΥΣ Β", "author": "Paul", "title": "2 Corinthians", "year": 56, "uncertainty": "low", "location": "Macedonia"},
    {"greek_marker": "ΠΡΟΣ ΓΑΛΑΤΑΣ", "author": "Paul", "title": "Galatians", "year": 49, "uncertainty": "medium", "location": "Antioch"},
    {"greek_marker": "ΠΡΟΣ ΕΦΕΣΙΟΥΣ", "author": "Paul", "title": "Ephesians", "year": 60, "uncertainty": "low", "location": "Rome"},
    {"greek_marker": "ΠΡΟΣ ΦΙΛΙΠΠΗΣΙΟΥΣ", "author": "Paul", "title": "Philippians", "year": 62, "uncertainty": "low", "location": "Rome"},
    {"greek_marker": "ΠΡΟΣ ΚΟΛΟΣΣΑΕΙΣ", "author": "Paul", "title": "Colossians", "year": 60, "uncertainty": "low", "location": "Rome"},
    {"greek_marker": "ΠΡΟΣ ΘΕΣΣΑΛΟΝΙΚΕΙΣ Α", "author": "Paul", "title": "1 Thessalonians", "year": 51, "uncertainty": "low", "location": "Corinth"},
    {"greek_marker": "ΠΡΟΣ ΘΕΣΣΑΛΟΝΙΚΕΙΣ Β", "author": "Paul", "title": "2 Thessalonians", "year": 51, "uncertainty": "low", "location": "Corinth"},
    {"greek_marker": "ΠΡΟΣ ΤΙΜΟΘΕΟΝ Α", "author": "Paul", "title": "1 Timothy", "year": 64, "uncertainty": "medium", "location": "Macedonia"},
    {"greek_marker": "ΠΡΟΣ ΤΙΜΟΘΕΟΝ Β", "author": "Paul", "title": "2 Timothy", "year": 67, "uncertainty": "medium", "location": "Rome"},
    {"greek_marker": "ΠΡΟΣ ΤΙΤΟΝ", "author": "Paul", "title": "Titus", "year": 64, "uncertainty": "medium", "location": "Macedonia"},
    {"greek_marker": "ΠΡΟΣ ΦΙΛΗΜΟΝΑ", "author": "Paul", "title": "Philemon", "year": 60, "uncertainty": "low", "location": "Rome"},
    {"greek_marker": "ΠΡΟΣ ΕΒΡΑΙΟΥΣ", "author": "Unknown", "title": "Hebrews", "year": 68, "uncertainty": "medium", "location": "Unknown"},
    {"greek_marker": "ΙΑΚΩΒΟΥ", "author": "James", "title": "James", "year": 48, "uncertainty": "medium", "location": "Jerusalem"},
    {"greek_marker": "ΠΕΤΡΟΥ Α", "author": "Peter", "title": "1 Peter", "year": 64, "uncertainty": "medium", "location": "Rome"},
    {"greek_marker": "ΠΕΤΡΟΥ Β", "author": "Peter", "title": "2 Peter", "year": 66, "uncertainty": "medium", "location": "Rome"},
    {"greek_marker": "ΙΩΑΝΝΟΥ Α", "author": "John", "title": "1 John", "year": 90, "uncertainty": "low", "location": "Ephesus"},
    {"greek_marker": "ΙΩΑΝΝΟΥ Β", "author": "John", "title": "2 John", "year": 90, "uncertainty": "low", "location": "Ephesus"},
    {"greek_marker": "ΙΩΑΝΝΟΥ Γ", "author": "John", "title": "3 John", "year": 90, "uncertainty": "low", "location": "Ephesus"},
    {"greek_marker": "ΙΟΥΔΑ", "author": "Jude", "title": "Jude", "year": 70, "uncertainty": "medium", "location": "Unknown"},
    {"greek_marker": "ΑΠΟΚΑΛΥΨΙΣ ΙΩΑΝΝΟΥ", "author": "John", "title": "Revelation", "year": 95, "uncertainty": "low", "location": "Patmos"},
]


def generate_kjv_metadata():
    """Generate BIBLE-KJV.meta.yaml with all 66 books."""

    sections = []
    for book in KJV_BOOKS:
        section = {
            'author': book['author'],
            'title': book['title'],
            'start_marker': book['file_marker'],
            'composition_year': book['year'],
            'composition_uncertainty': book['uncertainty'],
            'author_region': 'Eastern',
            'author_location': book['location'],
            'testament': book['testament'],
            'genre': book['genre'],
        }
        sections.append(section)

    metadata = {
        'text_info': {
            'id': 'bible-kjv',
            'title': 'The Holy Bible - King James Version',
            'authors': ['Multiple Biblical Authors'],
            'series': 'Biblical Texts',
            'volume': 'KJV',
            'is_anthology': True,
            'sections': sections,
        },
        'publication': {
            'original_language': 'Hebrew, Aramaic, Greek (translated to English)',
            'original_date': 'c. 1400 BC - 95 AD',
            'period': 'Biblical Era',
            'genre': 'Sacred Scripture',
            'translation': 'King James Version',
            'translation_date': '1611',
            'translators': ['47 scholars commissioned by King James I'],
        },
        'content': {
            'description': 'Complete Protestant canon in King James English',
            'format': 'Full biblical text with original versification',
            'themes': ['Revelation', 'Covenant', 'Redemption', 'Law and Grace'],
        },
        'sources': {
            'edition': 'King James Version (KJV)',
            'source': 'Project Gutenberg',
            'source_url': 'https://www.gutenberg.org/ebooks/10',
            'license': 'Public Domain',
        },
        'technical': {
            'encoding': 'UTF-8',
            'format': 'Plain text',
            'line_endings': 'Unix (LF)',
            'created': '2025-10-17',
        },
        'cataloging': {
            'canonical_order': True,
            'protestant_canon': True,
            'num_books': 66,
            'old_testament_books': 39,
            'new_testament_books': 27,
        },
    }

    output_file = Path('sources/BIBLE-KJV.meta.yaml')
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(metadata, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"✅ Generated: {output_file}")
    print(f"   Books: {len(sections)} (39 OT + 27 NT)")
    return output_file


def generate_sblgnt_metadata():
    """Generate BIBLE-SBLGNT.meta.yaml with all 27 NT books."""

    sections = []
    for book in SBLGNT_BOOKS:
        section = {
            'author': book['author'],
            'title': book['title'],
            'start_marker': book['greek_marker'],
            'composition_year': book['year'],
            'composition_uncertainty': book['uncertainty'],
            'author_region': 'Eastern',
            'author_location': book['location'],
            'testament': 'NT',
            'original_language': 'Greek',
        }
        sections.append(section)

    metadata = {
        'text_info': {
            'id': 'bible-sblgnt',
            'title': 'The Greek New Testament - SBL Greek New Testament',
            'authors': ['Multiple Biblical Authors'],
            'series': 'Biblical Texts',
            'volume': 'SBLGNT',
            'is_anthology': True,
            'sections': sections,
        },
        'publication': {
            'original_language': 'Koine Greek',
            'original_date': '48-95 AD',
            'period': 'First Century Christianity',
            'genre': 'Sacred Scripture',
            'editors': ['Michael W. Holmes'],
            'publication_date': '2010',
        },
        'content': {
            'description': 'Critical edition of the Greek New Testament',
            'format': 'Greek text with modern punctuation',
            'themes': ['Gospel', 'Apostolic Teaching', 'Early Church'],
        },
        'sources': {
            'edition': 'SBL Greek New Testament (SBLGNT)',
            'source': 'Society of Biblical Literature',
            'source_url': 'https://github.com/LogosBible/SBLGNT',
            'license': 'CC BY 4.0',
        },
        'technical': {
            'encoding': 'UTF-8',
            'format': 'Plain text',
            'line_endings': 'Unix (LF)',
            'created': '2025-10-17',
        },
        'cataloging': {
            'canonical_order': True,
            'protestant_canon': True,
            'num_books': 27,
            'testament': 'New Testament',
        },
    }

    output_file = Path('sources/BIBLE-SBLGNT.meta.yaml')
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(metadata, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"✅ Generated: {output_file}")
    print(f"   Books: {len(sections)} (NT only)")
    return output_file


if __name__ == '__main__':
    print("📖 Generating Bible metadata files...\n")
    generate_kjv_metadata()
    print()
    generate_sblgnt_metadata()
    print("\n✅ Bible metadata generation complete!")
