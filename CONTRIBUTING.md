# Contributing to CALLIMACHINA: The Alexandria Reconstruction Protocol

Thank you for your interest in contributing to CALLIMACHINA! This document provides guidelines and instructions for contributing to the project.

## 🎯 **Our Mission**

CALLIMACHINA aims to reconstruct the lost intellectual superstructure of the Library of Alexandria by hunting for bibliographic ghosts—reconstructing texts, authors, and knowledge graphs from surviving fragments, citations, palimpsests, and cross-cultural translations.

## 🤝 **Ways to Contribute**

### **1. Add New Fragments** 📜

**What:** Submit papyrus fragments, inscriptions, or manuscript data  
**How:** 
- Add YAML files to `pinakes/fragments/`
- Include metadata: provenance, date, text, language
- Follow DDbDP format standards

**Example:**
```yaml
id: papyri.oxy.4.654
author: Posidippus
text: "...on the statue of the queen, a dedication..."
date_range: "c. 1st century CE"
collection: oxy
language: greek
```

### **2. Improve Citations** 🔍

**What:** Expand citation sources and translation database  
**How:**
- Edit `citation_triangulator.py`
- Add new ancient sources
- Expand known translation chains
- Improve citation pattern matching

### **3. Enhance Stylometry** 🔬

**What:** Add author fingerprints and improve attribution algorithms  
**How:**
- Add extant text corpora to `stylometry_enhanced.py`
- Improve feature extraction methods
- Refine Burrows' Delta implementation
- Test on known anonymous fragments

### **4. Web Development** 🌐

**What:** Improve the web interface and visualizations  
**How:**
- Enhance D3.js network visualizations
- Improve fragment browser UI
- Add interactive confidence dashboards
- Mobile responsiveness

### **5. Documentation** 📝

**What:** Write tutorials, improve docs, create examples  
**How:**
- Expand `docs/` directory
- Create Jupyter notebooks
- Write methodology papers
- Make video tutorials

### **6. Testing** 🧪

**What:** Write tests, validate outputs, find edge cases  
**How:**
- Add pytest tests to `tests/`
- Validate reconstruction outputs
- Test edge cases in citation patterns
- Performance benchmarking

## 🚀 **Getting Started**

### **Prerequisites**

- Python 3.8 or higher
- Git
- Basic understanding of classical studies (helpful but not required)

### **Setup Development Environment**

1. **Fork the repository**
   ```bash
   git fork https://github.com/yourusername/callimachina.git
   cd callimachina
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Run tests**
   ```bash
   pytest tests/ -v
   ```

5. **Make your changes**
   ```bash
   git checkout -b feature/your-feature-name
   # Make your changes
   ```

6. **Test your changes**
   ```bash
   python pinakes/integration_engine.py
   ```

7. **Submit pull request**
   ```bash
   git add .
   git commit -m "Add your feature"
   git push origin feature/your-feature-name
   # Create pull request on GitHub
   ```

## 📋 **Contribution Guidelines**

### **Code Style**

- Follow PEP 8 Python style guide
- Use Black for code formatting
- Maximum line length: 100 characters
- Use type hints where appropriate

```bash
# Format your code
black pinakes/

# Check linting
flake8 pinakes/ --max-line-length=100
```

### **Commit Messages**

Use clear, descriptive commit messages:

```
feat: add Arabic translation hunter
fix: correct citation date parsing
docs: update methodology section
test: add stylometry unit tests
```

### **Pull Request Process**

1. **Update documentation**
   - Update README.md if needed
   - Add docstrings to new functions
   - Update API reference

2. **Add tests**
   - Write tests for new functionality
   - Ensure all tests pass
   - Maintain or improve code coverage

3. **Describe your changes**
   - Clear PR title and description
   - Reference any related issues
   - Include before/after examples

4. **Request review**
   - Tag relevant maintainers
   - Respond to feedback
   - Make requested changes

### **Testing Requirements**

```python
# Example test structure
def test_citation_triangulation():
    """Test citation triangulation with known data"""
    triangulator = CitationTriangulator()
    result = triangulator.triangulate_lost_work('Eratosthenes Geographika')
    
    assert result is not None
    assert result['citation_count'] == 4
    assert result['priority_score'] >= 90
```

Run tests with coverage:
```bash
pytest tests/ -v --cov=pinakes --cov-report=html
```

## 🏛️ **Classical Studies Guidelines**

### **Fragment Attribution**

- **DO** include full provenance information
- **DO** cite primary sources for all claims
- **DO** use standard abbreviations (P.Oxy., P.Herc., etc.)
- **DON'T** make speculative attributions without confidence scores
- **DON'T** ignore contradictory evidence

### **Translation Documentation**

- **DO** specify translator, date, and manuscript
- **DO** note translation type (literal, paraphrase, summary)
- **DO** document translation chains
- **DON'T** assume translations are complete
- **DON'T** ignore Syriac intermediaries

### **Confidence Scoring**

- **DO** provide component breakdowns
- **DO** update scores with new evidence
- **DO** flag low-confidence attributions
- **DON'T** present speculation as fact
- **DON'T** suppress uncertainty

## 🔬 **Technical Guidelines**

### **Adding New Modules**

1. **Create module file**
   ```bash
   touch pinakes/your_new_module.py
   ```

2. **Follow template structure**
   ```python
   #!/usr/bin/env python3
   """
   Your Module Description
   
   Detailed explanation of purpose and methodology
   """
   
   class YourModule:
       def __init__(self):
           """Initialize module"""
           pass
       
       def your_method(self):
           """Document all methods"""
           pass
   ```

3. **Add integration points**
   - Update `integration_engine.py`
   - Add configuration options
   - Test with existing pipeline

4. **Write tests**
   ```bash
   touch tests/test_your_module.py
   ```

### **Performance Considerations**

- **DO** use generators for large datasets
- **DO** implement caching where appropriate
- **DO** profile slow operations
- **DON'T** make unnecessary API calls
- **DON'T** load entire corpora into memory

### **API Design**

- **DO** provide clear, documented interfaces
- **DO** return standardized formats (YAML, JSON)
- **DO** handle errors gracefully
- **DON'T** break existing APIs without deprecation
- **DON'T** expose internal implementation details

## 🌐 **Web Development**

### **Website Structure**

```
website/
├── index.html              # Main dashboard
├── reconstructions.html    # Browse reconstructions
├── fragments.html          # Fragment browser
├── network.html           # Network visualization
├── translations.html      # Translation explorer
├── css/
│   └── style.css          # Main styles
└── js/
    ├── app.js             # Main application
    ├── api.js             # API client
    └── network.js         # Network visualization
```

### **Web Development Guidelines**

- Use semantic HTML5
- Ensure accessibility (ARIA labels, keyboard navigation)
- Mobile-responsive design
- Progressive enhancement
- Optimized performance

### **Testing Web Interface**

```bash
cd website
python -m http.server 8000
# Open http://localhost:8000
```

## 📚 **Documentation Guidelines**

### **Code Documentation**

```python
def calculate_confidence(self, reconstruction: Dict) -> float:
    """
    Calculate enhanced confidence using Bayesian updating.
    
    Args:
        reconstruction: Dictionary containing reconstruction data
        
    Returns:
        Enhanced confidence score between 0 and 1
        
    Raises:
        ValueError: If reconstruction format is invalid
        
    Example:
        >>> confidence = calculator.calculate_confidence(recon)
        >>> print(f"Confidence: {confidence:.1%}")
    """
    # Implementation
```

### **User Documentation**

- Update README.md for major changes
- Add examples to `docs/examples/`
- Maintain API reference
- Create tutorials for common tasks

## 🤔 **Getting Help**

### **Before Asking**

1. Check existing documentation
2. Search closed issues
3. Run tests to isolate problems
4. Create minimal reproducible example

### **Where to Ask**

- **Bug Reports:** [GitHub Issues](https://github.com/yourusername/callimachina/issues)
- **Feature Requests:** [GitHub Discussions](https://github.com/yourusername/callimachina/discussions)
- **General Questions:** Classical studies forums with CALLIMACHINA tag

### **Good Question Template**

```
**Problem:** Clear description of issue
**Context:** What you're trying to achieve
**Code:** Minimal reproducible example
**Error:** Full error message and traceback
**Environment:** Python version, OS, dependencies
**Attempts:** What you've tried already
```

## 🎉 **Recognition**

### **Contributors**

- Listed in CONTRIBUTORS.md
- Recognized in release notes
- Profile on project website
- Academic citation for significant contributions

### **Academic Citations**

If you use CALLIMACHINA in research:

```bibtex
@software{callimachina2025,
  title={CALLIMACHINA: The Alexandria Reconstruction Protocol v2.0},
  author={Your Name and Contributors},
  year={2025},
  url={https://github.com/yourusername/callimachina},
  note={Contribution: [Your specific contribution]}
}
```

## 📈 **Project Roadmap**

### **Phase 1: Core System** ✅ COMPLETE
- ✅ Pipeline architecture
- ✅ Bayesian confidence enhancement
- ✅ Stylometric fingerprinting
- ✅ Cross-cultural tracking
- ✅ Network visualization

### **Phase 2: Scale & Integration** 🔄 IN PROGRESS
- 🔄 TLG API integration
- 🔄 Live papyri.info connection
- 🔄 Multispectral imaging support
- 🔄 Community contribution system

### **Phase 3: Community & Research** 📋 PLANNED
- 📋 Peer review platform
- 📋 Collaborative editing
- 📋 Journal integration
- 📋 Teaching materials

## 🏛️ **Core Principles**

### **1. Scholarly Rigor**
- All reconstructions include confidence scores
- Full provenance tracking
- Transparent methodology
- Peer review ready

### **2. Open Science**
- Open source code
- Open data formats
- Reproducible results
- Community driven

### **3. Cross-Cultural Awareness**
- Track all transmission paths
- Respect cultural contexts
- Document translation chains
- Acknowledge intermediaries

### **4. Continuous Improvement**
- Update with new fragments
- Refine confidence models
- Incorporate new research
- Learn from corrections

## 📞 **Contact**

- **Issues:** [GitHub Issues](https://github.com/yourusername/callimachina/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/callimachina/discussions)
- **Email:** callimachina@alexandria.org
- **Mailing List:** callimachina-announce@alexandria.org

---

<p align="center">
  <i>🏛️ The Library endures in fragments. Your contributions help reconstruct it verse by verse. 🏛️</i>
</p>

---

**Thank you for contributing to CALLIMACHINA!**

*Last updated: 2025-11-06*  
*Version: 2.0*  
*Maintainers: CALLIMACHINA Development Team*
