#!/usr/bin/env python3
"""
Validator for KIMI reconstruction outputs.

Validates that each KIMI reconstruction directory contains all required files
with proper structure and content.

Required files per directory:
- metadata.yml
- reconstruction.md
- apparatus.md
- evidence.json
- summary.txt

Usage:
    python scripts/validate_kimi_run.py [--dir callimachina/discoveries]
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import yaml


class KimiValidator:
    """Validates KIMI reconstruction output directories."""

    REQUIRED_FILES = {
        'metadata.yml': 'YAML metadata file',
        'reconstruction.md': 'Reconstruction markdown',
        'apparatus.md': 'Critical apparatus markdown',
        'evidence.json': 'Evidence JSON file',
        'summary.txt': 'Summary text file'
    }

    REQUIRED_METADATA_FIELDS = [
        'work_id',
        'author',
        'title',
        'provenance',
        'sources',
        'confidence'
    ]

    def __init__(self, discoveries_dir: Path):
        self.discoveries_dir = Path(discoveries_dir)
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def find_kimi_directories(self) -> List[Path]:
        """Find all _KIMI directories."""
        return sorted([
            d for d in self.discoveries_dir.iterdir()
            if d.is_dir() and d.name.endswith('_KIMI')
        ])

    def validate_directory(self, kimi_dir: Path) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a single KIMI directory.

        Returns:
            (is_valid, errors, warnings)
        """
        errors = []
        warnings = []

        # Check for required files
        for filename, description in self.REQUIRED_FILES.items():
            filepath = kimi_dir / filename
            if not filepath.exists():
                errors.append(f"Missing {description}: {filename}")
            elif filepath.stat().st_size == 0:
                warnings.append(f"Empty {description}: {filename}")

        # Validate metadata.yml structure
        metadata_path = kimi_dir / 'metadata.yml'
        if metadata_path.exists():
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = yaml.safe_load(f)

                # Check required fields
                for field in self.REQUIRED_METADATA_FIELDS:
                    if field not in metadata:
                        errors.append(f"Missing required metadata field: {field}")
                    elif field == 'confidence' and isinstance(metadata[field], dict):
                        # Validate confidence structure
                        conf = metadata['confidence']
                        required_conf_fields = ['prior', 'posterior_mean', 'ci_lower', 'ci_upper']
                        for conf_field in required_conf_fields:
                            if conf_field not in conf:
                                errors.append(f"Missing confidence field: {conf_field}")

            except yaml.YAMLError as e:
                errors.append(f"Invalid YAML in metadata.yml: {e}")
            except Exception as e:
                errors.append(f"Error reading metadata.yml: {e}")

        # Validate evidence.json structure
        evidence_path = kimi_dir / 'evidence.json'
        if evidence_path.exists():
            try:
                with open(evidence_path, 'r', encoding='utf-8') as f:
                    evidence = json.load(f)

                # Basic structure check
                if 'work_id' not in evidence:
                    warnings.append("evidence.json missing work_id field")
                if 'evidence_chain' not in evidence:
                    warnings.append("evidence.json missing evidence_chain field")

            except json.JSONDecodeError as e:
                errors.append(f"Invalid JSON in evidence.json: {e}")
            except Exception as e:
                errors.append(f"Error reading evidence.json: {e}")

        # Check reconstruction.md has disclaimer
        reconstruction_path = kimi_dir / 'reconstruction.md'
        if reconstruction_path.exists():
            try:
                with open(reconstruction_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'probabilistic reconstruction' not in content.lower():
                        warnings.append("reconstruction.md may be missing disclaimer")
            except Exception as e:
                warnings.append(f"Error reading reconstruction.md: {e}")

        is_valid = len(errors) == 0
        return is_valid, errors, warnings

    def validate_all(self) -> Dict:
        """
        Validate all KIMI directories and return summary.

        Returns:
            Dictionary with validation results
        """
        kimi_dirs = self.find_kimi_directories()

        results = {
            'total_directories': len(kimi_dirs),
            'valid_directories': 0,
            'invalid_directories': 0,
            'directory_results': []
        }

        print(f"\n🔍 Validating {len(kimi_dirs)} KIMI reconstruction directories...\n")

        for kimi_dir in kimi_dirs:
            is_valid, errors, warnings = self.validate_directory(kimi_dir)

            result = {
                'directory': kimi_dir.name,
                'valid': is_valid,
                'errors': errors,
                'warnings': warnings
            }
            results['directory_results'].append(result)

            if is_valid:
                results['valid_directories'] += 1
                print(f"✅ {kimi_dir.name}")
            else:
                results['invalid_directories'] += 1
                print(f"❌ {kimi_dir.name}")
                for error in errors:
                    print(f"   ERROR: {error}")

            if warnings:
                for warning in warnings:
                    print(f"   ⚠️  WARNING: {warning}")

        return results

    def print_summary(self, results: Dict):
        """Print validation summary."""
        print("\n" + "="*70)
        print("📊 VALIDATION SUMMARY")
        print("="*70)
        print(f"Total KIMI directories: {results['total_directories']}")
        print(f"✅ Valid: {results['valid_directories']}")
        print(f"❌ Invalid: {results['invalid_directories']}")

        if results['invalid_directories'] == 0:
            print("\n🎉 All KIMI directories passed validation!")
        else:
            print(f"\n⚠️  {results['invalid_directories']} directories have issues")

        print("="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Validate KIMI reconstruction output directories'
    )
    parser.add_argument(
        '--dir',
        default='callimachina/discoveries',
        help='Path to discoveries directory (default: callimachina/discoveries)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )

    args = parser.parse_args()

    discoveries_dir = Path(args.dir)
    if not discoveries_dir.exists():
        print(f"❌ Error: Directory not found: {discoveries_dir}")
        sys.exit(1)

    validator = KimiValidator(discoveries_dir)
    results = validator.validate_all()

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        validator.print_summary(results)

    # Exit with error code if any directories are invalid
    sys.exit(0 if results['invalid_directories'] == 0 else 1)


if __name__ == '__main__':
    main()
