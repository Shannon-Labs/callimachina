"""
CALLIMACHINA v3.0: The Alexandria Reconstruction Protocol

Autonomous Digital Archaeology for Shannon-Labs

This package provides tools for:
- Predictive citation gap hunting
- Cross-lingual transmission mapping
- Bayesian confidence enhancement
- Recoverability prediction
"""

__version__ = "3.0.0"
__author__ = "Hunter Shannon"
__email__ = "hunter@shannonlabs.dev"

from .fragment_scraper import FragmentScraper
from .citation_network import CitationNetwork
from .bayesian_reconstructor import BayesianReconstructor
from .stylometric_engine import StylometricEngine
from .cross_lingual import CrossLingualMapper

__all__ = [
    "FragmentScraper",
    "CitationNetwork", 
    "BayesianReconstructor",
    "StylometricEngine",
    "CrossLingualMapper",
]