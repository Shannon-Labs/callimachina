"""
CrossLingualMapper: Arabic and Syriac corpus integration for translation chain analysis.

Queries multiple linguistic corpora to map:
- Greek→Syriac translation patterns
- Syriac→Arabic transmission routes  
- Arabic→Latin reception history
- Cross-lingual citation patterns
"""

import requests
import json
import time
import logging
from typing import Dict, List, Optional, Tuple, Any
from urllib.parse import urljoin, quote
import re
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np


class CrossLingualMapper:
    def __init__(self, rate_limit: float = 1.0, timeout: int = 30):
        """
        Initialize the cross-lingual mapper.
        
        Args:
            rate_limit: Seconds to wait between requests
            timeout: Request timeout in seconds
        """
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CALLIMACHINA v3.0 (Digital Archaeology Project)'
        })
        
        # Corpus endpoints
        self.corpus_endpoints = {
            'openiti': 'https://raw.githubusercontent.com/OpenITI',
            'syriaca': 'http://www.syriaca.org',
            'knowledge4all': 'https://knowledge4all.org',
            'persee': 'https://www.persee.fr',
            'alcorpus': 'https://arabiccorpus.qatar.cmu.edu',
        }
        
        # Translation center coordinates for mapping
        self.translation_centers = {
            'baghdad': {'lat': 33.3152, 'lon': 44.3661, 'period': '750-1258 CE'},
            'damascus': {'lat': 33.5138, 'lon': 36.2765, 'period': '661-750 CE'},
            'cairo': {'lat': 30.0444, 'lon': 31.2357, 'period': '969-1517 CE'},
            'cordoba': {'lat': 37.8882, 'lon': -4.7794, 'period': '756-1031 CE'},
            'toledo': {'lat': 39.8581, 'lon': -4.0226, 'period': '1085-1492 CE'},
            'edessa': {'lat': 37.1500, 'lon': 38.8000, 'period': '200-1146 CE'},
            'nisbis': {'lat': 37.0667, 'lon': 41.2167, 'period': '350-800 CE'},
            'gundishapur': {'lat': 32.3209, 'lon': 48.5154, 'period': '300-900 CE'},
        }
        
        self.logger = logging.getLogger(__name__)
        
    def _rate_limited_request(self, url: str, **kwargs) -> Optional[requests.Response]:
        """Make a rate-limited HTTP request."""
        time.sleep(self.rate_limit)
        try:
            response = self.session.get(url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"Request failed for {url}: {e}")
            return None
    
    def query_arabic_corpus(self, query: str, corpus: str = 'openiti', 
                           max_results: int = 50) -> List[Dict]:
        """
        Query Arabic corpus for references to Greek works.
        
        Args:
            query: Search query (author name, work title, or concept)
            corpus: Corpus to query ('openiti', 'alcorpus', 'persee')
            max_results: Maximum results to return
            
        Returns:
            List of matching passages
        """
        if corpus == 'openiti':
            return self._query_openiti(query, max_results)
        elif corpus == 'alcorpus':
            return self._query_alcorpus(query, max_results)
        elif corpus == 'persee':
            return self._query_persee(query, max_results)
        else:
            self.logger.warning(f"Unknown Arabic corpus: {corpus}")
            return []
    
    def _query_openiti(self, query: str, max_results: int) -> List[Dict]:
        """Query OpenITI corpus."""
        # OpenITI uses GitHub repository structure
        base_url = f"{self.corpus_endpoints['openiti']}/master/data"
        
        # For demonstration, we'll use a simplified approach
        # In practice, this would query the actual OpenITI API
        
        # Arabic transliterations of Greek authors
        arabic_names = self._get_arabic_transliterations(query)
        
        results = []
        
        for ar_name in arabic_names[:3]:  # Limit to top 3 variations
            search_url = f"{base_url}/search?q={quote(ar_name)}"
            response = self._rate_limited_request(search_url)
            
            if response:
                try:
                    data = response.json()
                    for item in data.get('results', [])[:max_results]:
                        result = {
                            'text': item.get('text', ''),
                            'author': item.get('author', ''),
                            'title': item.get('title', ''),
                            'source': 'openiti',
                            'language': 'arabic',
                            'confidence': 0.7,
                            'manuscript_info': item.get('manuscript', {}),
                            'greek_original': query
                        }
                        results.append(result)
                except (json.JSONDecodeError, KeyError):
                    pass
        
        self.logger.info(f"Found {len(results)} results from OpenITI for '{query}'")
        return results
    
    def _get_arabic_transliterations(self, greek_name: str) -> List[str]:
        """Get Arabic transliterations of Greek names."""
        # This is a simplified mapping
        # In practice, this would use a comprehensive database
        
        transliteration_map = {
            'Aristotle': ['أرسطو', 'أرسطوطاليس', 'Aristu', 'Aristutalis'],
            'Galen': ['جالينوس', 'جالين', 'Galinus', 'Galen'],
            'Ptolemy': ['بطليموس', 'Ptolemaios', 'Batlamyus'],
            'Euclid': ['إقليدس', 'Uqlidis'],
            'Hippocrates': ['أبقراط', 'Abuqrat'],
            'Plato': ['أفلاطون', 'Aflatun'],
            'Plotinus': ['بلوتينوس', 'Plotinus'],
            'Proclus': ['بروكلوس', 'Proclus'],
        }
        
        # Return transliterations or the original name if not found
        return transliteration_map.get(greek_name, [greek_name])
    
    def _query_alcorpus(self, query: str, max_results: int) -> List[Dict]:
        """Query Arabic Corpus (Qatar Computing Research Institute)."""
        base_url = self.corpus_endpoints['alcorpus']
        params = {
            'query': query,
            'limit': max_results,
            'format': 'json'
        }
        
        response = self._rate_limited_request(base_url, params=params)
        
        if not response:
            return []
        
        try:
            data = response.json()
            results = []
            
            for item in data.get('results', [])[:max_results]:
                result = {
                    'text': item.get('passage', ''),
                    'source': item.get('source', ''),
                    'author': item.get('author', ''),
                    'date': item.get('date', ''),
                    'corpus': 'alcorpus',
                    'language': 'arabic',
                    'confidence': item.get('confidence', 0.6),
                    'greek_original': query
                }
                results.append(result)
            
            return results
            
        except (json.JSONDecodeError, KeyError) as e:
            self.logger.error(f"Failed to parse alcorpus response: {e}")
            return []
    
    def _query_persee(self, query: str, max_results: int) -> List[Dict]:
        """Query Persee for Arabic/French scholarship."""
        base_url = f"{self.corpus_endpoints['persee']}/search"
        params = {
            'q': query,
            'fq': 'language:ar',
            'rows': max_results,
            'format': 'json'
        }
        
        response = self._rate_limited_request(base_url, params=params)
        
        if not response:
            return []
        
        try:
            data = response.json()
            results = []
            
            for doc in data.get('response', {}).get('docs', [])[:max_results]:
                result = {
                    'title': doc.get('title', ''),
                    'abstract': doc.get('abstract', ''),
                    'author': doc.get('author', ''),
                    'journal': doc.get('journal', ''),
                    'year': doc.get('year', ''),
                    'source': 'persee',
                    'language': doc.get('language', 'ar'),
                    'confidence': 0.8,
                    'greek_original': query
                }
                results.append(result)
            
            return results
            
        except (json.JSONDecodeError, KeyError) as e:
            self.logger.error(f"Failed to parse Persee response: {e}")
            return []
    
    def query_syriac_corpus(self, query: str, max_results: int = 50) -> List[Dict]:
        """
        Query Syriac corpus for Greek text transmissions.
        
        Args:
            query: Search query
            max_results: Maximum results
            
        Returns:
            List of Syriac text references
        """
        base_url = f"{self.corpus_endpoints['syriaca']}/search"
        params = {
            'q': query,
            'limit': max_results,
            'format': 'json'
        }
        
        response = self._rate_limited_request(base_url, params=params)
        
        if not response:
            return []
        
        try:
            data = response.json()
            results = []
            
            for item in data.get('results', [])[:max_results]:
                result = {
                    'text': item.get('text', ''),
                    'author': item.get('author', ''),
                    'title': item.get('title', ''),
                    'manuscript': item.get('manuscript', ''),
                    'date': item.get('date', ''),
                    'source': 'syriaca',
                    'language': 'syriac',
                    'confidence': item.get('confidence', 0.7),
                    'translator': item.get('translator', ''),
                    'greek_original': query
                }
                results.append(result)
            
            self.logger.info(f"Found {len(results)} Syriac references for '{query}'")
            return results
            
        except (json.JSONDecodeError, KeyError) as e:
            self.logger.error(f"Failed to parse Syriaca response: {e}")
            return []
    
    def map_translation_chain(self, greek_work: str) -> Dict[str, Any]:
        """
        Map the complete translation chain for a Greek work.
        
        Args:
            greek_work: Greek work identifier (e.g., 'Aristotle.Metaphysics')
            
        Returns:
            Translation chain dictionary
        """
        self.logger.info(f"Mapping translation chain for {greek_work}")
        
        # Query different corpora
        syriac_refs = self.query_syriac_corpus(greek_work)
        arabic_refs = self.query_arabic_corpus(greek_work)
        
        # Analyze translation patterns
        chain = {
            'greek_original': greek_work,
            'syriac_intermediary': self._analyze_syriac_links(syriac_refs, greek_work),
            'arabic_translation': self._analyze_arabic_links(arabic_refs, greek_work),
            'latin_translation': self._analyze_latin_reception(greek_work),
            'transmission_score': 0.0,
            'confidence': 0.0
        }
        
        # Calculate transmission score
        chain['transmission_score'] = self._calculate_transmission_score(chain)
        chain['confidence'] = self._calculate_chain_confidence(chain)
        
        return chain
    
    def _analyze_syriac_links(self, syriac_refs: List[Dict], 
                             greek_work: str) -> Optional[Dict]:
        """Analyze Syriac translation links."""
        if not syriac_refs:
            return None
        
        # Group by translator and manuscript
        translator_groups = {}
        for ref in syriac_refs:
            translator = ref.get('translator', 'Unknown')
            if translator not in translator_groups:
                translator_groups[translator] = []
            translator_groups[translator].append(ref)
        
        # Find the most reliable translation
        best_translator = max(translator_groups.keys(), 
                            key=lambda t: len(translator_groups[t]))
        best_refs = translator_groups[best_translator]
        
        return {
            'translator': best_translator,
            'references': best_refs,
            'reference_count': len(best_refs),
            'manuscripts': list(set(ref.get('manuscript', '') for ref in best_refs)),
            'date_range': self._estimate_date_range(best_refs),
            'confidence': min(len(best_refs) * 0.1, 0.9)
        }
    
    def _analyze_arabic_links(self, arabic_refs: List[Dict], 
                             greek_work: str) -> Optional[Dict]:
        """Analyze Arabic translation links."""
        if not arabic_refs:
            return None
        
        # Filter for direct translations (not just references)
        translations = [ref for ref in arabic_refs if 'translation' in ref.get('title', '').lower() or 
                       'ترجمة' in ref.get('title', '')]
        
        if not translations:
            translations = arabic_refs  # Fallback to all references
        
        # Extract translators and dates
        translators = list(set(ref.get('author', 'Unknown') for ref in translations))
        dates = [ref.get('date', '') for ref in translations if ref.get('date')]
        
        return {
            'translators': translators,
            'references': translations,
            'reference_count': len(translations),
            'manuscripts': list(set(ref.get('manuscript_info', {}).get('id', '') for ref in translations)),
            'date_range': self._estimate_date_range(translations),
            'confidence': min(len(translations) * 0.08, 0.85)
        }
    
    def _analyze_latin_reception(self, greek_work: str) -> Optional[Dict]:
        """Analyze Latin translation/reception."""
        # This would query Latin corpora
        # For now, return a placeholder based on known translation patterns
        
        known_latin_translations = {
            'Aristotle.Metaphysics': {
                'translator': 'William of Moerbeke',
                'date': '1260 CE',
                'location': 'Bruges'
            },
            'Aristotle.PosteriorAnalytics': {
                'translator': 'James of Venice',
                'date': '1125 CE',
                'location': 'Venice'
            },
            'Galen.OnAnatomicalProcedures': None,  # No known Latin translation
        }
        
        return known_latin_translations.get(greek_work, {
            'translator': 'Unknown',
            'date': 'Unknown',
            'location': 'Unknown',
            'note': 'Latin translation not well documented'
        })
    
    def _estimate_date_range(self, refs: List[Dict]) -> str:
        """Estimate date range from references."""
        dates = []
        for ref in refs:
            date_str = ref.get('date', '')
            # Extract year from date string (simplified)
            year_match = re.search(r'(\d{3,4})', date_str)
            if year_match:
                dates.append(int(year_match.group(1)))
        
        if not dates:
            return 'Unknown'
        
        return f"{min(dates)}-{max(dates)} CE"
    
    def _calculate_transmission_score(self, chain: Dict) -> float:
        """Calculate transmission pathway score (0-1)."""
        score = 0.0
        
        # Syriac intermediary bonus
        if chain.get('syriac_intermediary'):
            score += 0.3
            syriac_conf = chain['syriac_intermediary'].get('confidence', 0)
            score += syriac_conf * 0.2
        
        # Arabic translation bonus
        if chain.get('arabic_translation'):
            score += 0.3
            arabic_conf = chain['arabic_translation'].get('confidence', 0)
            score += arabic_conf * 0.2
        
        # Latin translation bonus
        if chain.get('latin_translation'):
            score += 0.2
        
        return min(score, 1.0)
    
    def _calculate_chain_confidence(self, chain: Dict) -> float:
        """Calculate overall chain confidence."""
        confidences = []
        
        if chain.get('syriac_intermediary'):
            confidences.append(chain['syriac_intermediary'].get('confidence', 0))
        
        if chain.get('arabic_translation'):
            confidences.append(chain['arabic_translation'].get('confidence', 0))
        
        if not confidences:
            return 0.0
        
        return np.mean(confidences)
    
    def identify_translation_centers(self) -> Dict[str, Dict]:
        """
        Identify major translation centers and their characteristics.
        
        Returns:
            Dictionary of translation centers
        """
        centers = {}
        
        for name, coords in self.translation_centers.items():
            center = {
                'name': name,
                'coordinates': coords,
                'works_translated': self._get_works_translated_at_center(name),
                'translators_active': self._get_translators_at_center(name),
                'transmission_score': self._calculate_center_transmission_score(name),
                'manuscripts_preserved': self._estimate_manuscripts_at_center(name)
            }
            centers[name] = center
        
        return centers
    
    def _get_works_translated_at_center(self, center: str) -> List[str]:
        """Get works translated at a specific center."""
        # This would query a database of translations
        # For now, return known examples
        
        center_works = {
            'baghdad': [
                'Aristotle.Metaphysics',
                'Galen.OnAnatomicalProcedures',
                'Ptolemy.Almagest',
                'Euclid.Elements'
            ],
            'toledo': [
                'Aristotle.Metaphysics',
                'Avicenna.Canon',
                'Alkhwarizmi.Algebra'
            ],
            'edessa': [
                'Aristotle.Categories',
                'Porphyry.Isagoge',
                'Hippocrates.Aphorisms'
            ]
        }
        
        return center_works.get(center, [])
    
    def _get_translators_at_center(self, center: str) -> List[str]:
        """Get known translators at a center."""
        translators = {
            'baghdad': ['Hunayn ibn Ishaq', 'Ishaq ibn Hunayn', 'Qusta ibn Luqa'],
            'toledo': ['Gerard of Cremona', 'John of Seville', 'Dominicus Gundissalinus'],
            'edessa': ['Sergius of Reshaina', 'Aitalaha'],
            'damascus': ['Yahya ibn Adi', 'Ibn al-Nadim'],
            'cairo': ['Ibn al-Haytham', 'Moses Maimonides'],
            'cordoba': ['Averroes', 'Ibn Tufayl'],
        }
        
        return translators.get(center, [])
    
    def _calculate_center_transmission_score(self, center: str) -> float:
        """Calculate transmission importance score for a center."""
        works = len(self._get_works_translated_at_center(center))
        translators = len(self._get_translators_at_center(center))
        
        # Normalize scores
        work_score = min(works / 20, 1.0)  # 20+ works = max score
        translator_score = min(translators / 10, 1.0)  # 10+ translators = max score
        
        return (work_score * 0.6 + translator_score * 0.4)
    
    def _estimate_manuscripts_at_center(self, center: str) -> int:
        """Estimate manuscripts preserved at a center."""
        # Rough estimates based on historical records
        manuscript_estimates = {
            'baghdad': 10000,  # House of Wisdom
            'cairo': 8000,     # Dar al-Hikma
            'cordoba': 6000,   # Caliphal library
            'toledo': 3000,    # Cathedral library
            'edessa': 2000,    # School of Edessa
            'damascus': 2500,  # Umayyad library
            'nisbis': 1500,    # School of Nisibis
            'gundishapur': 2000,  # Academy
        }
        
        return manuscript_estimates.get(center, 1000)
    
    def generate_priority_queue(self, greek_works: List[str]) -> pd.DataFrame:
        """
        Generate priority queue based on cross-lingual transmission evidence.
        
        Args:
            greek_works: List of Greek works to analyze
            
        Returns:
            DataFrame with ranked works
        """
        priorities = []
        
        for work in greek_works:
            chain = self.map_translation_chain(work)
            
            priority_score = (
                chain['transmission_score'] * 0.4 +
                chain['confidence'] * 0.3 +
                self._get_network_centrality(work) * 0.2 +
                self._get_fragment_availability(work) * 0.1
            )
            
            priorities.append({
                'work': work,
                'transmission_score': chain['transmission_score'],
                'confidence': chain['confidence'],
                'has_syriac': chain['syriac_intermediary'] is not None,
                'has_arabic': chain['arabic_translation'] is not None,
                'has_latin': chain['latin_translation'] is not None,
                'priority_score': priority_score,
                'search_strategy': self._generate_search_strategy(chain)
            })
        
        df = pd.DataFrame(priorities)
        if not df.empty:
            df = df.sort_values('priority_score', ascending=False).reset_index(drop=True)
        
        return df
    
    def _get_network_centrality(self, work: str) -> float:
        """Get network centrality for a work (placeholder)."""
        # This would integrate with CitationNetwork
        return 0.5
    
    def _get_fragment_availability(self, work: str) -> float:
        """Get fragment availability score (placeholder)."""
        # This would integrate with FragmentScraper
        return 0.3
    
    def _generate_search_strategy(self, chain: Dict) -> str:
        """Generate search strategy based on chain analysis."""
        strategies = []
        
        if chain.get('syriac_intermediary'):
            strategies.append("Syriac manuscript collections")
        
        if chain.get('arabic_translation'):
            strategies.append("Arabic scientific manuscripts")
        
        if chain.get('latin_translation'):
            strategies.append("Medieval Latin translations")
        
        if not strategies:
            strategies.append("Cross-lingual citation analysis")
        
        return " + ".join(strategies[:2])
    
    def export_translation_network(self, output_file: str):
        """
        Export translation network for visualization.
        
        Args:
            output_file: Output file path
        """
        # Create network data structure
        network = {
            'nodes': [],
            'edges': []
        }
        
        # Add translation centers as nodes
        for name, coords in self.translation_centers.items():
            network['nodes'].append({
                'id': name,
                'type': 'center',
                'lat': coords['lat'],
                'lon': coords['lon'],
                'period': coords['period'],
                'works_translated': len(self._get_works_translated_at_center(name))
            })
        
        # Add works as nodes and translation paths as edges
        # This would be expanded based on actual translation data
        
        with open(output_file, 'w') as f:
            json.dump(network, f, indent=2)
        
        self.logger.info(f"Exported translation network to {output_file}")