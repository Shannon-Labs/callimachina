# 📖 API Reference

## Core Classes

### `IntegrationEngine`

Main orchestrator for the reconstruction pipeline.

```python
from pinakes.integration_engine import IntegrationEngine

engine = IntegrationEngine(
    config_path="config/pipeline.yml",  # Optional
    verbose=True                         # Enable logging
)
```

#### Methods

**`run_full_pipeline(target_works=None, confidence_threshold=0.90)`**

Runs the complete 8-phase reconstruction pipeline.

- **Parameters:**
  - `target_works` (list): Specific works to reconstruct
  - `confidence_threshold` (float): Minimum confidence threshold
- **Returns:** Dictionary of reconstruction results
- **Example:**
```python
results = engine.run_full_pipeline(
    target_works=['Eratosthenes Geographika'],
    confidence_threshold=0.95
)
```

**`reconstruct_work(work_id, evidence_factors=None)`**

Reconstruct a single work with custom evidence weighting.

- **Parameters:**
  - `work_id` (str): Work identifier
  - `evidence_factors` (dict): Custom Bayesian priors
- **Returns:** Reconstruction object

### `FragmentScraper`

Extracts fragments from digital papyri collections.

```python
from pinakes.scrapers.papyri_scraper import FragmentScraper

scraper = FragmentScraper(
    sources=['papyri.info', 'perseus.tufts'],
    rate_limit=2  # requests per second
)

fragments = scraper.scrape_work('Callimachus Aetia')
```

### `CitationNetwork`

Builds and analyzes citation networks.

```python
from pinakes.network_builder import CitationNetwork

network = CitationNetwork()
network.build_from_fragments(fragments)

# Get network metrics
metrics = network.get_centrality_metrics()
graph = network.to_graphviz()  # For visualization
```

### `BayesianReconstructor`

Probabilistic text reconstruction using Bayesian methods.

```python
from pinakes.reconstruction_engine import BayesianReconstructor

reconstructor = BayesianReconstructor(
    prior_strength=0.5,
    evidence_weights={
        'citation_quality': 0.3,
        'temporal_distribution': 0.2,
        'translation_path': 0.2,
        'stylometric_score': 0.15,
        'network_centrality': 0.1,
        'genre_base_rate': 0.05
    }
)

reconstruction = reconstructor.reconstruct(
    fragments=fragment_list,
    citations=citation_network
)
```

## Configuration

### Pipeline Configuration

```yaml
# config/pipeline.yml
pipeline:
  phases:
    - fragment_scraping
    - citation_triangulation
    - network_building
    - stylometric_analysis
    - cross_lingual_mapping
    - bayesian_reconstruction
    - confidence_enhancement
    - integration_output

confidence_thresholds:
  low: 0.70
  medium: 0.85
  high: 0.95
  scholarly: 0.98

evidence_weights:
  citation_quality: 0.30
  temporal_distribution: 0.20
  translation_path: 0.20
  stylometric_score: 0.15
  network_centrality: 0.10
  genre_base_rate: 0.05
```

## Command Line Interface

### Basic Usage

```bash
# Reconstruct specific works
python callimachina/src/cli.py --reconstruct "Eratosthenes Geographika"

# Run full pipeline
python callimachina/src/cli.py --full-pipeline

# Generate report
python callimachina/src/cli.py --report --format markdown

# Custom configuration
python callimachina/src/cli.py --config config/custom.yml
```

### Options

- `--reconstruct WORK`: Reconstruct specific work(s)
- `--full-pipeline`: Run complete pipeline
- `--confidence THRESHOLD`: Set confidence threshold (0.0-1.0)
- `--report`: Generate output report
- `--format FORMAT`: Output format (json, yaml, markdown)
- `--verbose`: Enable detailed logging
- `--config PATH`: Custom configuration file

## Output Formats

### Reconstruction Object

```python
{
    "work_id": "eratosthenes_geographika",
    "title": "Eratosthenes Geographika",
    "confidence": 0.996,
    "confidence_level": "scholarly",
    "fragments": [
        {
            "id": "frag_001",
            "text": "Fragment text...",
            "source": "Strabo Geography 2.1.1",
            "confidence": 0.98,
            "language": "greek"
        }
    ],
    "citation_network": {
        "nodes": [...],
        "edges": [...],
        "centrality_metrics": {...}
    },
    "translation_chains": [
        {
            "path": "greek → arabic → latin",
            "sources": [...],
            "confidence": 0.95
        }
    ],
    "stylometric_fingerprint": {
        "author_likelihood": 0.92,
        "features": {...}
    },
    "bayesian_posterior": 0.996,
    "evidence_factors": {
        "citation_quality": 0.98,
        "temporal_distribution": 0.95,
        "translation_path": 0.92,
        "stylometric_score": 0.91,
        "network_centrality": 0.89,
        "genre_base_rate": 0.85
    }
}
```

### Report Formats

**Markdown:**
```markdown
# Reconstruction Report: Eratosthenes Geographika

**Confidence:** 99.6% (Scholarly)
**Fragments:** 12
**Sources:** 8

## Key Findings
...
```

**YAML:**
```yaml
work_id: eratosthenes_geographika
confidence: 0.996
confidence_level: scholarly
fragments:
  - id: frag_001
    text: "..."
    source: "Strabo Geography 2.1.1"
```

**JSON:**
```json
{
    "work_id": "eratosthenes_geographika",
    "confidence": 0.996,
    "fragments": [...]
}
```

## Advanced Usage

### Custom Evidence Weighting

```python
# Adjust Bayesian priors for specific research questions
engine = IntegrationEngine()

results = engine.reconstruct_work(
    work_id="Hippolytus On Heraclitus",
    evidence_factors={
        'citation_quality': 0.4,      # Emphasize source quality
        'temporal_distribution': 0.1,  # De-emphasize temporal spread
        'translation_path': 0.3,       # Focus on translation evidence
        'stylometric_score': 0.1,
        'network_centrality': 0.05,
        'genre_base_rate': 0.05
    }
)
```

### Batch Processing

```python
# Process multiple works
works = [
    'Eratosthenes Geographika',
    'Hippolytus On Heraclitus',
    'Posidippus Epigrams',
    'Callimachus Aetia'
]

results = engine.run_full_pipeline(target_works=works)
```

### Integration with External Tools

```python
# Export for Gephi
network = CitationNetwork()
network.build_from_fragments(fragments)
network.export_gephi('network.gexf')

# Export for statistical analysis
import pandas as pd

df = network.to_dataframe()
df.to_csv('citation_network.csv')
```

## Error Handling

```python
try:
    results = engine.run_full_pipeline()
except FragmentScrapingError as e:
    print(f"Failed to scrape fragments: {e}")
except CitationNetworkError as e:
    print(f"Network construction failed: {e}")
except ReconstructionError as e:
    print(f"Reconstruction failed: {e}")
except ConfidenceThresholdError as e:
    print(f"Confidence too low: {e}")
```

## Performance Tuning

```python
# For large-scale processing
engine = IntegrationEngine(
    config_path="config/high-performance.yml"
)

# config/high-performance.yml
pipeline:
  parallel_processing: true
  max_workers: 8
  batch_size: 100
  cache_enabled: true
  cache_ttl: 3600  # 1 hour
```