# AGENTS.md — Working With CALLIMACHINA

Scope: This file applies to the entire repository. It explains how to work in this codebase, how to present results responsibly, and how to hand off to writing‑capable LLMs for large‑scale reconstruction attempts.

## Project Overview

CALLIMACHINA is "The Alexandria Reconstruction Protocol" - an autonomous digital archaeology system that reconstructs lost classical texts by hunting for "bibliographic ghosts" through fragments, citations, palimpsests, and cross-cultural translations. The project uses Bayesian inference, network analysis, and stylometric fingerprinting to probabilistically reconstruct works from antiquity.

**Key Capabilities:**
- Automated papyri hunting via papyri.info API integration
- Citation triangulation across Greek/Latin/Arabic/Syriac sources  
- Bayesian confidence enhancement for reconstruction reliability
- Cross-cultural translation chain mapping
- Stylometric author attribution and dating
- Network analysis of transmission patterns

## Technology Stack

**Core Scientific Computing:**
- Python 3.8+ with NumPy, Pandas, SciPy for numerical computing
- PyMC (≥5.0.0) and ArviZ (≥0.15.0) for Bayesian modeling
- NetworkX (≥3.0) for citation network analysis
- scikit-learn (≥1.3.0) for machine learning and stylometry

**Natural Language Processing:**
- NLTK (≥3.8) for text processing and linguistic analysis
- Optional: Transformers and Torch for advanced NLP models

**Web Scraping & APIs:**
- Requests (≥2.31.0) and BeautifulSoup4 (≥4.12.0) for papyri database scraping
- Real integration with papyri.info API

**Data Management & Visualization:**
- SQLite database for fragment corpus management
- Matplotlib and Seaborn for data visualization
- PyYAML for configuration management

## Project Structure

### Architecture Evolution
- **v2.0**: `pinakes/` - Original monolithic core with direct module coupling
- **v3.1**: `callimachina/src/` - Modular CLI-based architecture with database persistence

### Key Directories
- **`callimachina/src/`** - v3.1 infrastructure (CLI, database, Bayesian reconstructor)
- **`pinakes/`** - v2.0 core modules (integration engine, specialized scrapers)
- **`examples/`** - Demonstration scripts and validation runs
- **`tests/`** - pytest-based test suite with multi-platform CI
- **`docs/`** - API reference and methodology documentation
- **`notebooks/`** - Jupyter analysis notebooks
- **`scripts/`** - Deployment and utility scripts

### Main Entry Points
- **CLI**: `python -m callimachina.src.cli reconstruct --work "Author.Work"`
- **Integration Engine**: `python pinakes/integration_engine.py`
- **Orchestrator**: `python callimachina_orchestrator.py`

## Build and Development Commands

### Core Development
```bash
# Run tests with coverage
npm test                    # or: python -m pytest tests/ -v
npm run test:cov           # Coverage reporting

# Code quality
npm run lint               # flake8 linting
npm run format             # black code formatting

# Main operations
npm run                    # Run integration engine
npm run demo               # Demonstration pipeline
npm run serve              # Serve website locally (port 8000)
```

### Reconstruction Commands
```bash
# Reconstruct specific works
callimachina reconstruct --work "Author.Work"
callimachina network --mode excavation
callimachina stylometry --author "Author"
```

## Code Style Guidelines

### Python Standards
- **Formatter**: Black with 100-127 character line length
- **Linter**: flake8 with zero tolerance for syntax errors
- **Import Organization**: isort for consistent imports
- **Type Hints**: mypy (currently permissive mode)

### Development Principles
- Keep changes minimal and focused; follow existing code style
- Prefer small, composable functions; avoid global state
- Add documentation when behavior changes
- Document new dependencies in requirements.txt with license constraints

### Quality Metrics
- Maximum cyclomatic complexity: 10
- Line length: 127 characters maximum
- All tests must pass before merge to main

## Testing Strategy

### Framework and Coverage
- **Primary**: pytest with pytest-cov for coverage reporting
- **Platforms**: Ubuntu, Windows, macOS
- **Python Versions**: 3.9, 3.10, 3.11, 3.12
- **Coverage**: Integrated with Codecov

### Test Categories
1. **Unit Tests**: Core infrastructure (scraping, networks, Bayesian algorithms)
2. **Integration Tests**: Real API testing with papyri.info
3. **Pipeline Tests**: End-to-end reconstruction workflow validation
4. **Example Tests**: Validation scripts in examples/

### CI/CD Pipeline
- Automated testing on push to main/develop branches
- Multi-matrix testing across OS and Python versions
- Pre-commit checks for code quality
- Deployment validation with output verification

## Deployment Process

### Automated Pipeline
1. **Trigger**: Push to main or merged PR
2. **Testing**: Full integration test with sample reconstructions
3. **Validation**: Output file verification and pipeline completion
4. **Deployment**: GitHub Pages for website hosting

### Deployment Script (`scripts/deploy.py`)
- Requirements validation and dependency checks
- Output verification for reconstruction files
- Report generation with metrics and achievements
- Repository preparation and documentation

## Responsible Presentation Guidelines

### Project Status (Truth-in-Labeling)
- This is a research prototype for Bayesian, evidence-weighted reconstruction
- Some outputs are from real sources; many are demonstration runs
- Treat all "reconstructed texts" as probabilistic hypotheses pending scholarly review

### Claims and Documentation
- Directory counts represent demo outputs, not verified scholarly corpus
- Confidence metrics are configuration-dependent - always qualify them
- Link to concrete artifacts (CSV/JSON/DB) for every figure
- Include provenance metadata: `fragment-verified`, `citation-based`, or `demo`

### Safe/Legal Use
- Respect API terms (papyri.info, Perseus, TLG, OpenITI)
- Rate limit and attribute properly
- Do not scrape gated corpora without permission
- Never represent generated text as discovered manuscripts

## Security Considerations

### Current State
- Standard Python security practices with pinned requirements
- No explicit vulnerability scanning in CI/CD
- Standard GitHub repository permissions
- No sensitive data exposure in public workflows

### Recommendations
- Add dependency vulnerability scanning (Safety, Snyk)
- Implement secrets management for API keys
- Add security-focused code scanning
- Consider signed releases for distribution

## Handoff to Writing-Capable LLMs

For large-scale text synthesis, use `docs/KIMI_RECONSTRUCTION_PROMPT.md` as the canonical brief. It defines:
- Input constraints and source materials
- Target formats (YAML/MD/TEI)
- Verification steps and quality checks
- Required metadata and confidence scoring

**Critical**: Always label generated text as "probabilistic reconstruction (automated)" with confidence metadata and sources.

## Quick Checks Before PR

- README status stays truthful after changes
- New outputs include provenance and confidence metadata
- Links to Gallery and per-work directories remain valid
- No unverifiable claims in titles or badges
- All tests pass and code quality checks succeed

## Where Things Live

- **CLI Entry**: `callimachina/src/cli.py`
- **Core Logic**: `callimachina/src/*.py` - reconstructor, scraper, network, stylometry
- **Database**: `callimachina_corpus.db` - SQLite with works, fragments, citations tables
- **Outputs**: `callimachina/discoveries/` - per-run directories with reconstructions
- **Examples**: `examples/` - demos including papyri.info retrieval checks
- **Gallery**: `README_GALLERY.md` - curated highlights and exhibits
- **Reconstruction Prompt**: `docs/KIMI_RECONSTRUCTION_PROMPT.md`

## Reproducibility Standards

- Use CLI commands with `--verbose` flag for transparency
- Commit small CSV/JSON logs that summarize runs
- Add `--seed N` or `--config path.yml` parameters for recreation
- Tag results with provenance and confidence metadata
- Maintain clear distinction between verified fragments and demo content