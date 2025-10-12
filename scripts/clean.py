#!/usr/bin/env python3
"""
Text cleaning script for Ignaria Corpus.

This script standardizes text formatting, removes unwanted characters,
and ensures consistent encoding across all texts in the corpus.
"""

import argparse
import os
import sys
import re
import unicodedata
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TextCleaner:
    def __init__(self, corpus_root):
        self.corpus_root = Path(corpus_root)
        self.sources_dir = self.corpus_root / "sources"
        
    def normalize_unicode(self, text):
        """Normalize Unicode characters."""
        # Normalize to NFC (Canonical Decomposition followed by Canonical Composition)
        text = unicodedata.normalize('NFC', text)
        return text
    
    def clean_whitespace(self, text):
        """Clean up whitespace issues."""
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        
        # Replace multiple newlines with double newline (paragraph break)
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        
        # Remove trailing whitespace from lines
        lines = text.split('\n')
        lines = [line.rstrip() for line in lines]
        text = '\n'.join(lines)
        
        return text
    
    def standardize_punctuation(self, text):
        """Standardize punctuation marks."""
        # Replace smart quotes with regular quotes
        replacements = {
            '"': '"',  # Left double quotation mark
            '"': '"',  # Right double quotation mark
            ''': "'",  # Left single quotation mark
            ''': "'",  # Right single quotation mark
            '–': '-',  # En dash
            '—': '--', # Em dash
            '…': '...', # Horizontal ellipsis
            '•': '*',   # Bullet
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text
    
    def remove_control_characters(self, text):
        """Remove unwanted control characters."""
        # Keep only printable characters and common whitespace
        allowed_chars = set(range(32, 127)) | {9, 10, 13}  # Tab, LF, CR
        
        # For extended characters (above 127), keep them but normalize
        cleaned_chars = []
        for char in text:
            if ord(char) in allowed_chars:
                cleaned_chars.append(char)
            elif ord(char) > 127:
                # Keep extended characters (non-ASCII) but normalize
                cleaned_chars.append(char)
            # Skip other control characters
        
        return ''.join(cleaned_chars)
    
    def standardize_line_endings(self, text, target_ending='\n'):
        """Standardize line endings to Unix format (LF)."""
        # Convert all line endings to LF
        text = text.replace('\r\n', '\n')  # CRLF to LF
        text = text.replace('\r', '\n')    # CR to LF
        
        return text
    
    def clean_page_numbers(self, text):
        """Remove or standardize page numbers."""
        # Remove standalone page numbers (like "Page 123" or just "123")
        text = re.sub(r'\n\s*Page\s+\d+\s*\n', '\n\n', text, flags=re.IGNORECASE)
        text = re.sub(r'\n\s*\d+\s*\n(?=\n)', '\n\n', text)
        
        return text
    
    def clean_headers_footers(self, text):
        """Remove common headers and footers."""
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip lines that look like headers/footers
            if re.match(r'^[\s\-\=_]+$', line):  # Lines of dashes, underscores, etc.
                continue
            if re.match(r'^\s*\d+\s*$', line):   # Standalone numbers
                continue
            if len(line.strip()) < 3:             # Very short lines
                continue
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def clean_text(self, text, aggressive=False):
        """Apply all cleaning operations to text."""
        logger.info("Starting text cleaning...")
        
        # Basic cleaning (always applied)
        text = self.normalize_unicode(text)
        text = self.remove_control_characters(text)
        text = self.standardize_punctuation(text)
        text = self.standardize_line_endings(text)
        
        if aggressive:
            # More aggressive cleaning
            text = self.clean_whitespace(text)
            text = self.clean_page_numbers(text)
            text = self.clean_headers_footers(text)
        
        logger.info("Text cleaning complete")
        return text
    
    def clean_file(self, file_path, aggressive=False, backup=True):
        """Clean a single text file."""
        try:
            logger.info(f"Cleaning {file_path}")
            
            # Read original file
            with open(file_path, 'r', encoding='utf-8') as f:
                original_text = f.read()
            
            # Create backup if requested
            if backup:
                backup_path = file_path.with_suffix(file_path.suffix + '.bak')
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_text)
                logger.info(f"Backup created: {backup_path}")
            
            # Clean the text
            cleaned_text = self.clean_text(original_text, aggressive)
            
            # Write cleaned text
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)
            
            # Report changes
            original_size = len(original_text)
            cleaned_size = len(cleaned_text)
            change = cleaned_size - original_size
            
            logger.info(f"Cleaned {file_path}: {original_size} -> {cleaned_size} chars ({change:+d})")
            return True
            
        except Exception as e:
            logger.error(f"Error cleaning {file_path}: {e}")
            return False
    
    def clean_all_texts(self, aggressive=False, backup=True):
        """Clean all text files in the sources directory."""
        if not self.sources_dir.exists():
            logger.error(f"Sources directory not found: {self.sources_dir}")
            return False
        
        text_files = list(self.sources_dir.glob("*.txt"))
        
        if not text_files:
            logger.warning("No text files found in sources directory")
            return True
        
        logger.info(f"Found {len(text_files)} text files to clean")
        
        success_count = 0
        for file_path in text_files:
            if self.clean_file(file_path, aggressive, backup):
                success_count += 1
        
        logger.info(f"Successfully cleaned {success_count}/{len(text_files)} files")
        return success_count == len(text_files)
    
    def preview_changes(self, file_path, aggressive=False):
        """Preview what changes would be made to a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_text = f.read()
            
            cleaned_text = self.clean_text(original_text, aggressive)
            
            print(f"Preview of changes for {file_path}:")
            print(f"Original size: {len(original_text)} characters")
            print(f"Cleaned size: {len(cleaned_text)} characters")
            print(f"Change: {len(cleaned_text) - len(original_text):+d} characters")
            
            # Show first few lines of difference
            original_lines = original_text.split('\n')[:5]
            cleaned_lines = cleaned_text.split('\n')[:5]
            
            print("\nFirst 5 lines comparison:")
            for i, (orig, clean) in enumerate(zip(original_lines, cleaned_lines)):
                if orig != clean:
                    print(f"Line {i+1}:")
                    print(f"  Original: {repr(orig)}")
                    print(f"  Cleaned:  {repr(clean)}")
                else:
                    print(f"Line {i+1}: No change")
            
            return True
            
        except Exception as e:
            logger.error(f"Error previewing {file_path}: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Clean texts in Ignaria Corpus")
    parser.add_argument("--file", help="Clean a specific file")
    parser.add_argument("--all", action="store_true", help="Clean all text files")
    parser.add_argument("--aggressive", action="store_true", help="Apply aggressive cleaning")
    parser.add_argument("--no-backup", action="store_true", help="Don't create backup files")
    parser.add_argument("--preview", action="store_true", help="Preview changes without applying")
    parser.add_argument("--corpus-root", default=".", help="Root directory of the corpus")
    
    args = parser.parse_args()
    
    cleaner = TextCleaner(args.corpus_root)
    backup = not args.no_backup
    
    if args.preview and args.file:
        cleaner.preview_changes(args.file, args.aggressive)
    elif args.file:
        success = cleaner.clean_file(args.file, args.aggressive, backup)
        sys.exit(0 if success else 1)
    elif args.all:
        success = cleaner.clean_all_texts(args.aggressive, backup)
        sys.exit(0 if success else 1)
    else:
        parser.error("Specify either --file or --all")

if __name__ == "__main__":
    main()
