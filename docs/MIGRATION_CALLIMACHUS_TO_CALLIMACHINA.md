# Migration Guide: CALLIMACHUS → CALLIMACHINA

**Version:** 3.1.1  
**Date:** 2025-11-08  
**Migration Impact:** Low (mostly naming changes)

---

## 🎯 Overview

As of version 3.1.1, the project has been renamed from **CALLIMACHUS** to **CALLIMACHINA** to better reflect its nature as a machine-assisted system. This guide helps users and contributors adapt to the changes.

### What Changed

The name change is a deliberate portmanteau:
- **CALLIMACHINA** = "machina" (machine) + "Callimachus" (the Alexandrian librarian)
- Represents a machine-assisted homage to Callimachus's cataloging and reconstruction work

---

## 📦 Repository Changes

### Repository URL

**Old:**
```bash
git clone https://github.com/Shannon-Labs/callimachus.git
cd callimachus
```

**New:**
```bash
git clone https://github.com/Shannon-Labs/callimachina.git
cd callimachina
```

### Update Existing Clone

If you have an existing clone, update your remote URL:

```bash
git remote set-url origin https://github.com/Shannon-Labs/callimachina.git
git pull
```

---

## 📁 File and Directory Changes

### Renamed Files

| Old Name | New Name |
|----------|----------|
| `CALLIMACHUS_STATUS.md` | `CALLIMACHINA_STATUS.md` |
| `docs/CALLIMACHUS_v3.1_UPDATE_REPORT.md` | `docs/CALLIMACHINA_v3.1_UPDATE_REPORT.md` |

### No Directory Structure Changes

The internal directory structure remains unchanged:
- `callimachina/` - Main package directory (unchanged)
- `callimachina/src/` - Source code (unchanged)
- `callimachina/discoveries/` - Reconstruction outputs (unchanged)

---

## 💻 Code Changes

### Python Package Name

The package name remains **`callimachina`** (no change needed):

```python
# This remains the same
from callimachina.src.bayesian_reconstructor import BayesianReconstructor
from callimachina.src.database import DatabaseManager
```

### CLI Entry Point

The CLI command remains **`callimachina`** (no change needed):

```bash
# This remains the same
callimachina reconstruct --confidence-threshold 0.7
python -m callimachina.src.cli reconstruct
```

### Class Names (Internal)

Internal class names have been updated for consistency:

| Old Class Name | New Class Name |
|----------------|----------------|
| `CallimachusOrchestrator` | `CallimachinaOrchestrator` |
| `CallimachusAPI` (website) | `CallimachinaAPI` |
| `CallimachusApp` (website) | `CallimachinaApp` |

**Note:** These are internal changes. If you're using the public API, no code changes are needed.

---

## 📖 Documentation Updates

### Updated Links

If you have bookmarks or references to documentation:

| Old Link | New Link |
|----------|----------|
| `docs/CALLIMACHUS_v3.1_UPDATE_REPORT.md` | `docs/CALLIMACHINA_v3.1_UPDATE_REPORT.md` |
| References to "CALLIMACHUS project" | References to "CALLIMACHINA project" |

### Citation Updates

Update your citations to use the new name:

**Old:**
```bibtex
@software{callimachus_v3,
  title = {CALLIMACHUS: The Alexandria Reconstruction Protocol},
  url = {https://github.com/Shannon-Labs/callimachus},
  ...
}
```

**New:**
```bibtex
@software{callimachina_v3,
  title = {CALLIMACHINA: The Alexandria Reconstruction Protocol},
  url = {https://github.com/Shannon-Labs/callimachina},
  version = {3.1.1},
  ...
}
```

Or use the provided `CITATION.cff` file.

---

## 🔧 Installation Updates

### PyPI (When Available)

**Old:**
```bash
pip install callimachus  # Old package name (deprecated)
```

**New:**
```bash
pip install callimachina  # New package name
```

### Development Installation

No changes needed:
```bash
git clone https://github.com/Shannon-Labs/callimachina.git
cd callimachina
pip install -r requirements.txt
python callimachina/seed_corpus.py
```

---

## 🤖 CI/CD and Automation

### GitHub Actions

If you have forks or workflows referencing the old repo:

**Update workflow references:**
```yaml
# Old
uses: Shannon-Labs/callimachus/.github/workflows/test.yml@main

# New
uses: Shannon-Labs/callimachina/.github/workflows/test.yml@main
```

### Badges

Update badge URLs in your documentation:

**Old:**
```markdown
[![Stars](https://img.shields.io/github/stars/Shannon-Labs/callimachus?style=social)](https://github.com/Shannon-Labs/callimachus)
```

**New:**
```markdown
[![Stars](https://img.shields.io/github/stars/Shannon-Labs/callimachina?style=social)](https://github.com/Shannon-Labs/callimachina)
```

---

## ❓ FAQ

### Do I need to reinstall the package?

If you installed from source (`pip install -e .`), no reinstallation needed. The package name was always `callimachina`.

### Will old imports break?

No. The Python package structure and import paths remain unchanged:
```python
from callimachina.src.cli import callimachina  # Still works
```

### What about existing data?

All data structures remain compatible:
- SQLite database schema unchanged
- Output directory structure unchanged  
- YAML/JSON formats unchanged

### What if I have local changes?

Standard git workflow applies:
```bash
git remote set-url origin https://github.com/Shannon-Labs/callimachina.git
git fetch origin
git merge origin/main  # or rebase
```

### Why the name change?

**CALLIMACHINA** better represents the system as a machine-assisted tool (not claiming to be Callimachus himself). The portmanteau emphasizes:
- **machina** - Acknowledging the computational/AI nature
- **Callimachus** - Honoring the librarian's cataloging legacy

---

## 🆘 Support

If you encounter issues during migration:

1. **Check** this guide for common solutions
2. **Search** existing issues: https://github.com/Shannon-Labs/callimachina/issues
3. **Create** a new issue with the `migration` label

---

## 📋 Checklist for Contributors

- [ ] Update local git remote URL
- [ ] Pull latest changes from `main`
- [ ] Update any documentation references to CALLIMACHUS → CALLIMACHINA
- [ ] Update any hardcoded repository URLs
- [ ] Test that imports still work
- [ ] Update citations/references in papers or documentation

---

**Last Updated:** 2025-11-08  
**Migration Complexity:** Low  
**Breaking Changes:** None (naming only)
