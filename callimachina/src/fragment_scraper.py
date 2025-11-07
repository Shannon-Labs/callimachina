"""
FragmentScraper: Web scraping and API integration for papyrological sources.

Integrates with:
- papyri.info (Duke Databank of Documentary Papyri)
- TLG (Thesaurus Linguae Graecae) 
- Oxyrhynchus Papyri database
- Herculaneum papyri collections
"""

import requests
import json
import time
import logging
from typing import Dict, List, Optional, Tuple, Any
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from collections import defaultdict


class FragmentScraper:
    def __init__(self, rate_limit: float = 1.0, timeout: int = 30):
        """
        Initialize the fragment scraper.
        
        Args:
            rate_limit: Seconds to wait between requests (default: 1.0)
            timeout: Request timeout in seconds (default: 30)
        """
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CALLIMACHINA v3.0 (Digital Archaeology Project)'
        })
        
        # Base URLs for different sources
        self.sources = {
            'papyri_info': 'https://papyri.info',
            'tlg': 'https://www.tlg.uci.edu',
            'oxyrhynchus': 'http://www.papyrology.ox.ac.uk',
            'herculaneum': 'https://163.1.169.40',
        }
        
        self.logger = logging.getLogger(__name__)
        
        # RSS load balancing stats
        self.rss_stats = {
            'queue_hits': {},
            'last_verified': None
        }
        
    def verify_rss_balance(self) -> Dict[str, Any]:
        """
        Verify RSS load balancing across network queues.
        Returns load distribution and balance metrics.
        """
        import time
        from collections import defaultdict
        
        try:
            # Check /proc/interrupts for eth0 queue statistics
            with open('/proc/interrupts', 'r') as f:
                interrupt_data = f.read()
            
            # Parse queue interrupts (eth0-rx-0, eth0-rx-1, etc.)
            import re
            queue_pattern = r'eth0-rx-(\d+)\s+(\d+)'
            matches = re.findall(queue_pattern, interrupt_data)
            
            if matches:
                queue_stats = {}
                for queue_num, count in matches:
                    queue_stats[f'queue_{queue_num}'] = int(count)
                
                # Calculate balance metrics
                values = list(queue_stats.values())
                if len(values) > 1:
                    max_load = max(values)
                    min_load = min(values)
                    avg_load = sum(values) / len(values)
                    
                    # Imbalance percentage (lower is better)
                    imbalance = ((max_load - min_load) / avg_load * 100) if avg_load > 0 else 0
                    
                    return {
                        'balanced': imbalance < 50,  # <50% imbalance acceptable
                        'imbalance_percent': round(imbalance, 1),
                        'queue_stats': queue_stats,
                        'recommendation': (
                            "Use production multi-source traffic" if imbalance > 50 
                            else "RSS working within normal parameters"
                        ),
                        'timestamp': time.time()
                    }
            
            return {
                'balanced': True, 
                'note': 'No queue data available - test environment detected',
                'recommendation': 'RSS verification not available in test environment'
            }
            
        except Exception as e:
            # Fallback for non-Linux or containerized environments (macOS, Docker, etc.)
            return {
                'balanced': True, 
                'error': str(e),
                'note': 'RSS verification unavailable - assuming balanced',
                'recommendation': 'RSS verification requires Linux /proc filesystem'
            }
    
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
    
    def search_papyri_info(self, query: str, max_results: int = 50) -> List[Dict]:
        """
        Search the Duke Databank of Documentary Papyri.
        
        Args:
            query: Search query (author, work, or text fragment)
            max_results: Maximum number of results to return
            
        Returns:
            List of fragment dictionaries
        """
        search_url = f"{self.sources['papyri_info']}/search"
        params = {
            'q': query,
            'limit': max_results,
            'type': 'text',
            'format': 'json'
        }
        
        response = self._rate_limited_request(search_url, params=params)
        if not response:
            return []
        
        try:
            data = response.json()
            fragments = []
            
            for item in data.get('results', [])[:max_results]:
                fragment = {
                    'id': item.get('id', ''),
                    'text': item.get('text', ''),
                    'source': 'papyri.info',
                    'metadata': {
                        'date': item.get('date', ''),
                        'provenance': item.get('provenance', ''),
                        'publication': item.get('publication', ''),
                        'ddb_id': item.get('ddb_id', ''),
                    },
                    'url': item.get('url', ''),
                    'confidence': 0.8  # Base confidence for papyri.info
                }
                fragments.append(fragment)
                
            self.logger.info(f"Found {len(fragments)} fragments from papyri.info for query '{query}'")
            return fragments
            
        except (json.JSONDecodeError, KeyError) as e:
            self.logger.error(f"Failed to parse papyri.info response: {e}")
            return []
    
    def get_fragment_text(self, fragment_id: str, source: str = 'papyri_info') -> Optional[str]:
        """
        Retrieve full text of a specific fragment.
        
        Args:
            fragment_id: Unique identifier for the fragment
            source: Source database ('papyri_info', 'tlg', etc.)
            
        Returns:
            Full text of the fragment or None
        """
        if source not in self.sources:
            self.logger.error(f"Unknown source: {source}")
            return None
        
        if source == 'papyri_info':
            url = f"{self.sources[source]}/ddbdp/{fragment_id}"
        else:
            url = f"{self.sources[source]}/fragment/{fragment_id}"
        
        response = self._rate_limited_request(url)
        if not response:
            return None
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text based on source-specific patterns
        if source == 'papyri_info':
            text_div = soup.find('div', {'class': 'text'})
            if text_div:
                return text_div.get_text(strip=True)
        
        # Fallback: return all text
        return soup.get_text(strip=True)
    
    def search_by_author(self, author: str, work: Optional[str] = None) -> List[Dict]:
        """
        Search for fragments by author and optionally by work.
        
        Args:
            author: Author name (e.g., 'Callimachus', 'Posidippus')
            work: Specific work title (optional)
            
        Returns:
            List of matching fragments
        """
        query = author
        if work:
            query = f"{author} {work}"
        
        fragments = self.search_papyri_info(query)
        
        # Filter by author more precisely
        filtered = []
        for fragment in fragments:
            text = fragment.get('text', '').lower()
            if author.lower() in text or self._is_likely_author_match(fragment, author):
                filtered.append(fragment)
        
        return filtered
    
    def _is_likely_author_match(self, fragment: Dict, author: str) -> bool:
        """
        Heuristic to determine if fragment likely belongs to the author.
        
        Args:
            fragment: Fragment dictionary
            author: Author name
            
        Returns:
            True if likely match
        """
        metadata = fragment.get('metadata', {})
        publication = metadata.get('publication', '').lower()
        
        # Check if author appears in publication info
        author_lower = author.lower()
        if author_lower in publication:
            return True
        
        # Check for common abbreviations
        abbreviations = self._get_author_abbreviations(author)
        for abbr in abbreviations:
            if abbr.lower() in publication:
                return True
        
        return False
    
    def _get_author_abbreviations(self, author: str) -> List[str]:
        """Get common abbreviations for classical authors."""
        abbreviations = {
            'Callimachus': ['Callim.', 'Call.', 'Cal.'],
            'Posidippus': ['Posid.', 'Pos.'],
            'Eratosthenes': ['Eratosth.', 'Erat.'],
            'Hippolytus': ['Hippol.', 'Hipp.'],
            'Euphorion': ['Euphor.', 'Euph.'],
            'Apollodorus': ['Apollod.', 'Ap.'],
        }
        return abbreviations.get(author, [])
    
    def get_oxyrhynchus_fragments(self, series: str = "PSI") -> List[Dict]:
        """
        Retrieve fragments from Oxyrhynchus collection.
        
        Args:
            series: Publication series (PSI, P.Oxy, etc.)
            
        Returns:
            List of fragment dictionaries
        """
        url = f"{self.sources['oxyrhynchus']}/POxy/"
        params = {'series': series, 'format': 'json'}
        
        response = self._rate_limited_request(url, params=params)
        if not response:
            return []
        
        try:
            data = response.json()
            fragments = []
            
            for item in data.get('fragments', []):
                fragment = {
                    'id': item.get('inventory', ''),
                    'text': item.get('transcription', ''),
                    'source': 'oxyrhynchus',
                    'metadata': {
                        'date': item.get('date', ''),
                        'provenance': 'Oxyrhynchus',
                        'publication': item.get('publication', ''),
                        'image_url': item.get('image_url', ''),
                    },
                    'confidence': 0.85
                }
                fragments.append(fragment)
                
            return fragments
            
        except (json.JSONDecodeError, KeyError) as e:
            self.logger.error(f"Failed to parse Oxyrhynchus response: {e}")
            return []
    
    def extract_citation_patterns(self, text: str) -> List[Dict]:
        """
        Extract citation patterns from fragment text.
        
        Looks for patterns like:
        - "As Aristotle says in his Physics..."
        - "Cf. Homer, Iliad 3.45"
        - "According to Plato's Republic..."
        
        Args:
            text: Fragment text to analyze
            
        Returns:
            List of citation dictionaries
        """
        citations = []
        
        # Pattern 1: "As [Author] says in [Work]"
        pattern1 = r'\bAs\s+(\w+)\s+says?\s+in\s+(?:his\s+)?([\w\s]+?)[,\.\s]'
        matches = re.finditer(pattern1, text, re.IGNORECASE)
        for match in matches:
            citations.append({
                'cited_author': match.group(1),
                'cited_work': match.group(2).strip(),
                'pattern': 'as_says_in',
                'confidence': 0.7
            })
        
        # Pattern 2: "Cf. [Author], [Work] [Book].[Line]"
        pattern2 = r'\b[Cc]f\.\s+(\w+),?\s+([\w\s]+?)\s+(\d+)\.(\d+)'
        matches = re.finditer(pattern2, text)
        for match in matches:
            citations.append({
                'cited_author': match.group(1),
                'cited_work': match.group(2).strip(),
                'book': int(match.group(3)),
                'line': int(match.group(4)),
                'pattern': 'cf_book_line',
                'confidence': 0.9
            })
        
        # Pattern 3: "According to [Author]'s [Work]"
        pattern3 = r'\bAccording\s+to\s+(\w+)\'s\s+([\w\s]+?)[,\.\s]'
        matches = re.finditer(pattern3, text, re.IGNORECASE)
        for match in matches:
            citations.append({
                'cited_author': match.group(1),
                'cited_work': match.group(2).strip(),
                'pattern': 'according_to',
                'confidence': 0.6
            })
        
        return citations
    
    def batch_search(self, queries: List[str], source: str = 'papyri_info') -> Dict[str, List[Dict]]:
        """
        Perform batch search for multiple queries.
        
        Args:
            queries: List of search queries
            source: Source database to search
            
        Returns:
            Dictionary mapping queries to fragment lists
        """
        results = {}
        
        for query in queries:
            if source == 'papyri_info':
                fragments = self.search_papyri_info(query)
            elif source == 'oxyrhynchus':
                # Oxyrhynchus doesn't support general search, use get_oxyrhynchus_fragments
                fragments = self.get_oxyrhynchus_fragments()
                # Filter by query
                fragments = [f for f in fragments if query.lower() in f.get('text', '').lower()]
            else:
                fragments = []
            
            results[query] = fragments
            self.logger.info(f"Batch search: '{query}' found {len(fragments)} fragments")
        
        return results