#!/usr/bin/env python3
"""
Validation script for Ignaria Corpus.

This script validates the integrity and format of texts in the corpus,
ensuring consistency and detecting issues.
"""

import argparse
import os
import sys
import yaml
import hashlib
from pathlib import Path
import logging
import re

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CorpusValidator:
    def __init__(self, corpus_root):
        self.corpus_root = Path(corpus_root)
        self.sources_dir = self.corpus_root / "sources"
        self.manifest_path = self.corpus_root / "manifest.yaml"
        self.errors = []
        self.warnings = []
    
    def load_manifest(self):
        """Load the corpus manifest."""
        try:
            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.errors.append(f"Manifest not found at {self.manifest_path}")
            return None
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML in manifest: {e}")
            return None
    
    def validate_manifest(self, manifest):
        """Validate the manifest structure."""
        required_fields = ["corpus", "texts"]
        
        for field in required_fields:
            if field not in manifest:
                self.errors.append(f"Missing required field in manifest: {field}")
        
        if "texts" in manifest:
            for i, text in enumerate(manifest["texts"]):
                self.validate_text_entry(text, i)
    
    def validate_text_entry(self, text_entry, index):
        """Validate a single text entry in the manifest."""
        required_fields = ["id", "title", "author", "file"]
        
        for field in required_fields:
            if field not in text_entry:
                self.errors.append(f"Text entry {index}: missing required field '{field}'")
        
        # Check if files exist
        if "file" in text_entry:
            file_path = self.corpus_root / text_entry["file"]
            if not file_path.exists():
                self.errors.append(f"Text entry {index}: file not found: {file_path}")
        
        if "metadata" in text_entry:
            meta_path = self.corpus_root / text_entry["metadata"]
            if not meta_path.exists():
                self.errors.append(f"Text entry {index}: metadata file not found: {meta_path}")
    
    def validate_text_file(self, file_path):
        """Validate a text file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check encoding
            try:
                content.encode('utf-8')
            except UnicodeEncodeError:
                self.errors.append(f"Invalid UTF-8 encoding in {file_path}")
            
            # Check for common issues
            if len(content.strip()) == 0:
                self.warnings.append(f"Empty file: {file_path}")
            
            # Check for suspicious characters
            if '\x00' in content:
                self.errors.append(f"Null bytes found in {file_path}")
            
            # Check line endings consistency
            lines = content.splitlines()
            if content.endswith('\r\n'):
                line_ending = 'CRLF'
            elif content.endswith('\n'):
                line_ending = 'LF'
            elif content.endswith('\r'):
                line_ending = 'CR'
            else:
                line_ending = 'Unknown'
            
            # Check for mixed line endings
            crlf_count = content.count('\r\n')
            lf_count = content.count('\n') - crlf_count
            cr_count = content.count('\r') - crlf_count
            
            if sum([bool(crlf_count), bool(lf_count), bool(cr_count)]) > 1:
                self.warnings.append(f"Mixed line endings in {file_path}")
            
            # Basic text statistics
            word_count = len(content.split())
            char_count = len(content)
            
            logger.info(f"{file_path}: {char_count} chars, {word_count} words, {len(lines)} lines")
            
            return {
                "char_count": char_count,
                "word_count": word_count,
                "line_count": len(lines),
                "line_ending": line_ending
            }
            
        except Exception as e:
            self.errors.append(f"Error reading {file_path}: {e}")
            return None
    
    def validate_metadata_file(self, meta_path):
        """Validate a metadata file."""
        try:
            with open(meta_path, 'r', encoding='utf-8') as f:
                metadata = yaml.safe_load(f)
            
            # Check required metadata fields
            required_fields = ["text_info", "publication", "technical"]
            
            for field in required_fields:
                if field not in metadata:
                    self.warnings.append(f"Missing metadata section '{field}' in {meta_path}")
            
            # Validate text_info section
            if "text_info" in metadata:
                text_info = metadata["text_info"]
                required_text_fields = ["id", "title", "author"]
                
                for field in required_text_fields:
                    if field not in text_info:
                        self.warnings.append(f"Missing text_info field '{field}' in {meta_path}")
            
            return metadata
            
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML in metadata file {meta_path}: {e}")
            return None
        except Exception as e:
            self.errors.append(f"Error reading metadata file {meta_path}: {e}")
            return None
    
    def validate_corpus_integrity(self):
        """Perform comprehensive corpus validation."""
        logger.info("Starting corpus validation...")
        
        # Validate manifest
        manifest = self.load_manifest()
        if manifest:
            self.validate_manifest(manifest)
            
            # Validate each text and its metadata
            if "texts" in manifest:
                for text_entry in manifest["texts"]:
                    if "file" in text_entry:
                        file_path = self.corpus_root / text_entry["file"]
                        self.validate_text_file(file_path)
                    
                    if "metadata" in text_entry:
                        meta_path = self.corpus_root / text_entry["metadata"]
                        self.validate_metadata_file(meta_path)
        
        # Check for orphaned files
        if self.sources_dir.exists():
            for file_path in self.sources_dir.iterdir():
                if file_path.is_file() and file_path.suffix == '.txt':
                    # Check if this file is referenced in manifest
                    relative_path = file_path.relative_to(self.corpus_root)
                    found_in_manifest = False
                    
                    if manifest and "texts" in manifest:
                        for text_entry in manifest["texts"]:
                            if text_entry.get("file") == str(relative_path):
                                found_in_manifest = True
                                break
                    
                    if not found_in_manifest:
                        self.warnings.append(f"Orphaned text file: {file_path}")
        
        # Report results
        logger.info(f"Validation complete. Errors: {len(self.errors)}, Warnings: {len(self.warnings)}")
        
        if self.errors:
            logger.error("Errors found:")
            for error in self.errors:
                logger.error(f"  ERROR: {error}")
        
        if self.warnings:
            logger.warning("Warnings found:")
            for warning in self.warnings:
                logger.warning(f"  WARNING: {warning}")
        
        return len(self.errors) == 0
    
    def generate_report(self, output_file=None):
        """Generate a validation report."""
        report = {
            "validation_summary": {
                "errors": len(self.errors),
                "warnings": len(self.warnings),
                "status": "PASS" if len(self.errors) == 0 else "FAIL"
            },
            "errors": self.errors,
            "warnings": self.warnings
        }
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                yaml.dump(report, f, default_flow_style=False)
            logger.info(f"Validation report saved to {output_file}")
        else:
            print(yaml.dump(report, default_flow_style=False))

def main():
    parser = argparse.ArgumentParser(description="Validate Ignaria Corpus")
    parser.add_argument("--corpus-root", default=".", help="Root directory of the corpus")
    parser.add_argument("--report", help="Save validation report to file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    validator = CorpusValidator(args.corpus_root)
    success = validator.validate_corpus_integrity()
    
    if args.report:
        validator.generate_report(args.report)
    elif args.verbose:
        validator.generate_report()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
