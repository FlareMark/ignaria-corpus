#!/usr/bin/env python3
"""
Generate metadata files for the complete Church Fathers collection.
Ante-Nicene Fathers (9 volumes) + Nicene and Post-Nicene Fathers Series I & II (28 volumes)
"""

import yaml
from pathlib import Path
from datetime import date

# Metadata for all 37 volumes
CHURCH_FATHERS_METADATA = {
    # Ante-Nicene Fathers (9 volumes)
    "ANF-01": {
        "title": "Ante-Nicene Fathers, Vol. I: The Apostolic Fathers with Justin Martyr and Irenaeus",
        "authors": ["Clement of Rome", "Mathetes", "Polycarp", "Ignatius", "Barnabas", "Papias", "Justin Martyr", "Irenaeus"],
        "period": "Apostolic and Sub-Apostolic Era",
        "date_range": "c. 30-202 AD",
        "description": "The Apostolic Fathers and early apologists"
    },
    "ANF-02": {
        "title": "Ante-Nicene Fathers, Vol. II: Fathers of the Second Century",
        "authors": ["Hermas", "Tatian", "Theophilus", "Athenagoras", "Clement of Alexandria"],
        "period": "Second Century",
        "date_range": "c. 100-215 AD",
        "description": "Greek apologists and Alexandrian theologians"
    },
    "ANF-03": {
        "title": "Ante-Nicene Fathers, Vol. III: Latin Christianity: Its Founder, Tertullian",
        "authors": ["Tertullian"],
        "period": "Late Second/Early Third Century",
        "date_range": "c. 155-240 AD",
        "description": "Tertullian's works in three parts: Apologetic, Anti-Marcion, and Ethical"
    },
    "ANF-04": {
        "title": "Ante-Nicene Fathers, Vol. IV: The Fathers of the Third Century",
        "authors": ["Tertullian", "Minucius Felix", "Commodian", "Origen"],
        "period": "Third Century",
        "date_range": "c. 185-254 AD",
        "description": "Tertullian (Part IV), Latin apologists, and Origen"
    },
    "ANF-05": {
        "title": "Ante-Nicene Fathers, Vol. V: The Fathers of the Third Century",
        "authors": ["Hippolytus", "Cyprian", "Caius", "Novatian"],
        "period": "Third Century",
        "date_range": "c. 170-258 AD",
        "description": "Hippolytus, Cyprian of Carthage, and other third-century writers"
    },
    "ANF-06": {
        "title": "Ante-Nicene Fathers, Vol. VI: The Fathers of the Third Century",
        "authors": ["Gregory Thaumaturgus", "Dionysius the Great", "Julius Africanus", "Anatolius", "Methodius", "Arnobius"],
        "period": "Third Century",
        "date_range": "c. 213-330 AD",
        "description": "Greek and Latin fathers of the later third century"
    },
    "ANF-07": {
        "title": "Ante-Nicene Fathers, Vol. VII: The Fathers of the Third and Fourth Centuries",
        "authors": ["Lactantius", "Venantius", "Asterius", "Victorinus", "Dionysius"],
        "period": "Late Third/Early Fourth Century",
        "date_range": "c. 250-330 AD",
        "description": "Lactantius and other transitional figures, plus Apostolic Teaching and Constitutions"
    },
    "ANF-08": {
        "title": "Ante-Nicene Fathers, Vol. VIII: The Twelve Patriarchs, Excerpts and Epistles, Apocrypha",
        "authors": ["Various"],
        "period": "First-Fourth Centuries",
        "date_range": "c. 100-300 AD",
        "description": "Pseudepigrapha, apocrypha, Clementine literature, and Syriac documents"
    },
    "ANF-09": {
        "title": "Ante-Nicene Fathers, Vol. IX: Recently Discovered Additions to Early Christian Literature",
        "authors": ["Origen", "Tatian", "Various"],
        "period": "Second-Third Centuries",
        "date_range": "c. 150-254 AD",
        "description": "Gospel of Peter, Diatessaron, Origen's Commentaries on John and Matthew"
    },

    # Nicene and Post-Nicene Fathers, Series I (14 volumes - Augustine and Chrysostom)
    "NPNF1-01": {
        "title": "Nicene and Post-Nicene Fathers, Series I, Vol. I: Augustine - Life, Confessions, Letters",
        "authors": ["Augustine of Hippo"],
        "period": "Late Fourth/Early Fifth Century",
        "date_range": "354-430 AD",
        "description": "Prolegomena, Augustine's life and work, Confessions, and selected letters"
    },
    "NPNF1-02": {
        "title": "Nicene and Post-Nicene Fathers, Series I, Vol. II: Augustine - City of God, Christian Doctrine",
        "authors": ["Augustine of Hippo"],
        "period": "Late Fourth/Early Fifth Century",
        "date_range": "354-430 AD",
        "description": "The City of God and On Christian Doctrine"
    },
    "NPNF1-03": {
        "title": "Nicene and Post-Nicene Fathers, Series I, Vol. III: Augustine - On the Holy Trinity, Doctrinal and Moral Treatises",
        "authors": ["Augustine of Hippo"],
        "period": "Late Fourth/Early Fifth Century",
        "date_range": "354-430 AD",
        "description": "On the Holy Trinity and various doctrinal and ethical treatises"
    },
    "NPNF1-04": {
        "title": "Nicene and Post-Nicene Fathers, Series I, Vol. IV: Augustine - Anti-Manichaean and Anti-Donatist Writings",
        "authors": ["Augustine of Hippo"],
        "period": "Late Fourth/Early Fifth Century",
        "date_range": "354-430 AD",
        "description": "Polemical works against Manichaeism and Donatism"
    },
    "NPNF1-05": {
        "title": "Nicene and Post-Nicene Fathers, Series I, Vol. V: Augustine - Anti-Pelagian Writings",
        "authors": ["Augustine of Hippo"],
        "period": "Early Fifth Century",
        "date_range": "354-430 AD",
        "description": "Works on grace, free will, and predestination against Pelagianism"
    },
    "NPNF1-06": {
        "title": "Nicene and Post-Nicene Fathers, Series I, Vol. VI: Augustine - Sermon on the Mount, Harmony of the Gospels, Homilies",
        "authors": ["Augustine of Hippo"],
        "period": "Late Fourth/Early Fifth Century",
        "date_range": "354-430 AD",
        "description": "Biblical exposition and harmonization"
    },
    "NPNF1-07": {
        "title": "Nicene and Post-Nicene Fathers, Series I, Vol. VII: Augustine - Homilies on John and First John, Soliloquies",
        "authors": ["Augustine of Hippo"],
        "period": "Late Fourth/Early Fifth Century",
        "date_range": "354-430 AD",
        "description": "Homilies on the Gospel of John, First Epistle of John, and Soliloquies"
    },
    "NPNF1-08": {
        "title": "Nicene and Post-Nicene Fathers, Series I, Vol. VIII: Augustine - Expositions on the Psalms",
        "authors": ["Augustine of Hippo"],
        "period": "Late Fourth/Early Fifth Century",
        "date_range": "354-430 AD",
        "description": "Complete exposition of the Psalms"
    },
    "NPNF1-09": {
        "title": "Nicene and Post-Nicene Fathers, Series I, Vol. IX: Chrysostom - On the Priesthood, Ascetic Treatises, Homilies",
        "authors": ["John Chrysostom"],
        "period": "Late Fourth/Early Fifth Century",
        "date_range": "c. 347-407 AD",
        "description": "On the Priesthood, ascetic writings, select homilies and letters"
    },
    "NPNF1-10": {
        "title": "Nicene and Post-Nicene Fathers, Series I, Vol. X: Chrysostom - Homilies on Matthew",
        "authors": ["John Chrysostom"],
        "period": "Late Fourth/Early Fifth Century",
        "date_range": "c. 347-407 AD",
        "description": "Complete homilies on the Gospel of Matthew"
    },
    "NPNF1-11": {
        "title": "Nicene and Post-Nicene Fathers, Series I, Vol. XI: Chrysostom - Homilies on Acts and Romans",
        "authors": ["John Chrysostom"],
        "period": "Late Fourth/Early Fifth Century",
        "date_range": "c. 347-407 AD",
        "description": "Homilies on the Acts of the Apostles and the Epistle to the Romans"
    },
    "NPNF1-12": {
        "title": "Nicene and Post-Nicene Fathers, Series I, Vol. XII: Chrysostom - Homilies on First and Second Corinthians",
        "authors": ["John Chrysostom"],
        "period": "Late Fourth/Early Fifth Century",
        "date_range": "c. 347-407 AD",
        "description": "Homilies on Paul's Corinthian epistles"
    },
    "NPNF1-13": {
        "title": "Nicene and Post-Nicene Fathers, Series I, Vol. XIII: Chrysostom - Homilies on Galatians through Philemon",
        "authors": ["John Chrysostom"],
        "period": "Late Fourth/Early Fifth Century",
        "date_range": "c. 347-407 AD",
        "description": "Homilies on Galatians, Ephesians, Philippians, Colossians, Thessalonians, Timothy, Titus, and Philemon"
    },
    "NPNF1-14": {
        "title": "Nicene and Post-Nicene Fathers, Series I, Vol. XIV: Chrysostom - Homilies on John and Hebrews",
        "authors": ["John Chrysostom"],
        "period": "Late Fourth/Early Fifth Century",
        "date_range": "c. 347-407 AD",
        "description": "Homilies on the Gospel of John and the Epistle to the Hebrews"
    },

    # Nicene and Post-Nicene Fathers, Series II (14 volumes - Various Greek and Latin Fathers)
    "NPNF2-01": {
        "title": "Nicene and Post-Nicene Fathers, Series II, Vol. I: Eusebius - Church History, Life of Constantine",
        "authors": ["Eusebius of Caesarea"],
        "period": "Fourth Century",
        "date_range": "c. 260-339 AD",
        "description": "Church History (AD 1-324), Life of Constantine, Oration in Praise of Constantine"
    },
    "NPNF2-02": {
        "title": "Nicene and Post-Nicene Fathers, Series II, Vol. II: Socrates and Sozomenus - Church Histories",
        "authors": ["Socrates Scholasticus", "Sozomen"],
        "period": "Fifth Century",
        "date_range": "c. 380-450 AD",
        "description": "Socrates: Church History (AD 305-438); Sozomenus: Church History (AD 323-425)"
    },
    "NPNF2-03": {
        "title": "Nicene and Post-Nicene Fathers, Series II, Vol. III: Theodoret, Jerome, Gennadius, Rufinus",
        "authors": ["Theodoret", "Jerome", "Gennadius", "Rufinus"],
        "period": "Fourth-Fifth Centuries",
        "date_range": "c. 345-466 AD",
        "description": "Church histories and biographical works"
    },
    "NPNF2-04": {
        "title": "Nicene and Post-Nicene Fathers, Series II, Vol. IV: Athanasius - Select Writings and Letters",
        "authors": ["Athanasius of Alexandria"],
        "period": "Fourth Century",
        "date_range": "c. 296-373 AD",
        "description": "Select works and letters of Athanasius, defender of Nicene orthodoxy"
    },
    "NPNF2-05": {
        "title": "Nicene and Post-Nicene Fathers, Series II, Vol. V: Gregory of Nyssa - Dogmatic Treatises and Letters",
        "authors": ["Gregory of Nyssa"],
        "period": "Fourth Century",
        "date_range": "c. 335-395 AD",
        "description": "Dogmatic treatises, select writings and letters"
    },
    "NPNF2-06": {
        "title": "Nicene and Post-Nicene Fathers, Series II, Vol. VI: Jerome - Letters and Select Works",
        "authors": ["Jerome"],
        "period": "Late Fourth/Early Fifth Century",
        "date_range": "c. 347-420 AD",
        "description": "Jerome's correspondence and selected treatises"
    },
    "NPNF2-07": {
        "title": "Nicene and Post-Nicene Fathers, Series II, Vol. VII: Cyril of Jerusalem and Gregory Nazianzen",
        "authors": ["Cyril of Jerusalem", "Gregory of Nazianzus"],
        "period": "Fourth Century",
        "date_range": "c. 313-390 AD",
        "description": "Cyril's Catechetical Lectures and Gregory's Orations"
    },
    "NPNF2-08": {
        "title": "Nicene and Post-Nicene Fathers, Series II, Vol. VIII: Basil - Letters and Select Works",
        "authors": ["Basil the Great"],
        "period": "Fourth Century",
        "date_range": "c. 330-379 AD",
        "description": "Basil's letters and selected treatises"
    },
    "NPNF2-09": {
        "title": "Nicene and Post-Nicene Fathers, Series II, Vol. IX: Hilary of Poitiers and John of Damascus",
        "authors": ["Hilary of Poitiers", "John of Damascus"],
        "period": "Fourth and Eighth Centuries",
        "date_range": "c. 310-749 AD",
        "description": "Hilary's works on the Trinity and John of Damascus's theological writings"
    },
    "NPNF2-10": {
        "title": "Nicene and Post-Nicene Fathers, Series II, Vol. X: Ambrose - Select Works and Letters",
        "authors": ["Ambrose of Milan"],
        "period": "Fourth Century",
        "date_range": "c. 339-397 AD",
        "description": "Selected works and letters of Ambrose"
    },
    "NPNF2-11": {
        "title": "Nicene and Post-Nicene Fathers, Series II, Vol. XI: Sulpitius Severus, Vincent of Lerins, John Cassian",
        "authors": ["Sulpitius Severus", "Vincent of Lerins", "John Cassian"],
        "period": "Fourth-Fifth Centuries",
        "date_range": "c. 363-435 AD",
        "description": "Historical and monastic writings"
    },
    "NPNF2-12": {
        "title": "Nicene and Post-Nicene Fathers, Series II, Vol. XII: Leo the Great and Gregory the Great (Part I)",
        "authors": ["Leo I", "Gregory I"],
        "period": "Fifth-Sixth Centuries",
        "date_range": "c. 400-604 AD",
        "description": "Letters and select works of two great popes"
    },
    "NPNF2-13": {
        "title": "Nicene and Post-Nicene Fathers, Series II, Vol. XIII: Gregory the Great (Part II), Ephraim Syrus, Aphrahat",
        "authors": ["Gregory I", "Ephrem the Syrian", "Aphrahat"],
        "period": "Fourth-Sixth Centuries",
        "date_range": "c. 306-604 AD",
        "description": "Gregory's continued works and Syriac fathers"
    },
    "NPNF2-14": {
        "title": "Nicene and Post-Nicene Fathers, Series II, Vol. XIV: The Seven Ecumenical Councils",
        "authors": ["Various Church Councils"],
        "period": "Fourth-Eighth Centuries",
        "date_range": "325-787 AD",
        "description": "Proceedings and canons of the seven ecumenical councils"
    }
}

def generate_metadata(volume_id, info):
    """Generate metadata YAML for a single volume."""

    # Determine series
    if volume_id.startswith("ANF"):
        series = "Ante-Nicene Fathers"
        volume_num = int(volume_id.split("-")[1])
        editors = ["Alexander Roberts", "James Donaldson"]
        publication_date = "1867-1873"
    elif volume_id.startswith("NPNF1"):
        series = "Nicene and Post-Nicene Fathers, Series I"
        volume_num = int(volume_id.split("-")[1])
        editors = ["Philip Schaff"]
        publication_date = "1886-1889"
    else:  # NPNF2
        series = "Nicene and Post-Nicene Fathers, Series II"
        volume_num = int(volume_id.split("-")[1])
        editors = ["Philip Schaff", "Henry Wace"]
        publication_date = "1890-1900"

    metadata = {
        "text_info": {
            "id": volume_id.lower(),
            "title": info["title"],
            "authors": info["authors"],
            "series": series,
            "volume": volume_num
        },
        "publication": {
            "original_language": "Greek and Latin (translated to English)",
            "original_date": info["date_range"],
            "period": info["period"],
            "genre": "Patristic Theology",
            "editors": editors,
            "publication_date": publication_date
        },
        "content": {
            "description": info["description"],
            "format": "Complete volume with all treatises, letters, and homilies",
            "themes": [
                "Early Church theology",
                "Patristic exegesis",
                "Doctrinal development",
                "Church history"
            ]
        },
        "sources": {
            "edition": f"{series}, Volume {volume_num}",
            "source": "Christian Classics Ethereal Library (CCEL)",
            "source_url": "https://www.ccel.org/fathers",
            "license": "Public domain",
            "translation_notes": "Historical English translation from 19th century scholarly editions"
        },
        "technical": {
            "encoding": "UTF-8",
            "format": "Plain text",
            "line_endings": "Unix (LF)",
            "created": str(date.today()),
            "last_modified": str(date.today())
        },
        "cataloging": {
            "ccel_id": volume_id.lower(),
            "series_info": f"{series}, Vol. {volume_num}",
            "historical_significance": "Part of the definitive 19th-century collection of early church writings"
        },
        "notes": [
            "Complete volume from the standard English translation of the Church Fathers",
            "Includes scholarly introductions, footnotes, and indices from original editors",
            "Public domain - freely available for study and research",
            f"Part of the comprehensive 38-volume collection of early Christian literature"
        ]
    }

    return metadata

def main():
    """Generate all metadata files."""
    corpus_root = Path(__file__).parent.parent
    sources_dir = corpus_root / "sources"

    print(f"Generating metadata for {len(CHURCH_FATHERS_METADATA)} volumes...")

    for volume_id, info in CHURCH_FATHERS_METADATA.items():
        # Create metadata file
        meta_filename = f"{volume_id}.meta.yaml"
        meta_path = sources_dir / meta_filename

        metadata = generate_metadata(volume_id, info)

        with open(meta_path, 'w', encoding='utf-8') as f:
            yaml.dump(metadata, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        print(f"✓ Created {meta_filename}")

    print(f"\n✅ Generated {len(CHURCH_FATHERS_METADATA)} metadata files successfully!")

if __name__ == "__main__":
    main()
