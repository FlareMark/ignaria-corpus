#!/usr/bin/env python3
"""
Download script for Ignaria Corpus texts.

This script handles downloading texts from various sources and adding them
to the corpus with proper metadata.
"""

import argparse
import os
import sys
import yaml
import requests
from pathlib import Path
from urllib.parse import urlparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CorpusDownloader:
    def __init__(self, corpus_root):
        self.corpus_root = Path(corpus_root)
        self.sources_dir = self.corpus_root / "sources"
        self.manifest_path = self.corpus_root / "manifest.yaml"
        
    def load_manifest(self):
        """Load the corpus manifest."""
        try:
            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Manifest not found at {self.manifest_path}")
            return None
    
    def save_manifest(self, manifest):
        """Save the updated manifest."""
        with open(self.manifest_path, 'w', encoding='utf-8') as f:
            yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
    
    def download_text(self, url, filename, metadata=None):
        """Download a text from URL and save to sources directory."""
        try:
            logger.info(f"Downloading {filename} from {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Save text file
            text_path = self.sources_dir / filename
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            # Save metadata if provided
            if metadata:
                meta_path = self.sources_dir / f"{Path(filename).stem}.meta.yaml"
                with open(meta_path, 'w', encoding='utf-8') as f:
                    yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)
            
            logger.info(f"Successfully downloaded {filename}")
            return True
            
        except requests.RequestException as e:
            logger.error(f"Failed to download {filename}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error processing {filename}: {e}")
            return False
    
    def add_to_manifest(self, text_id, title, author, filename, metadata=None):
        """Add a new text to the manifest."""
        manifest = self.load_manifest()
        if not manifest:
            return False
        
        # Create text entry
        text_entry = {
            "id": text_id,
            "title": title,
            "author": author,
            "file": f"sources/{filename}",
            "metadata": f"sources/{Path(filename).stem}.meta.yaml",
            "status": "active",
            "added": "2024-01-01"  # Should be current date
        }
        
        # Add metadata fields if provided
        if metadata:
            for key in ["language", "period", "genre"]:
                if key in metadata:
                    text_entry[key] = metadata[key]
        
        # Add to manifest
        if "texts" not in manifest:
            manifest["texts"] = []
        
        manifest["texts"].append(text_entry)
        
        # Update categories if provided
        if metadata and "categories" in metadata:
            for category in metadata["categories"]:
                if category not in manifest.get("categories", {}):
                    manifest["categories"][category] = []
                manifest["categories"][category].append(text_id)
        
        self.save_manifest(manifest)
        logger.info(f"Added {text_id} to manifest")
        return True
    
    def list_available_sources(self):
        """List available text sources."""
        sources = {
            "ccel": {
                "name": "Christian Classics Ethereal Library",
                "url_base": "https://www.ccel.org/",
                "formats": ["txt", "html", "xml"]
            },
            "gutenberg": {
                "name": "Project Gutenberg",
                "url_base": "https://www.gutenberg.org/",
                "formats": ["txt", "html", "epub"]
            }
        }
        
        print("Available sources:")
        for key, source in sources.items():
            print(f"  {key}: {source['name']}")
            print(f"    URL: {source['url_base']}")
            print(f"    Formats: {', '.join(source['formats'])}")
            print()

def main():
    parser = argparse.ArgumentParser(description="Download texts for Ignaria Corpus")
    parser.add_argument("--url", help="URL to download text from")
    parser.add_argument("--filename", help="Local filename to save as")
    parser.add_argument("--text-id", help="Unique identifier for the text")
    parser.add_argument("--title", help="Title of the work")
    parser.add_argument("--author", help="Author of the work")
    parser.add_argument("--list-sources", action="store_true", help="List available sources")
    parser.add_argument("--corpus-root", default=".", help="Root directory of the corpus")
    
    args = parser.parse_args()
    
    downloader = CorpusDownloader(args.corpus_root)
    
    if args.list_sources:
        downloader.list_available_sources()
        return
    
    if not all([args.url, args.filename, args.text_id, args.title, args.author]):
        parser.error("URL, filename, text-id, title, and author are required for downloading")
    
    # Create sources directory if it doesn't exist
    downloader.sources_dir.mkdir(exist_ok=True)
    
    # Download the text
    success = downloader.download_text(args.url, args.filename)
    
    if success:
        # Add to manifest
        metadata = {
            "language": "English",  # Default, should be specified
            "period": "Unknown",    # Default, should be specified
            "genre": "Unknown"      # Default, should be specified
        }
        
        downloader.add_to_manifest(
            args.text_id, args.title, args.author, 
            args.filename, metadata
        )
        print(f"Successfully added {args.title} to the corpus")
    else:
        print("Download failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
