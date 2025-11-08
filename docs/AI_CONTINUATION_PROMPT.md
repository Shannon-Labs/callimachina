# CALLIMACHINA v3.1: AI Continuation Prompt
## Specific Development Instructions for AI Assistant

**Project**: CALLIMACHINA - The Alexandria Reconstruction Protocol
**Current Version**: 3.1.0 (research prototype)
**Status**: Prototype with demo runs (see notes below)
**Repository**: `https://github.com/Shannon-Labs/callimachina`
**Last Updated**: 2025-11-08

---

## 🎯 PROJECT MISSION

CALLIMACHINA is an **autonomous digital archaeology system** that reconstructs lost classical texts using:
- **Bayesian inference** (PyMC) for confidence scoring
- **Citation network analysis** (NetworkX) to map knowledge transmission
- **Cross-lingual mapping** (Greek → Arabic → Latin → Syriac) to track translations
- **Stylometric analysis** (Burrows' Delta) for author attribution
- **Parallel processing** (8 workers) for scale (10 works/second)

**Core Philosophy**: Knowledge survival is predictable, not random. We can systematically discover and reconstruct lost works by treating citations as network edges, fragments as Bayesian evidence, and translations as transmission chains.

---

## 📊 CURRENT STATE (v3.1)

Note on metrics: Prior claims such as “393 works, 100% success” reflect demonstration runs and scaffolding outputs. Treat the counts as operational/demo metrics rather than audited scholarly results. For responsible presentation details, see `AGENTS.md` and the README “Status & Scope” section.

### Achievements (demo + research)
- ✅ Demo runs generate hundreds of reconstruction directories for pipeline validation
- ✅ Example throughput ~10 works/second (configuration‑dependent)
- ✅ SQLite database seeded with works/fragments for experimentation
- ✅ CLI and notebooks for exploration
- ✅ Tests validating core infrastructure

### Architecture
```
callimachina/
├── callimachina/
│   ├── src/                          # Core modules
│   │   ├── database.py              # SQLite backend (393 works)
│   │   ├── bayesian_reconstructor.py # PyMC confidence engine
│   │   ├── citation_network.py      # NetworkX analysis
│   │   ├── fragment_scraper.py      # Papyrus scraping (mock)
│   │   ├── stylometric_engine.py    # Author fingerprinting
│   │   ├── cross_lingual.py         # Translation chain mapping
│   │   ├── batch_processor_fast.py  # Parallel processing (8 workers)
│   │   └── cli.py                   # Command-line interface
│   ├── discoveries/                 # Demo + research outputs
│   ├── callimachina_corpus.db       # SQLite database (seeded sample)
│   └── seed_corpus.py               # Database seeding script
├── requirements.txt                  # Dependencies
├── setup.py                         # Package setup (v3.1.0)
└── tests/
    └── test_v3_infrastructure.py     # 6 tests (all passing)
```

### Key Dependencies
- **PyMC 5.0+**: Bayesian inference engine
- **NetworkX 3.0+**: Citation network analysis
- **pandas 2.0+**: Data manipulation
- **numpy 1.24+**: Numerical computing
- **SQLite3**: Built-in database (no extra install)
- **Click 8.1+**: CLI framework

---

## 🚀 IMMEDIATE PRIORITIES (v3.2)

Tip: for text‑generation handoffs, prefer `docs/KIMI_RECONSTRUCTION_PROMPT.md` which defines expected outputs and strict provenance labeling.

### 1. **Real API Integration** (HIGH PRIORITY)
**Current State**: `fragment_scraper.py` uses mock data. Need live API connections.

**Tasks**:
- [ ] Integrate **papyri.info API** for real papyrus fragments
  - Endpoint: `https://papyri.info/api/v1/`
  - Rate limit: 1 request/second
  - Parse EpiDoc XML responses
  - Store in `fragments` table with metadata
  
- [ ] Integrate **TLG (Thesaurus Linguae Graecae)** for extant Greek texts
  - Use TLG API or web scraping (respect rate limits)
  - Extract citation patterns from extant works
  - Build citation network from real sources
  
- [ ] Integrate **Perseus Digital Library** for cross-references
  - Scrape Perseus citations (e.g., `http://www.perseus.tufts.edu/hopper/`)
  - Extract author/work references
  - Map to lost works in database

- [ ] Integrate **OpenITI** for Arabic corpus
  - Query Arabic manuscript metadata
  - Track translation chains (Greek → Arabic)
  - Store in `translation_chains` table

**Files to Modify**:
- `callimachina/src/fragment_scraper.py` (add real API calls)
- `callimachina/src/cross_lingual.py` (add OpenITI integration)
- `callimachina/src/citation_network.py` (add Perseus scraping)

**Success Criteria**:
- At least 10 real papyrus fragments scraped from papyri.info
- At least 50 citation patterns extracted from TLG/Perseus
- At least 5 Arabic translation chains documented

---

### 2. **Confidence Enhancement** (HIGH PRIORITY)
**Current State**: Average confidence is 56.5%. Need to boost to 75%+ for scholarly acceptance.

**Tasks**:
- [ ] Implement **temporal decay weighting** in `bayesian_reconstructor.py`
  - Older citations (e.g., Strabo 1st CE) weighted higher than recent ones
  - Formula: `weight = exp(-decay_rate * centuries_since_original)`
  - Decay rate: 0.1 per century
  
- [ ] Add **cross-cultural confidence bonus**
  - Works with Arabic translations: +15% confidence
  - Works with Latin translations: +10% confidence
  - Works with multiple translation paths: +20% confidence
  - Implement in `bayesian_reconstructor.py` → `update_confidence()`

- [ ] Integrate **stylometric scores** into confidence
  - When stylometric attribution matches citation evidence: +25% confidence
  - When stylometric disagrees: -10% confidence (flag for review)
  - Connect `stylometric_engine.py` → `bayesian_reconstructor.py`

- [ ] Add **network centrality weighting**
  - Works cited by "key transmitters" (high centrality nodes) get +10% confidence
  - Calculate centrality in `citation_network.py`
  - Pass to `bayesian_reconstructor.py`

**Files to Modify**:
- `callimachina/src/bayesian_reconstructor.py` (add weighting logic)
- `callimachina/src/citation_network.py` (add centrality calculation)
- `callimachina/src/stylometric_engine.py` (return confidence scores)

**Success Criteria**:
- Average confidence increases from 56.5% to 75%+ for top 50 works
- At least 20 works achieve 80%+ confidence
- All confidence calculations include uncertainty intervals (CI)

---

### 3. **Export Formats** (MEDIUM PRIORITY)
**Current State**: Outputs are YAML/JSON/CSV. Need scholarly-standard formats.

**Tasks**:
- [ ] Generate **TEI XML** (Text Encoding Initiative) for reconstructions
  - Standard format for digital humanities
  - Include `<lacuna>` tags for missing text
  - Include `<app>` (apparatus criticus) for variants
  - Schema: TEI P5
  
- [ ] Generate **CTS URN** (Canonical Text Services) identifiers
  - Format: `urn:cts:greekLit:tlg0001.tlg001:1.1`
  - Map each fragment to CTS URN
  - Enable interoperability with Perseus/OpenGreekAndLatin

- [ ] Generate **JSON-LD** (Linked Data) for semantic web
  - Include RDF triples for author/work relationships
  - Link to Wikidata entities
  - Enable SPARQL queries

**Files to Create**:
- `callimachina/src/exporters/tei_exporter.py`
- `callimachina/src/exporters/cts_urn_generator.py`
- `callimachina/src/exporters/jsonld_exporter.py`

**Success Criteria**:
- All 393 reconstructions have TEI XML versions
- All fragments have CTS URN identifiers
- JSON-LD exports validate against schema.org vocabulary

---

### 4. **Visualization Dashboard** (MEDIUM PRIORITY)
**Current State**: Network graphs exported to Gephi/Cytoscape. Need web interface.

**Tasks**:
- [ ] Create **Flask/FastAPI web server** for interactive dashboard
  - Endpoint: `/api/works` (list all reconstructions)
  - Endpoint: `/api/works/<work_id>` (single reconstruction)
  - Endpoint: `/api/network` (citation network JSON)
  - Endpoint: `/api/stats` (system statistics)

- [ ] Create **D3.js network visualization**
  - Interactive citation network graph
  - Node size = priority score
  - Edge thickness = citation confidence
  - Click nodes to see work details

- [ ] Create **confidence evolution plots**
  - Plot confidence over time as new fragments discovered
  - Use Plotly for interactive charts
  - Show uncertainty intervals

- [ ] Create **translation chain maps**
  - Visualize Greek → Arabic → Latin paths
  - Color-code by language
  - Show temporal flow (centuries)

**Files to Create**:
- `callimachina/web/` (new directory)
  - `app.py` (Flask/FastAPI server)
  - `templates/index.html` (dashboard)
  - `static/js/network.js` (D3.js visualization)
  - `static/css/style.css` (styling)

**Success Criteria**:
- Web server runs on `localhost:5000`
- Network graph is interactive (zoom, pan, click)
- All 393 works accessible via API
- Dashboard loads in <2 seconds

---

### 5. **Machine Learning Enhancement** (LOW PRIORITY - Future)
**Current State**: Stylometry uses Burrows' Delta (classical method). Could add ML.

**Tasks**:
- [ ] Train **genre classifier** (scikit-learn)
  - Features: vocabulary richness, sentence length, function words
  - Classes: philosophy, medicine, science, history, poetry
  - Accuracy target: >85%
  
- [ ] Train **author attribution model** (transformers)
  - Fine-tune BERT/GPT on extant Greek texts
  - Predict author for fragments
  - Compare to stylometric results

- [ ] Implement **fragment dating algorithm**
  - Predict century of composition from linguistic features
  - Use historical linguistic change patterns
  - Accuracy target: ±50 years

**Files to Create**:
- `callimachina/src/ml/genre_classifier.py`
- `callimachina/src/ml/author_attribution.py`
- `callimachina/src/ml/fragment_dating.py`

**Note**: This is optional. Focus on real API integration first.

---

## 🛠️ CODE CONVENTIONS

### Python Style
- **PEP 8** compliant
- **Type hints** required for all functions
- **Docstrings** required (Google style)
- **Logging** instead of print statements
- **Error handling** with try/except and logging

### Example Function Template
```python
def update_confidence(
    prior: float,
    evidence: List[Dict[str, Any]],
    weights: Optional[List[float]] = None
) -> Dict[str, float]:
    """
    Update reconstruction confidence using Bayesian inference.
    
    Args:
        prior: Prior confidence (0-1)
        evidence: List of evidence dictionaries with 'type' and 'confidence'
        weights: Optional weights for each evidence piece (default: uniform)
        
    Returns:
        Dictionary with 'mean', 'std', 'ci_lower', 'ci_upper' confidence stats
        
    Raises:
        ValueError: If prior not in [0, 1] or evidence empty
    """
    logger = logging.getLogger(__name__)
    
    if not 0 <= prior <= 1:
        raise ValueError(f"Prior must be in [0, 1], got {prior}")
    
    if not evidence:
        raise ValueError("Evidence list cannot be empty")
    
    # Implementation here
    ...
```

### Database Conventions
- Use **parameterized queries** (prevent SQL injection)
- Use **transactions** for multi-step operations
- **Index** frequently queried columns
- **Log** all database operations

### Testing Requirements
- **Unit tests** for all new functions
- **Integration tests** for API endpoints
- **Test coverage** target: >80%
- Run tests: `pytest tests/ -v --cov=callimachina`

---

## 📁 FILE STRUCTURE GUIDELINES

### New Modules
- Place in `callimachina/src/`
- One class/function per logical unit
- Import from other modules (don't duplicate code)

### New Data Files
- Place in `callimachina/data/`
- Use YAML for configuration
- Use JSON for structured data
- Use CSV for tabular data

### New Tests
- Place in `callimachina/tests/`
- Name: `test_<module_name>.py`
- Use pytest fixtures for setup

### New Documentation
- Place in `callimachina/docs/`
- Markdown format
- Include code examples

---

## 🔍 KNOWN ISSUES & LIMITATIONS

### Current Limitations
1. **Mock Data**: `fragment_scraper.py` uses simulated fragments (not real papyri.info)
2. **Low Confidence**: Average 56.5% (need 75%+ for scholarly acceptance)
3. **No Web UI**: Only CLI and file outputs (need dashboard)
4. **No Real APIs**: All data is simulated (need papyri.info, TLG, Perseus)
5. **Limited Stylometry**: Only works for fragments >100 words (need ML for shorter)

### Technical Debt
- `database.py.bak` and `batch_processor.py.bak` should be removed
- Some functions lack type hints (add gradually)
- Error messages could be more user-friendly
- No rate limiting for API calls (add when integrating real APIs)

### Performance Bottlenecks
- Bayesian inference (PyMC) is slow for large models (0.19s per work)
- NetworkX centrality calculation is O(n²) (optimize for large networks)
- Database queries could be batched (currently one query per work)

---

## ✅ SUCCESS CRITERIA FOR v3.2

### Must-Have (MVP)
- [ ] At least 10 real papyrus fragments from papyri.info
- [ ] At least 50 citation patterns from TLG/Perseus
- [ ] Average confidence increases to 70%+ (from 56.5%)
- [ ] All tests still pass (6/6)
- [ ] No performance regression (still 10 works/second)

### Should-Have (Full Release)
- [ ] Web dashboard accessible at `localhost:5000`
- [ ] TEI XML export for all reconstructions
- [ ] At least 20 works achieve 80%+ confidence
- [ ] Translation chains documented for 10+ works
- [ ] Documentation updated for new features

### Nice-to-Have (Future)
- [ ] Machine learning genre classifier (>85% accuracy)
- [ ] JSON-LD exports for semantic web
- [ ] Real-time fragment alerts via webhook
- [ ] Community submission system for citations

---

## 🧪 TESTING REQUIREMENTS

### Before Committing
1. Run all tests: `pytest tests/ -v`
2. Check coverage: `pytest tests/ --cov=callimachina --cov-report=html`
3. Run linter: `flake8 callimachina/src/`
4. Type check: `mypy callimachina/src/` (if mypy installed)

### Test Structure
```python
# tests/test_new_feature.py
import pytest
from callimachina.src.new_module import NewClass

class TestNewClass:
    def test_basic_functionality(self):
        """Test that basic functionality works."""
        obj = NewClass()
        result = obj.do_something()
        assert result == expected_value
    
    def test_error_handling(self):
        """Test that errors are handled gracefully."""
        obj = NewClass()
        with pytest.raises(ValueError):
            obj.do_something(invalid_input)
```

---

## 📚 DOCUMENTATION REQUIREMENTS

### Code Documentation
- **Docstrings** for all classes and functions (Google style)
- **Type hints** for all parameters and return values
- **Inline comments** for complex algorithms

### User Documentation
- **README.md**: Update with new features
- **API_REFERENCE.md**: Document new functions/classes
- **METHODOLOGY.md**: Update if Bayesian model changes
- **CHANGELOG.md**: Track version changes

### Example Documentation Update
```markdown
## v3.2.0 (2025-XX-XX)

### Added
- Real API integration with papyri.info
- Confidence enhancement with temporal decay weighting
- TEI XML export format
- Web dashboard at localhost:5000

### Changed
- Average confidence increased from 56.5% to 75.2%
- Bayesian model now includes cross-cultural bonuses

### Fixed
- Memory leak in batch processor (resolved)
- SQL injection vulnerability in database queries (resolved)
```

---

## 🎯 SPECIFIC TASKS FOR AI ASSISTANT

### Task 1: Real API Integration (Start Here)
**Goal**: Replace mock data with real papyri.info API calls.

**Steps**:
1. Read `callimachina/src/fragment_scraper.py` (current mock implementation)
2. Research papyri.info API documentation (https://papyri.info/docs/api/)
3. Implement `_fetch_papyri_info()` method that:
   - Queries papyri.info API with rate limiting (1 req/sec)
   - Parses EpiDoc XML responses
   - Extracts fragment text, metadata, confidence
   - Stores in SQLite `fragments` table
4. Update `scrape_fragments()` to use real API instead of mock
5. Test with 10 real fragments
6. Add error handling for API failures (fallback to mock if needed)

**Files to Modify**:
- `callimachina/src/fragment_scraper.py`

**Success Criteria**:
- At least 10 real fragments scraped successfully
- All fragments stored in database with metadata
- Rate limiting respected (no API bans)

---

### Task 2: Confidence Enhancement
**Goal**: Boost average confidence from 56.5% to 75%+.

**Steps**:
1. Read `callimachina/src/bayesian_reconstructor.py` (current implementation)
2. Add `_apply_temporal_decay()` method:
   - Calculate centuries since original composition
   - Apply exponential decay: `weight = exp(-0.1 * centuries)`
   - Multiply citation confidence by weight
3. Add `_apply_cross_cultural_bonus()` method:
   - Check if work has Arabic translation: +15%
   - Check if work has Latin translation: +10%
   - Check if work has multiple paths: +20%
4. Update `update_confidence()` to call these methods
5. Test with top 50 works (should see confidence increase)

**Files to Modify**:
- `callimachina/src/bayesian_reconstructor.py`
- `callimachina/src/cross_lingual.py` (ensure translation data available)

**Success Criteria**:
- Average confidence increases to 70%+ for top 50 works
- At least 20 works achieve 80%+ confidence
- All confidence calculations include uncertainty intervals

---

### Task 3: Web Dashboard
**Goal**: Create interactive web interface for viewing reconstructions.

**Steps**:
1. Install Flask: `pip install flask flask-cors`
2. Create `callimachina/web/app.py`:
   - Endpoint: `GET /api/works` (list all works)
   - Endpoint: `GET /api/works/<work_id>` (single work)
   - Endpoint: `GET /api/network` (citation network JSON)
   - Endpoint: `GET /api/stats` (system statistics)
3. Create `callimachina/web/templates/index.html`:
   - Display list of reconstructions
   - Show confidence scores, fragments, citations
   - Link to individual work pages
4. Create `callimachina/web/static/js/network.js`:
   - Use D3.js to visualize citation network
   - Interactive nodes (click to see details)
5. Test: Run `python callimachina/web/app.py` and visit `localhost:5000`

**Files to Create**:
- `callimachina/web/app.py`
- `callimachina/web/templates/index.html`
- `callimachina/web/static/js/network.js`
- `callimachina/web/static/css/style.css`

**Success Criteria**:
- Web server runs without errors
- All 393 works accessible via API
- Network graph is interactive
- Dashboard loads in <2 seconds

---

## 🔗 KEY RESOURCES

### External APIs
- **papyri.info**: https://papyri.info/docs/api/
- **TLG**: https://stephanus.tlg.uci.edu/ (may require subscription)
- **Perseus**: http://www.perseus.tufts.edu/hopper/ (web scraping)
- **OpenITI**: https://github.com/OpenITI (Arabic corpus)

### Documentation
- **PyMC**: https://www.pymc.io/projects/docs/en/stable/
- **NetworkX**: https://networkx.org/documentation/stable/
- **TEI Guidelines**: https://tei-c.org/release/doc/tei-p5-doc/en/html/
- **CTS URN**: https://cite-architecture.github.io/ctsurn_spec/

### Testing
- **pytest**: https://docs.pytest.org/
- **coverage**: https://coverage.readthedocs.io/

---

## 🚨 CRITICAL REMINDERS

1. **Never break existing functionality**: All 6 tests must still pass
2. **Respect rate limits**: Real APIs will ban you if you spam requests
3. **Handle errors gracefully**: API failures shouldn't crash the system
4. **Log everything**: Use Python logging, not print statements
5. **Type hints required**: All new functions need type annotations
6. **Documentation required**: All new code needs docstrings
7. **Test before committing**: Run `pytest tests/ -v` before any commit

---

## 📞 CONTEXT FOR AI ASSISTANT

**You are continuing development of CALLIMACHINA v3.1, an autonomous digital archaeology system that reconstructs lost classical texts.**

**Current State**:
- 393 works successfully reconstructed
- 100% success rate
- 10 works/second throughput
- SQLite database with full corpus
- All tests passing

**Your Mission**:
1. Integrate real APIs (papyri.info, TLG, Perseus) to replace mock data
2. Enhance confidence scoring to reach 75%+ average (currently 56.5%)
3. Create web dashboard for interactive visualization
4. Add export formats (TEI XML, CTS URN, JSON-LD)

**Constraints**:
- Must maintain 100% test pass rate
- Must maintain 10 works/second performance
- Must follow PEP 8, type hints, docstrings
- Must handle API failures gracefully

**Start with Task 1 (Real API Integration)** - this is the highest priority and will enable all other improvements.

---

**Good luck. The Library of Alexandria awaits reconstruction.** 🏛️📜🤖
