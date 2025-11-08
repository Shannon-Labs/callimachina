#!/usr/bin/env python3
"""
Validator for KIMI reconstruction runs.
Checks completeness, proper formatting, and generates index CSV.
"""

import os
import sys
import yaml
import json
import csv
from pathlib import Path
from datetime import datetime


def validate_metadata(file_path):
    """Validate metadata.yml file."""
    errors = []
    warnings = []
    
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Required fields
        required_fields = ['work_id', 'author', 'title', 'provenance', 'sources', 'confidence']
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # Validate confidence structure
        if 'confidence' in data:
            conf = data['confidence']
            conf_fields = ['prior', 'posterior_mean', 'ci_lower', 'ci_upper', 'rationale']
            for field in conf_fields:
                if field not in conf:
                    errors.append(f"Missing confidence field: {field}")
        
        # Validate provenance
        if 'provenance' in data and data['provenance'] not in ['citation-based', 'fragment-verified', 'demo']:
            warnings.append(f"Unusual provenance value: {data['provenance']}")
        
    except Exception as e:
        errors.append(f"Failed to parse metadata: {e}")
    
    return errors, warnings


def validate_reconstruction(file_path):
    """Validate reconstruction.md file."""
    errors = []
    warnings = []
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check for disclaimer
        if "probabilistic reconstruction (automated)" not in content.lower():
            errors.append("Missing required disclaimer")
        
        # Check for confidence mention
        if "confidence" not in content.lower():
            warnings.append("No confidence mention in header")
        
        # Check for lacunae markers
        if "[…]" not in content and "[?]" not in content:
            warnings.append("No lacunae markers found - may be too speculative")
        
        # Check length (should be substantial)
        if len(content) < 500:
            warnings.append("Reconstruction seems very short")
            
    except Exception as e:
        errors.append(f"Failed to read reconstruction: {e}")
    
    return errors, warnings


def validate_apparatus(file_path):
    """Validate apparatus.md file."""
    errors = []
    warnings = []
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check for sections
        required_sections = ['Fragmentary Sources', 'Stylometric Analysis', 'Historical Context']
        for section in required_sections:
            if section.lower() not in content.lower():
                warnings.append(f"May be missing section: {section}")
        
        # Check length
        if len(content) < 1000:
            warnings.append("Apparatus seems brief")
            
    except Exception as e:
        errors.append(f"Failed to read apparatus: {e}")
    
    return errors, warnings


def validate_evidence(file_path):
    """Validate evidence.json file."""
    errors = []
    warnings = []
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Required structure
        if 'work_id' not in data:
            errors.append("Missing work_id")
        
        if 'passage_mapping' not in data:
            errors.append("Missing passage_mapping")
        else:
            passages = data['passage_mapping']
            if not passages:
                warnings.append("No passages mapped")
            
            for i, passage in enumerate(passages):
                if 'passage_id' not in passage:
                    errors.append(f"Passage {i} missing passage_id")
                if 'evidence_items' not in passage:
                    errors.append(f"Passage {i} missing evidence_items")
                if 'confidence' not in passage:
                    errors.append(f"Passage {i} missing confidence")
        
        if 'summary_statistics' not in data:
            warnings.append("Missing summary_statistics")
        
    except Exception as e:
        errors.append(f"Failed to parse evidence.json: {e}")
    
    return errors, warnings


def validate_summary(file_path):
    """Validate summary.txt file."""
    errors = []
    warnings = []
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check for key elements
        if "PROVENANCE" not in content:
            warnings.append("Missing PROVENANCE label")
        
        if "POSTERIOR CONFIDENCE" not in content:
            errors.append("Missing POSTERIOR CONFIDENCE")
        
        if "EVIDENCE SOURCES" not in content:
            warnings.append("Missing EVIDENCE SOURCES")
        
        # Check length (should be substantial)
        if len(content) < 1000:
            warnings.append("Summary seems brief")
            
    except Exception as e:
        errors.append(f"Failed to read summary: {e}")
    
    return errors, warnings


def validate_directory(dir_path):
    """Validate a single reconstruction directory."""
    errors = []
    warnings = []
    
    required_files = [
        'metadata.yml',
        'reconstruction.md',
        'apparatus.md',
        'evidence.json',
        'summary.txt'
    ]
    
    # Check for required files
    for file_name in required_files:
        file_path = dir_path / file_name
        if not file_path.exists():
            errors.append(f"Missing required file: {file_name}")
            continue
        
        # Validate based on file type
        if file_name == 'metadata.yml':
            e, w = validate_metadata(file_path)
            errors.extend([f"metadata.yml: {err}" for err in e])
            warnings.extend([f"metadata.yml: {warn}" for warn in w])
        
        elif file_name == 'reconstruction.md':
            e, w = validate_reconstruction(file_path)
            errors.extend([f"reconstruction.md: {err}" for err in e])
            warnings.extend([f"reconstruction.md: {warn}" for warn in w])
        
        elif file_name == 'apparatus.md':
            e, w = validate_apparatus(file_path)
            errors.extend([f"apparatus.md: {err}" for err in e])
            warnings.extend([f"apparatus.md: {warn}" for warn in w])
        
        elif file_name == 'evidence.json':
            e, w = validate_evidence(file_path)
            errors.extend([f"evidence.json: {err}" for err in e])
            warnings.extend([f"evidence.json: {warn}" for warn in w])
        
        elif file_name == 'summary.txt':
            e, w = validate_summary(file_path)
            errors.extend([f"summary.txt: {err}" for err in e])
            warnings.extend([f"summary.txt: {warn}" for warn in w])
    
    return errors, warnings


def generate_index_csv(directories, output_path):
    """Generate index CSV from directories."""
    
    rows = []
    
    for dir_path in directories:
        metadata_file = dir_path / 'metadata.yml'
        if not metadata_file.exists():
            continue
        
        try:
            with open(metadata_file, 'r') as f:
                data = yaml.safe_load(f)
            
            # Extract required fields
            work_id = data.get('work_id', '')
            provenance = data.get('provenance', '')
            
            confidence = data.get('confidence', {})
            posterior_mean = confidence.get('posterior_mean', '')
            ci_lower = confidence.get('ci_lower', '')
            ci_upper = confidence.get('ci_upper', '')
            
            sources = data.get('sources', [])
            sources_count = len(sources)
            
            # Build row
            rows.append({
                'work_id': work_id,
                'path': str(dir_path),
                'provenance': provenance,
                'posterior_mean': posterior_mean,
                'ci_lower': ci_lower,
                'ci_upper': ci_upper,
                'sources_count': sources_count
            })
            
        except Exception as e:
            print(f"Warning: Could not parse metadata for {dir_path}: {e}")
    
    # Write CSV
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['work_id', 'path', 'provenance', 'posterior_mean', 'ci_lower', 'ci_upper', 'sources_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    
    return len(rows)


def main():
    """Main validation function."""
    
    if len(sys.argv) != 2:
        print("Usage: python validate_kimi_run.py <discoveries_directory>")
        sys.exit(1)
    
    discoveries_dir = Path(sys.argv[1])
    if not discoveries_dir.exists():
        print(f"Error: Directory {discoveries_dir} does not exist")
        sys.exit(1)
    
    # Find all KIMI reconstruction directories
    kimi_dirs = [d for d in discoveries_dir.iterdir() 
                 if d.is_dir() and d.name.endswith('_KIMI')]
    
    if not kimi_dirs:
        print("No KIMI reconstruction directories found")
        sys.exit(1)
    
    print(f"Found {len(kimi_dirs)} KIMI reconstruction directories")
    print("=" * 60)
    
    total_errors = 0
    total_warnings = 0
    
    # Validate each directory
    for i, dir_path in enumerate(sorted(kimi_dirs), 1):
        print(f"\n{i}. Validating {dir_path.name}...")
        
        errors, warnings = validate_directory(dir_path)
        
        if errors:
            print(f"   ❌ ERRORS ({len(errors)}):")
            for error in errors:
                print(f"      - {error}")
            total_errors += len(errors)
        
        if warnings:
            print(f"   ⚠️  WARNINGS ({len(warnings)}):")
            for warning in warnings:
                print(f"      - {warning}")
            total_warnings += len(warnings)
        
        if not errors and not warnings:
            print(f"   ✅ OK")
    
    # Generate index CSV
    print("\n" + "=" * 60)
    print("Generating index CSV...")
    
    index_file = discoveries_dir / f"KIMI_RUN_INDEX_{datetime.now().strftime('%Y-%m-%d')}.csv"
    count = generate_index_csv(kimi_dirs, index_file)
    
    print(f"✅ Generated {index_file} with {count} entries")
    
    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print(f"Directories validated: {len(kimi_dirs)}")
    print(f"Total errors: {total_errors}")
    print(f"Total warnings: {total_warnings}")
    
    if total_errors == 0:
        print("\n🎉 All reconstructions passed validation!")
        sys.exit(0)
    else:
        print(f"\n❌ {total_errors} errors found - please review")
        sys.exit(1)


if __name__ == '__main__':
    main()
EOF