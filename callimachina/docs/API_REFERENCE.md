# CALLIMACHINA v3.0 API Reference

**Complete documentation for developers and contributors**

---

## TABLE OF CONTENTS

1. [Installation](#installation)
2. [Core Classes](#core-classes)
3. [FragmentScraper API](#fragmentscraper-api)
4. [CitationNetwork API](#citationnetwork-api)
5. [BayesianReconstructor API](#bayesianreconstructor-api)
6. [StylometricEngine API](#stylometricengine-api)
7. [CrossLingualMapper API](#crosslingualmapper-api)
8. [CLI Interface](#cli-interface)
9. [Configuration](#configuration)
10. [Examples](#examples)

---

## INSTALLATION

### Requirements

- Python 3.8+
- 8GB+ RAM recommended
- Internet connection for API access

### Install from Source

```bash
git clone https://github.com/Shannon-Labs/callimachina.git
cd callimachina
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

### Verify Installation

```bash
python -c "import callimachina; print(callimachina.__version__)"
# Should print: 3.0.0
```

### Test Installation

```bash
python tests/test_v3_infrastructure.py
# Should pass 5/5 tests
```

---

## CORE CLASSES

### Overview

CALLIMACHINA provides five main classes:

```python
from callimachina import (
    FragmentScraper,      # Web scraping and data collection
    CitationNetwork,      # Network analysis
    BayesianReconstructor, # Bayesian inference
    StylometricEngine,    # Author fingerprinting
    CrossLingualMapper    # Translation chain analysis
)
```

### Basic Workflow

```python
# 1. Scrape fragments
scraper = FragmentScraper()
fragments = scraper.search_by_author("Eratosthenes")

# 2. Build citation network
network = CitationNetwork()
network.build_network(fragments)
gaps = network.identify_citation_gaps()

# 3. Reconstruct work
reconstructor = BayesianReconstructor()
results = reconstructor.reconstruct_work(
    work_id="Eratosthenes.Geographika.Book3",
    fragments=fragments,
    citations=network.get_citations(),
    metadata={"genre": "science", "century": -3}
)

# 4. Attribute authorship
stylometer = StylometricEngine(language="greek")
stylometer.create_author_profile("Eratosthenes", known_texts)
attribution = stylometer.attribute_text(unknown_fragment)

# 5. Map translation chains
mapper = CrossLingualMapper()
chain = mapper.map_translation_chain("Eratosthenes.Geographika")
```

---

## FRAGMENTSCRAPER API

### Class Definition

```python
class FragmentScraper:
    def __init__(self, rate_limit: float = 1.0, timeout: int = 30)
```

### Parameters

- `rate_limit` (float): Seconds between requests (default: 1.0)
- `timeout` (int): Request timeout in seconds (default: 30)

### Methods

#### `search_papyri_info(query, max_results=50)`

Search the Duke Databank of Documentary Papyri.

**Parameters**:
- `query` (str): Search query
- `max_results` (int): Maximum results to return

**Returns**: List[Dict] - List of fragment dictionaries

**Example**:
```python
scraper = FragmentScraper()
fragments = scraper.search_papyri_info("Aristotle Physics", max_results=10)

# Returns:
# [
#   {
#     'id': 'papyri.info/ddbdp/12345',
#     'text': '... fragment text ...',
#     'source': 'papyri.info',
#     'confidence': 0.8,
#     'metadata': {...}
#   }
# ]
```

---

#### `search_by_author(author, work=None)`

Search for fragments by author and optionally work.

**Parameters**:
- `author` (str): Author name
- `work` (str, optional): Work title

**Returns**: List[Dict] - Matching fragments

**Example**:
```python
# Search for all works by an author
fragments = scraper.search_by_author("Callimachus")

# Search for specific work
fragments = scraper.search_by_author("Posidippus", "Epigrams")
```

---

#### `get_fragment_text(fragment_id, source='papyri_info')`

Retrieve full text of a specific fragment.

**Parameters**:
- `fragment_id` (str): Fragment identifier
- `source` (str): Source database

**Returns**: str - Full text or None

**Example**:
```python
text = scraper.get_fragment_text("ddbdp/12345", "papyri_info")
print(text)
# Output: "... and as Aristotle says in his Physics ..."
```

---

#### `extract_citation_patterns(text)`

Extract citation patterns from fragment text.

**Parameters**:
- `text` (str): Text to analyze

**Returns**: List[Dict] - Citation dictionaries

**Example**:
```python
citations = scraper.extract_citation_patterns(
    "As Aristotle says in his Physics, the natural motion..."
)

# Returns:
# [
#   {
#     'cited_author': 'Aristotle',
#     'cited_work': 'Physics',
#     'pattern': 'as_says_in',
#     'confidence': 0.7
#   }
# ]
```

**Supported Patterns**:
- `"As [Author] says in [Work]"` → pattern: `as_says_in`
- `"Cf. [Author], [Work] [Book].[Line]"` → pattern: `cf_book_line`
- `"According to [Author]'s [Work]"` → pattern: `according_to`

---

#### `batch_search(queries, source='papyri_info')`

Perform batch search for multiple queries.

**Parameters**:
- `queries` (List[str]): List of search queries
- `source` (str): Source database

**Returns**: Dict[str, List[Dict]] - Results by query

**Example**:
```python
results = scraper.batch_search([
    "Aristotle Metaphysics",
    "Plato Republic",
    "Galen Anatomy"
])

# Returns:
# {
#   'Aristotle Metaphysics': [...fragments...],
#   'Plato Republic': [...fragments...],
#   'Galen Anatomy': [...fragments...]
# }
```

---

## CITATIONNETWORK API

### Class Definition

```python
class CitationNetwork:
    def __init__(self)
```

### Methods

#### `build_network(fragments)`

Build citation network from fragment data.

**Parameters**:
- `fragments` (List[Dict]): List of fragment dictionaries with citation data

**Returns**: networkx.DiGraph - Directed citation graph

**Example**:
```python
network = CitationNetwork()
G = network.build_network(fragments)

print(f"Nodes: {len(G.nodes())}")
print(f"Edges: {len(G.edges())}")
```

---

#### `identify_citation_gaps(min_citations=3)`

Identify "ghost genres" - works cited but not extant.

**Parameters**:
- `min_citations` (int): Minimum citations to consider a gap

**Returns**: List[Dict] - Citation gap analysis

**Example**:
```python
gaps = network.identify_citation_gaps(min_citations=3)

for gap in gaps[:5]:
    print(f"{gap['author']}: {gap['recoverability_score']:.2f}")
    print(f"  Reason: {gap['reason']}")
    print(f"  Strategy: {gap['search_strategy']}")
```

**Gap Dictionary Structure**:
```python
{
    'author': str,              # Cited author
    'citations': int,           # Number of citations
    'citing_authors': List[str], # Who cites them
    'genre': str,               # Inferred genre
    'recoverability_score': float,  # 0-1
    'reason': str,              # Why we think it's lost
    'predicted_works': int,     # Estimated works
    'search_strategy': str      # Where to look
}
```

---

#### `identify_load_bearing_nodes(threshold=0.1)`

Identify critical nodes whose loss would collapse chains.

**Parameters**:
- `threshold` (float): Centrality threshold

**Returns**: List[Dict] - Critical node analysis

**Example**:
```python
critical = network.identify_load_bearing_nodes()

for node in critical[:10]:
    print(f"{node['node']}: {node['combined_score']:.3f}")
    print(f"  Impact: {node['impact_score']:.3f}")
    print(f"  Risk: {node['risk_level']}")
```

---

#### `map_translation_chains()`

Map translation chains (Greek→Syriac→Arabic→Latin).

**Returns**: List[Dict] - Translation chain dictionaries

**Example**:
```python
chains = network.map_translation_chains()

for chain in chains:
    print(f"Greek: {chain['greek_original']}")
    if chain['arabic_translation']:
        print(f"Arabic: {chain['arabic_translation']['translator']}")
```

---

#### `calculate_priority_queue(gaps, critical_nodes)`

Calculate priority queue for excavation.

**Parameters**:
- `gaps` (List[Dict]): Citation gaps
- `critical_nodes` (List[Dict]): Critical nodes

**Returns**: pandas.DataFrame - Ranked targets

**Example**:
```python
priority_df = network.calculate_priority_queue(gaps, critical)
print(priority_df[['target', 'priority_score', 'search_strategy']].head())
```

---

#### `export_network(filepath, format='graphml')`

Export network to file.

**Parameters**:
- `filepath` (str): Output file path
- `format` (str): Format ('graphml', 'gexf', 'json')

**Example**:
```python
network.export_network("citation_network.graphml")
network.export_network("citation_network.json", format="json")
```

---

#### `visualize_network(filepath, figsize=(12, 8))`

Create network visualization.

**Parameters**:
- `filepath` (str): Output image path
- `figsize` (tuple): Figure size (width, height)

**Example**:
```python
network.visualize_network("network.png", figsize=(15, 10))
```

---

## BAYESIANRECONSTRUCTOR API

### Class Definition

```python
class BayesianReconstructor:
    def __init__(self, random_seed: int = 42)
```

### Parameters

- `random_seed` (int): Random seed for reproducibility (default: 42)

### Methods

#### `update_confidence(prior, evidence, weights=None)`

Update reconstruction confidence using Bayesian inference.

**Parameters**:
- `prior` (float): Prior confidence (0-1)
- `evidence` (List[Dict]): Evidence list
- `weights` (List[float], optional): Evidence weights

**Returns**: Dict[str, float] - Posterior statistics

**Example**:
```python
reconstructor = BayesianReconstructor()

prior = 0.6
evidence = [
    {'type': 'fragment', 'confidence': 0.9},
    {'type': 'citation', 'confidence': 0.8},
    {'type': 'translation', 'confidence': 0.7}
]

posterior = reconstructor.update_confidence(prior, evidence)
print(f"Posterior mean: {posterior['mean']:.3f}")
print(f"95% CI: [{posterior['ci_lower']:.3f}, {posterior['ci_upper']:.3f}]")
```

**Posterior Statistics Dictionary**:
```python
{
    'mean': float,      # Posterior mean
    'std': float,       # Standard deviation
    'ci_lower': float,  # 2.5% percentile
    'ci_upper': float,  # 97.5% percentile
    'median': float     # Posterior median
}
```

---

#### `reconstruct_work(work_id, fragments, citations, metadata)`

Perform full Bayesian reconstruction.

**Parameters**:
- `work_id` (str): Unique work identifier
- `fragments` (List[Dict]): Fragment data
- `citations` (List[Dict]): Citation data
- `metadata` (Dict): Work metadata

**Returns**: Dict[str, Any] - Reconstruction results

**Example**:
```python
results = reconstructor.reconstruct_work(
    work_id="Eratosthenes.Geographika.Book3",
    fragments=fragments,
    citations=citations,
    metadata={
        "author": "Eratosthenes",
        "title": "Geographika Book 3",
        "genre": "science",
        "century": -3
    }
)

print(f"Confidence: {results['posterior_confidence']['mean']:.1%}")
print(f"Fragments used: {results['fragments_used']}")
```

**Results Dictionary Structure**:
```python
{
    'work_id': str,
    'metadata': Dict,
    'prior_confidence': float,
    'posterior_confidence': Dict[str, float],
    'fragments_used': int,
    'citations_used': int,
    'reconstruction': Dict,    # Positioned text
    'metrics': Dict,           # Quality metrics
    'evidence_summary': Dict   # Evidence statistics
}
```

---

#### `plot_confidence_evolution(work_id, save_path=None)`

Plot confidence evolution over time.

**Parameters**:
- `work_id` (str): Work identifier
- `save_path` (str, optional): Path to save plot

**Example**:
```python
reconstructor.plot_confidence_evolution(
    "Eratosthenes.Geographika.Book3",
    save_path="confidence_evolution.png"
)
```

---

#### `save_reconstruction(results, output_dir)`

Save reconstruction to disk.

**Parameters**:
- `results` (Dict): Reconstruction results
- `output_dir` (str): Output directory

**Example**:
```python
reconstructor.save_reconstruction(results, "discoveries/eratosthenes-geographika")
# Creates:
# - eratosthenes-geographika_reconstruction.json
# - eratosthenes-geographika_text.md
# - eratosthenes-geographika_metrics.csv
# - eratosthenes-geographika_confidence_history.csv
```

---

#### `compare_reconstructions(reconstructions)`

Compare multiple reconstructions.

**Parameters**:
- `reconstructions` (List[Dict]): List of reconstruction results

**Returns**: pandas.DataFrame - Comparison table

**Example**:
```python
comparisons = reconstructor.compare_reconstructions([rec1, rec2, rec3])
print(comparisons[['work_id', 'posterior_mean', 'overall_quality']])
```

---

## STYLOMETRICENGINE API

### Class Definition

```python
class StylometricEngine:
    def __init__(self, language: str = 'greek')
```

### Parameters

- `language` (str): Language code ('greek', 'latin', 'arabic', 'syriac')

### Methods

#### `extract_features(texts)`

Extract stylometric features from texts.

**Parameters**:
- `texts` (List[str]): List of text strings

**Returns**: pandas.DataFrame - Feature matrix

**Example**:
```python
stylometer = StylometricEngine(language="greek")
texts = ["καὶ ὁ ἄνθρωπος ἦν", "ἡ γυνὴ καλὴ ἦν"]
features = stylometer.extract_features(texts)

print(features.columns)
# Output: ['char_count', 'word_count', 'avg_word_length', ...]
```

**Feature Categories**:
- Basic statistics (char_count, word_count, etc.)
- Lexical features (vocabulary richness, hapax ratio)
- Syntactic features (sentence length, punctuation)
- Morphological features (case endings, particles)
- Character features (diversity, bigrams)

---

#### `create_author_profile(author, texts, metadata=None)`

Create stylometric profile for an author.

**Parameters**:
- `author` (str): Author name
- `texts` (List[str]): List of authentic texts
- `metadata` (Dict, optional): Additional metadata

**Returns**: Dict[str, Any] - Author profile

**Example**:
```python
# Known authentic texts by Eratosthenes
known_texts = [
    "... text of Geographika Book 1 ...",
    "... text of Geographika Book 2 ...",
    "... text of On the Measurement of the Earth ..."
]

profile = stylometer.create_author_profile("Eratosthenes", known_texts)
print(f"Profile reliability: {profile['reliability_score']:.2f}")
```

**Profile Structure**:
```python
{
    'author': str,
    'signature': Dict,         # Mean and std of features
    'ngram_signature': Dict,   # Characteristic n-grams
    'feature_importance': Dict, # Important features
    'text_count': int,
    'total_word_count': int,
    'reliability_score': float
}
```

---

#### `attribute_text(text, candidates=None)`

Attribute anonymous text to potential authors.

**Parameters**:
- `text` (str): Text to attribute
- `candidates` (List[str], optional): Candidate authors

**Returns**: List[Tuple[str, float]] - (author, confidence) pairs

**Example**:
```python
# Attribute unknown fragment
unknown = "... fragment text ..."
attributions = stylometer.attribute_text(unknown)

for author, confidence in attributions[:3]:
    print(f"{author}: {confidence:.2f}")
```

---

#### `verify_authenticity(text, claimed_author)`

Verify if text is authentic to claimed author.

**Parameters**:
- `text` (str): Text to verify
- `claimed_author` (str): Alleged author

**Returns**: Dict[str, Any] - Verification results

**Example**:
```python
results = stylometer.verify_authenticity(unknown, "Eratosthenes")

if results['authentic']:
    print(f"Authentic! Confidence: {results['confidence']:.1%}")
else:
    print(f"Probably not authentic. Best alternative: {results['best_alternative']}")
```

**Results Structure**:
```python
{
    'authentic': bool,
    'confidence': float,
    'relative_confidence': float,
    'claimed_author_score': float,
    'best_alternative': Tuple[str, float],
    'feature_analysis': Dict  # Detailed analysis
}
```

---

#### `detect_stylistic_outliers(texts, metadata)`

Detect texts with different stylistic patterns.

**Parameters**:
- `texts` (List[str]): Texts to analyze
- `metadata` (List[Dict]): Metadata for each text

**Returns**: List[Dict] - Outlier information

**Example**:
```python
texts = [text1, text2, text3, text4]
metadata = [
    {'work': 'fragment1', 'date': '200 CE'},
    {'work': 'fragment2', 'date': '150 CE'},
    # ...
]

outliers = stylometer.detect_stylistic_outliers(texts, metadata)
for outlier in outliers:
    print(f"Outlier: {outlier['metadata']['work']}")
```

---

#### `visualize_author_signatures(authors=None, save_path=None)`

Visualize author signatures using PCA.

**Parameters**:
- `authors` (List[str], optional): Authors to visualize
- `save_path` (str, optional): Path to save plot

**Example**:
```python
stylometer.visualize_author_signatures(
    authors=["Eratosthenes", "Aristotle", "Plato"],
    save_path="author_signatures.png"
)
```

---

## CROSSLINGUALMAPPER API

### Class Definition

```python
class CrossLingualMapper:
    def __init__(self, rate_limit: float = 1.0, timeout: int = 30)
```

### Parameters

- `rate_limit` (float): Seconds between requests (default: 1.0)
- `timeout` (int): Request timeout in seconds (default: 30)

### Methods

#### `query_arabic_corpus(query, corpus='openiti', max_results=50)`

Query Arabic corpus for Greek text references.

**Parameters**:
- `query` (str): Search query
- `corpus` (str): Corpus to query ('openiti', 'alcorpus', 'persee')
- `max_results` (int): Maximum results

**Returns**: List[Dict] - Arabic references

**Example**:
```python
mapper = CrossLingualMapper()
arabic_refs = mapper.query_arabic_corpus("Aristotle Metaphysics", corpus="openiti")

for ref in arabic_refs[:3]:
    print(f"{ref['title']} by {ref['author']}")
```

---

#### `query_syriac_corpus(query, max_results=50)`

Query Syriac corpus for Greek text transmissions.

**Parameters**:
- `query` (str): Search query
- `max_results` (int): Maximum results

**Returns**: List[Dict] - Syriac references

**Example**:
```python
syriac_refs = mapper.query_syriac_corpus("Aristotle Categories")

for ref in syriac_refs:
    print(f"Syriac manuscript: {ref['manuscript']}")
    print(f"Translator: {ref['translator']}")
```

---

#### `map_translation_chain(greek_work)`

Map complete translation chain for a Greek work.

**Parameters**:
- `greek_work` (str): Greek work identifier

**Returns**: Dict[str, Any] - Translation chain

**Example**:
```python
chain = mapper.map_translation_chain("Aristotle.Metaphysics")

print(f"Transmission score: {chain['transmission_score']:.2f}")
print(f"Syriac: {chain['syriac_intermediary'] is not None}")
print(f"Arabic: {chain['arabic_translation'] is not None}")
```

**Chain Structure**:
```python
{
    'greek_original': str,
    'syriac_intermediary': Dict or None,
    'arabic_translation': Dict or None,
    'latin_translation': Dict or None,
    'transmission_score': float,
    'confidence': float
}
```

---

#### `identify_translation_centers()`

Identify major translation centers.

**Returns**: Dict[str, Dict] - Translation center information

**Example**:
```python
centers = mapper.identify_translation_centers()

for name, info in centers.items():
    print(f"{name}: {info['transmission_score']:.2f}")
    print(f"  Works: {len(info['works_translated'])}")
    print(f"  Translators: {len(info['translators_active'])}")
```

**Major Centers**: Baghdad, Toledo, Edessa, Cairo, Damascus, Cordoba, Nisibis, Gundishapur

---

#### `generate_priority_queue(greek_works)`

Generate priority queue based on cross-lingual evidence.

**Parameters**:
- `greek_works` (List[str]): Greek works to analyze

**Returns**: pandas.DataFrame - Ranked priorities

**Example**:
```python
works = [
    "Aristotle.LostDialogues",
    "Eratosthenes.Geographika.Book3",
    "Hippolytus.OnHeraclitus"
]

priorities = mapper.generate_priority_queue(works)
print(priorities[['work', 'priority_score', 'has_arabic']].head())
```

---

#### `export_translation_network(output_file)`

Export translation network for visualization.

**Parameters**:
- `output_file` (str): Output JSON file

**Example**:
```python
mapper.export_translation_network("translation_network.json")
# Creates network file for Gephi/Cytoscape visualization
```

---

## CLI INTERFACE

### Command-Line Usage

CALLIMACHINA provides a command-line interface:

```bash
callimachina --help
```

### Commands

#### `reconstruct`

Reconstruct a lost work.

```bash
callimachina reconstruct --target "Eratosthenes.Geographika.Book3" \
                       --output discoveries/eratosthenes \
                       --priority high
```

**Options**:
- `--target` (str): Work identifier
- `--output` (str): Output directory
- `--priority` (str): Priority level
- `--config` (str): Configuration file

---

#### `network`

Analyze citation network.

```bash
callimachina network --mode excavation \
                    --output priority_queue.csv \
                    --visualize network.png
```

**Options**:
- `--mode` (str): Analysis mode
- `--output` (str): Output file
- `--visualize` (str): Visualization output
- `--fragments` (str): Fragment data source

---

#### `stylometry`

Perform stylometric analysis.

```bash
callimachina stylometry --author "Eratosthenes" \
                       --texts path/to/texts/*.txt \
                       --unknown unknown_fragment.txt
```

**Options**:
- `--author` (str): Author name
- `--texts` (str): Glob pattern for known texts
- `--unknown` (str): Unknown text file
- `--language` (str): Language code

---

#### `cross-lingual`

Map translation chains.

```bash
callimachina cross-lingual --work "Aristotle.Metaphysics" \
                          --output translation_chain.json
```

**Options**:
- `--work` (str): Work identifier
- `--output` (str): Output file
- `--corpus` (str): Corpus to query

---

#### `daily`

Run daily excavation (for cron/CI).

```bash
callimachina daily --config config/daily.yml \
                  --notify hunter@shannonlabs.dev
```

**Options**:
- `--config` (str): Configuration file
- `--notify` (str): Email for alerts
- `--test` (bool): Test mode (no actual scraping)

---

## CONFIGURATION

### Configuration File Format

CALLIMACHINA uses YAML configuration files:

```yaml
# config.yml
project:
  name: "CALLIMACHINA v3.0"
  version: "3.0.0"
  author: "Hunter Shannon"

scraping:
  rate_limit: 1.0
  timeout: 30
  sources:
    - papyri.info
    - oxyrhynchus
    - tlg

bayesian:
  random_seed: 42
  default_priors:
    fragment_authenticity: 0.7
    citation_reliability: 0.8
  
network:
  min_citations: 3
  centrality_threshold: 0.1

stylometry:
  language: "greek"
  min_texts_for_profile: 3
  
output:
  directory: "discoveries"
  formats: ["json", "md", "csv"]
  
logging:
  level: "INFO"
  file: "callimachina.log"
```

### Environment Variables

```bash
export CALLIMACHINA_CONFIG=/path/to/config.yml
export CALLIMACHINA_OUTPUT_DIR=/path/to/output
export CALLIMACHINA_LOG_LEVEL=DEBUG
export CALLIMACHINA_RANDOM_SEED=12345
```

---

## EXAMPLES

### Complete Reconstruction Example

```python
"""
Complete example: Reconstructing Eratosthenes' Geographika Book 3
"""

from callimachina import (
    FragmentScraper,
    CitationNetwork,
    BayesianReconstructor,
    StylometricEngine,
    CrossLingualMapper
)

# Initialize components
scraper = FragmentScraper()
network = CitationNetwork()
reconstructor = BayesianReconstructor()
stylometer = StylometricEngine(language="greek")
mapper = CrossLingualMapper()

# Step 1: Collect fragments
print("Step 1: Collecting fragments...")
fragments = scraper.search_by_author("Eratosthenes", "Geographika")
print(f"Found {len(fragments)} fragments")

# Step 2: Extract citations
print("\nStep 2: Extracting citations...")
for fragment in fragments:
    citations = scraper.extract_citation_patterns(fragment['text'])
    fragment['citations'] = citations

# Step 3: Build citation network
print("\nStep 3: Building citation network...")
G = network.build_network(fragments)
print(f"Network: {len(G.nodes())} nodes, {len(G.edges())} edges")

# Step 4: Identify gaps
print("\nStep 4: Identifying citation gaps...")
gaps = network.identify_citation_gaps()
print(f"Found {len(gaps)} citation gaps")

# Step 5: Map translation chain
print("\nStep 5: Mapping translation chain...")
chain = mapper.map_translation_chain("Eratosthenes.Geographika")
print(f"Transmission score: {chain['transmission_score']:.2f}")

# Step 6: Create author profile
print("\nStep 6: Creating author profile...")
# Note: This would use known authentic texts
# known_texts = [...]
# profile = stylometer.create_author_profile("Eratosthenes", known_texts)

# Step 7: Reconstruct work
print("\nStep 7: Reconstructing work...")
results = reconstructor.reconstruct_work(
    work_id="Eratosthenes.Geographika.Book3",
    fragments=fragments,
    citations=[c for f in fragments for c in f.get('citations', [])],
    metadata={
        "author": "Eratosthenes",
        "title": "Geographika Book 3",
        "genre": "science",
        "century": -3
    }
)

# Step 8: Save results
print("\nStep 8: Saving results...")
reconstructor.save_reconstruction(results, "discoveries/eratosthenes-geographika")

# Print summary
print("\n" + "="*60)
print("RECONSTRUCTION SUMMARY")
print("="*60)
print(f"Work: {results['work_id']}")
print(f"Confidence: {results['posterior_confidence']['mean']:.1%}")
print(f"Fragments: {results['fragments_used']}")
print(f"Citations: {results['citations_used']}")
print(f"Text coverage: {results['metrics']['text_coverage']:.1%}")
print("="*60)
```

### Batch Processing Example

```python
"""
Batch process multiple works from priority queue
"""

import pandas as pd
from callimachina import (
    FragmentScraper,
    CitationNetwork,
    BayesianReconstructor
)

# Load priority queue
priority_df = pd.read_csv("discoveries/priority_queue.csv")

# Initialize components
scraper = FragmentScraper()
network = CitationNetwork()
reconstructor = BayesianReconstructor()

# Process top 5 priorities
for _, row in priority_df.head(5).iterrows():
    work_id = row['target']
    print(f"\nProcessing: {work_id}")
    
    try:
        # Extract author and work
        if '.' in work_id:
            author, work = work_id.split('.', 1)
        else:
            author, work = work_id, ""
        
        # Collect fragments
        fragments = scraper.search_by_author(author, work)
        
        if not fragments:
            print(f"  No fragments found for {work_id}")
            continue
        
        # Extract citations
        for fragment in fragments:
            citations = scraper.extract_citation_patterns(fragment['text'])
            fragment['citations'] = citations
        
        # Reconstruct
        results = reconstructor.reconstruct_work(
            work_id=work_id,
            fragments=fragments,
            citations=[c for f in fragments for c in f.get('citations', [])],
            metadata={"author": author, "title": work}
        )
        
        # Save
        output_dir = f"discoveries/{work_id.lower().replace('.', '-')}"
        reconstructor.save_reconstruction(results, output_dir)
        
        print(f"  ✓ Confidence: {results['posterior_confidence']['mean']:.1%}")
        print(f"  ✓ Saved to: {output_dir}")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        continue

print("\nBatch processing complete!")
```

### Network Analysis Example

```python
"""
Analyze citation network and identify research opportunities
"""

from callimachina import FragmentScraper, CitationNetwork
import matplotlib.pyplot as plt

# Collect data
scraper = FragmentScraper()

# Search for multiple authors
authors = ["Aristotle", "Plato", "Galen", "Hippocrates"]
all_fragments = []

for author in authors:
    fragments = scraper.search_by_author(author)
    all_fragments.extend(fragments)
    print(f"Collected {len(fragments)} fragments for {author}")

# Build network
network = CitationNetwork()
G = network.build_network(all_fragments)

# Analyze
print(f"\nNetwork statistics:")
print(f"Nodes: {len(G.nodes())}")
print(f"Edges: {len(G.edges())}")
print(f"Density: {nx.density(G):.3f}")

# Find gaps
print(f"\nTop citation gaps:")
gaps = network.identify_citation_gaps(min_citations=2)
for gap in gaps[:5]:
    print(f"{gap['author']}: score {gap['recoverability_score']:.2f}")

# Find critical nodes
print(f"\nLoad-bearing nodes:")
critical = network.identify_load_bearing_nodes()
for node in critical[:5]:
    print(f"{node['node']}: impact {node['impact_score']:.3f}")

# Visualize
network.visualize_network("citation_network.png")
print("\nVisualization saved to citation_network.png")

# Save priority queue
priority_df = network.calculate_priority_queue(gaps, critical)
priority_df.to_csv("priority_queue.csv", index=False)
print("Priority queue saved to priority_queue.csv")
```

---

## ERROR HANDLING

### Common Exceptions

```python
from callimachina import FragmentScraper, BayesianReconstructor

# Handle network errors
scraper = FragmentScraper()
try:
    fragments = scraper.search_papyri_info("Aristotle")
except ConnectionError as e:
    print(f"Network error: {e}")
    fragments = []  # Use cached data

# Handle reconstruction errors
reconstructor = BayesianReconstructor()
try:
    results = reconstructor.reconstruct_work(
        work_id="Unknown.Work",
        fragments=[],
        citations=[],
        metadata={}
    )
except ValueError as e:
    print(f"Reconstruction error: {e}")
    # Not enough evidence

# Handle missing author profiles
from callimachina import StylometricEngine
stylometer = StylometricEngine()
try:
    attribution = stylometer.attribute_text(text, ["UnknownAuthor"])
except ValueError as e:
    print(f"Profile error: {e}")
    # No profile available
```

### Logging Configuration

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Set specific component log levels
logging.getLogger('callimachina.fragment_scraper').setLevel(logging.DEBUG)
logging.getLogger('callimachina.bayesian_reconstructor').setLevel(logging.WARNING)
```

---

## PERFORMANCE TIPS

### 1. Batch Operations

```python
# Instead of individual searches
queries = ["Aristotle", "Plato", "Galen"]
results = scraper.batch_search(queries)  # More efficient
```

### 2. Caching Results

```python
import json
import os

# Cache network results
network_file = "citation_network.json"
if os.path.exists(network_file):
    G = nx.read_graphml(network_file)
else:
    G = network.build_network(fragments)
    nx.write_graphml(G, network_file)
```

### 3. Parallel Processing

```python
from multiprocessing import Pool

def process_work(work_id):
    # Process single work
    fragments = scraper.search_by_author(work_id)
    results = reconstructor.reconstruct_work(work_id, fragments, [], {})
    return results

# Process in parallel
with Pool(4) as p:
    results = p.map(process_work, work_list)
```

### 4. Memory Management

```python
# Process large networks in chunks
for chunk in chunks(large_fragment_list, size=100):
    G_chunk = network.build_network(chunk)
    # Analyze and discard
    del G_chunk
```

---

## CONTRIBUTING

### Code Style

- Follow PEP 8
- Use type hints
- Include docstrings
- Add tests for new features

### Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=callimachina tests/

# Run specific test
pytest tests/test_fragment_scraper.py::test_search
```

### Adding New Features

1. Fork the repository
2. Create feature branch
3. Add tests
4. Update documentation
5. Submit pull request

---

## SUPPORT

### Getting Help

- **GitHub Issues**: https://github.com/Shannon-Labs/callimachina/issues
- **Email**: hunter@shannonlabs.dev
- **Documentation**: https://shannon-labs.github.io/callimachina

### Reporting Bugs

Include:
- System information
- Python version
- Error message
- Minimal reproducible example
- Expected behavior

### Feature Requests

Open an issue with:
- Use case description
- Proposed API
- Implementation ideas
- Priority level

---

## LICENSE

CALLIMACHINA v3.0 is released under the MIT License.

See LICENSE file for details.

---

**API Version**: 3.0.0  
**Last Updated**: 2025-11-06  
**Documentation Version**: 1.0