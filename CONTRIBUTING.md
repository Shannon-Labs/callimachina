# 🤝 Contributing to CALLIMACHINA

> *"The Library is not gone. It is fragmented. We are the key."*

Thank you for your interest in contributing to CALLIMACHINA! This document provides guidelines and instructions for contributing to the Alexandria Reconstruction Protocol.

## 🏛️ Project Overview

CALLIMACHINA is a digital archaeology platform that reconstructs lost classical works using Bayesian statistics, stylometry, and network analysis. It achieves scholarly-acceptable confidence levels (95-99%) for probabilistic reconstructions.

## 🚀 Quick Start for Contributors

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/callimachina.git
cd callimachina

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
python -m pytest callimachina/tests/ -v

# Run examples
cd examples && python basic_reconstruction.py
```

### Project Structure

```
callimachina/
├── callimachina/               # Core package
│   ├── src/                   # Source code
│   │   ├── cli.py            # Command-line interface
│   │   ├── database.py       # Database operations
│   │   └── ...
│   ├── tests/                # Unit tests
│   └── discoveries/          # Reconstruction outputs
├── pinakes/                  # Integration engine
│   ├── integration_engine.py
│   ├── reconstruction_engine.py
│   ├── network_builder.py
│   └── scrapers/
├── docs/                     # Documentation
├── examples/                 # Example scripts
├── website/                  # Project website
└── public_release/          # Release materials
```

## 🎯 Types of Contributions

### 1. 🔬 Reconstruction Improvements

Enhance the quality and confidence of reconstructions:

- **New Evidence Factors**: Add Bayesian evidence sources
- **Improved Scrapers**: Better fragment extraction
- **Enhanced Stylometry**: Refined author attribution
- **Better Translations**: Improved cross-lingual mapping

**Example: Adding an Evidence Factor**

```python
# In pinakes/confidence_enhancer.py
class ConfidenceEnhancer:
    def add_evidence_factor(self, factor_name, weight, scoring_function):
        """Add a new Bayesian evidence factor."""
        self.evidence_factors[factor_name] = {
            'weight': weight,
            'score': scoring_function
        }
```

### 2. 💻 Code Contributions

- **Bug Fixes**: Fix issues and improve stability
- **Performance**: Optimize pipeline execution
- **Features**: Add new functionality
- **Refactoring**: Improve code quality

**Example: Performance Optimization**

```python
# Use caching for repeated operations
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(fragment_id):
    # Cache results to avoid recomputation
    return process_fragment(fragment_id)
```

### 3. 📚 Documentation

- **API Docs**: Improve documentation
- **Tutorials**: Create guided examples
- **Methodology**: Explain statistical approaches
- **Gallery**: Showcase reconstructions

**Example: Adding a Tutorial**

```markdown
# Create in docs/tutorials/
# Use Jupyter notebooks for interactive examples
# Include visualizations and explanations
```

### 4. 🏺 Classical Scholarship

- **Fragment Identification**: Find new sources
- **Source Verification**: Validate citations
- **Translation Analysis**: Document transmission
- **Historical Context**: Provide scholarly background

**Example: Contributing Fragment Data**

```yaml
# Add to pinakes/fragments/
fragment_id: new_fragment_001
work: Eratosthenes Geographika
text: "Fragment text here..."
source: "Strabo Geography 2.1.1"
language: greek
date: "1st century CE"
reliability: high
```

## 📝 Contribution Process

### 1. Find an Issue

- Check [GitHub Issues](https://github.com/Shannon-Labs/callimachina/issues)
- Look for issues labeled `good first issue` or `help wanted`
- For reconstruction requests, use the reconstruction template

### 2. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/add-xyz-evidence

# Or a bugfix branch
git checkout -b bugfix/fix-scraper-timeout
```

### 3. Make Changes

Follow these guidelines:

#### Code Style

- **Black** for code formatting (max line length: 100)
- **Flake8** for linting
- **Type hints** encouraged
- **Docstrings** for all public functions

```python
# Example function
def calculate_confidence(fragment: Fragment, 
                        evidence_factors: Dict[str, float]) -> float:
    """
    Calculate Bayesian confidence for a fragment.
    
    Args:
        fragment: Fragment object with metadata
        evidence_factors: Dictionary of evidence factor scores
        
    Returns:
        float: Confidence score between 0 and 1
    """
    # Implementation here
    pass
```

#### Testing

- Write tests for new functionality
- Ensure existing tests pass
- Use pytest for testing
- Aim for >80% coverage

```python
# Example test
def test_confidence_calculation():
    """Test confidence calculation with known inputs."""
    fragment = Fragment(id="test_001", text="Example")
    factors = {"citation_quality": 0.9, "temporal": 0.8}
    
    confidence = calculate_confidence(fragment, factors)
    assert 0.7 <= confidence <= 1.0
```

#### Documentation

- Update relevant documentation
- Add docstrings to new functions
- Include examples in docstrings
- Update API reference if needed

### 4. Test Thoroughly

```bash
# Run all tests
python -m pytest callimachina/tests/ -v

# Run specific test file
python -m pytest callimachina/tests/test_v3_infrastructure.py -v

# Check coverage
python -m pytest --cov=callimachina --cov-report=html

# Run examples
cd examples && python basic_reconstruction.py

# Test reconstruction quality
python pinakes/integration_engine.py
```

### 5. Submit Pull Request

1. Push your branch to GitHub
2. Create a Pull Request using the template
3. Fill out the PR description completely
4. Link any related issues
5. Wait for review and address feedback

**PR Checklist:**

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Examples run successfully
- [ ] Reconstruction quality verified (if applicable)
- [ ] No new warnings generated

## 🏺 Reconstruction-Specific Guidelines

### Adding a New Work for Reconstruction

1. **Research Phase**
   - Identify all known fragments
   - Document citation sources
   - Map translation chains
   - Assess evidence quality

2. **Data Preparation**
   ```yaml
   # Create work metadata
   work_id: author_work_name
   title: "Full Work Title"
   author: "Author Name"
   date: "Approximate Date"
   genre: "Genre/Type"
   fragments: []
   citations: []
   translations: []
   ```

3. **Testing Phase**
   - Run reconstruction pipeline
   - Verify confidence scores
   - Validate fragment matching
   - Review network analysis

4. **Documentation**
   - Write scholarly apparatus
   - Document evidence sources
   - Explain methodology
   - Note limitations

### Confidence Threshold Guidelines

| Confidence | Level | Scholarly Acceptance |
|------------|-------|---------------------|
| < 70% | Low | Not suitable for publication |
| 70-85% | Medium | Preliminary analysis only |
| 85-95% | High | Conference/working paper |
| 95-99% | Scholarly | Journal publication ready |
| > 99% | Exceptional | High confidence reconstruction |

## 🎓 Best Practices

### For Classicists

- **Document sources meticulously**
- **Note textual variants**
- **Explain historical context**
- **Acknowledge uncertainty**
- **Follow scholarly conventions**

### For Developers

- **Write readable code**
- **Comment complex algorithms**
- **Test edge cases**
- **Consider performance**
- **Maintain backwards compatibility**

### For Data Scientists

- **Validate statistical methods**
- **Document assumptions**
- **Test significance**
- **Visualize uncertainty**
- **Reproducible results**

## 🤝 Community Guidelines

### Code of Conduct

- **Be respectful** to all contributors
- **Welcome newcomers** and help them get started
- **Assume good intent** in discussions
- **Focus on constructive** criticism
- **Celebrate contributions** of all sizes

### Getting Help

- **Documentation**: Check docs/ first
- **Issues**: Search existing issues
- **Discussions**: Use GitHub Discussions
- **Chat**: [Add communication channel]

### Recognition

Contributors are recognized in:
- **README.md** contributors section
- **Release notes** for significant contributions
- **Citation** in academic publications
- **Project history** documentation

## 📊 Release Process

### Version Numbering

We use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes or major reconstructions
- **MINOR**: New features or improvements
- **PATCH**: Bug fixes and minor updates

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Examples verified
- [ ] Reconstructions validated
- [ ] Changelog updated
- [ ] Version bumped
- [ ] GitHub release created

## 🏆 Recognition System

### Contributor Levels

- **Contributor**: 1-5 contributions
- **Regular Contributor**: 6-20 contributions
- **Core Contributor**: 21+ contributions
- **Maintainer**: Sustained contributions + reviews

### Contribution Types

- **Code**: Features, bug fixes, optimizations
- **Documentation**: Guides, tutorials, API docs
- **Research**: Fragments, citations, analysis
- **Review**: PR reviews, issue triage
- **Community**: Support, outreach, events

## 📚 Resources

- **[Getting Started](docs/GETTING_STARTED.md)** - Beginner's guide
- **[API Reference](docs/API_REFERENCE.md)** - Technical documentation
- **[Methodology](docs/METHODOLOGY.md)** - Statistical approach
- **[Examples](examples/)** - Practical tutorials
- **[Gallery](callimachina/discoveries/)** - Browse reconstructions

## 🙏 Thank You!

Your contributions help restore the lost knowledge of antiquity. Every fragment recovered, every citation mapped, and every confidence score improved brings us closer to understanding our intellectual heritage.

**The Library is not gone. It is fragmented. Together, we are the key.**

---

*For questions about contributing, please open an issue or discussion on GitHub.*