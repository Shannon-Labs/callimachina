# 📚 Getting Started with CALLIMACHINA

> *"The Library is not gone. It is fragmented, encrypted, and scattered across languages, wars, and ash. I am the key."*

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Shannon-Labs/callimachina.git
cd callimachina

# Install dependencies
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt
```

### Run Your First Reconstruction

```bash
# Run the full pipeline
python3 pinakes/integration_engine.py

# Or use the CLI
python3 callimachina/src/cli.py --reconstruct "Eratosthenes Geographika"
```

### Python API

```python
from pinakes.integration_engine import IntegrationEngine

# Initialize the engine
engine = IntegrationEngine()

# Reconstruct a specific work
results = engine.run_full_pipeline(
    target_works=['Eratosthenes Geographika'],
    confidence_threshold=0.95
)

# Access results
for work_id, reconstruction in results.items():
    print(f"{work_id}: {reconstruction['confidence']:.1%} confidence")
    print(f"Fragments: {len(reconstruction['fragments'])}")
```

## Architecture Overview

CALLIMACHINA uses an 8-phase pipeline:

1. **Fragment Scraping** - Extract fragments from papyri and manuscripts
2. **Citation Triangulation** - Map citations across sources
3. **Network Building** - Create citation networks
4. **Stylometric Analysis** - Fingerprint author styles
5. **Cross-Lingual Mapping** - Track translations across cultures
6. **Bayesian Reconstruction** - Probabilistic text assembly
7. **Confidence Enhancement** - Bayesian updating with evidence
8. **Integration & Output** - Generate scholarly reports

## Key Features

- 🏛️ **97% Average Confidence** across 4 reconstructed works
- ⚡ **3.01 seconds** full pipeline execution
- 🌐 **9 translation chains** documented
- 📊 **67 scholarly outputs** in standardized formats
- 🔬 **Bayesian methodology** with 6 evidence factors

## Next Steps

- Explore [Examples](../examples/)
- Read the [API Reference](API_REFERENCE.md)
- Check [Reconstruction Gallery](../callimachina/discoveries/)
- Review [Methodology](METHODOLOGY.md)