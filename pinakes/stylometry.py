#!/usr/bin/env python3
"""
Stylometric Fingerprinting Module for CALLIMACHINA Protocol
Implements Burrows' Delta and authorial attribution for anonymous fragments

Core Mandate: Solve fragment attribution disputes computationally
"""

import re
import math
from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple, Optional
from datetime import datetime
import yaml

class StylometricEngine:
    def __init__(self):
        self.author_fingerprints = {}
        self.common_words_cache = {}
        self.ngram_cache = {}
        self.delta_threshold = -2.0  # Lower = more confident attribution
        
        print("[STYLOMETRIC ENGINE] Initializing authorial fingerprinting system...")
        self._load_extant_texts()
        print(f"[STYLOMETRIC ENGINE] Loaded {len(self.author_fingerprints)} author fingerprints")
    
    def _load_extant_texts(self):
        """
        Load extant works for authorial fingerprinting
        In production, would load from TLG, Perseus, etc.
        """
        # Simulated extant texts for major authors
        # Would be replaced with actual corpus data
        extant_corpus = {
            "Posidippus": {
                "extant_epigrams": self._get_posidippus_corpus(),
                "genre": "epigram",
                "period": "hellenistic"
            },
            "Callimachus": {
                "hymns": self._get_callimachina_corpus(),
                "genre": "hymn",
                "period": "hellenistic"
            },
            "Theocritus": {
                "idylls": self._get_theocritus_corpus(),
                "genre": "bucolic",
                "period": "hellenistic"
            },
            "Hippolytus": {
                "refutation": self._get_hippolytus_corpus(),
                "genre": "theology",
                "period": "early_christian"
            },
            "Eratosthenes": {
                "geographica_fragments": self._get_eratosthenes_corpus(),
                "genre": "geography",
                "period": "hellenistic"
            }
        }
        
        # Generate fingerprints for each author
        for author, works in extant_corpus.items():
            combined_text = " ".join(works.values())
            fingerprint = self._generate_fingerprint(combined_text, author)
            self.author_fingerprints[author] = fingerprint
    
    def _generate_fingerprint(self, text: str, author: str) -> Dict:
        """
        Generate stylometric fingerprint using Burrows' Delta method
        """
        # Clean and normalize text
        cleaned = self._clean_text(text)
        tokens = self._tokenize(cleaned)
        
        # Most common words (function words) - Delta uses top 50-150
        word_freq = Counter(tokens)
        most_common = word_freq.most_common(150)
        
        # Character n-grams (3-7 characters for Greek)
        char_ngrams = self._get_char_ngrams(cleaned, 3, 7)
        
        # Calculate z-scores for normalization
        word_zscores = self._calculate_zscores(word_freq, most_common[:50])
        ngram_zscores = self._calculate_zscores(char_ngrams, char_ngrams.most_common(50))
        
        fingerprint = {
            'author': author,
            'total_words': len(tokens),
            'unique_words': len(word_freq),
            'vocabulary_richness': len(word_freq) / len(tokens) if tokens else 0,
            'avg_word_length': sum(len(w) for w in tokens) / len(tokens) if tokens else 0,
            'common_words': dict(most_common[:50]),
            'word_zscores': word_zscores,
            'char_ngrams': dict(ngram_zscores),
            'hapax_legomena': len([w for w, c in word_freq.items() if c == 1]),
            'dislegomena': len([w for w, c in word_freq.items() if c == 2]),
            'generated': datetime.now().isoformat()
        }
        
        return fingerprint
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize Greek text for analysis"""
        # Remove punctuation, numbers, normalize spaces
        text = re.sub(r'[\d\W_]+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize Greek text"""
        # Simple whitespace tokenization
        # In production, would use specialized Greek tokenizer
        return text.split()
    
    def _get_char_ngrams(self, text: str, min_n: int, max_n: int) -> Counter:
        """Extract character n-grams from text"""
        ngrams = Counter()
        text = re.sub(r'\s+', '', text)  # Remove spaces for n-grams
        
        for n in range(min_n, max_n + 1):
            for i in range(len(text) - n + 1):
                ngram = text[i:i+n]
                ngrams[ngram] += 1
        
        return ngrams
    
    def _calculate_zscores(self, freq_dist: Counter, most_common: List[Tuple]) -> Dict[str, float]:
        """Calculate z-scores for features (Burrows' Delta core)"""
        zscores = {}
        
        # Get frequencies of most common items
        values = []
        for item, _ in most_common:
            values.append(freq_dist.get(item, 0))
        
        if not values:
            return {}
        
        mean = sum(values) / len(values)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in values) / len(values))
        
        # Avoid division by zero
        if std_dev == 0:
            std_dev = 1.0
        
        for item, _ in most_common:
            freq = freq_dist.get(item, 0)
            zscores[item] = (freq - mean) / std_dev
        
        return zscores
    
    def attribute_fragment(self, fragment_text: str, 
                          candidates: List[str] = None) -> List[Tuple[str, float]]:
        """
        Attribute anonymous fragment to most likely author using Delta
        Returns list of (author, delta_score) sorted by confidence
        """
        if not fragment_text or len(fragment_text.strip()) < 50:
            return [("insufficient_text", 0.0)]
        
        # Generate fingerprint for the fragment
        fragment_fp = self._generate_fingerprint(fragment_text, "anonymous")
        
        # Determine candidate authors
        if not candidates:
            candidates = list(self.author_fingerprints.keys())
        
        delta_scores = []
        
        for author in candidates:
            if author not in self.author_fingerprints:
                continue
            
            author_fp = self.author_fingerprints[author]
            
            # Calculate Burrows' Delta
            delta = self._calculate_delta(fragment_fp, author_fp)
            delta_scores.append((author, delta))
        
        # Sort by delta score (lower = more similar)
        delta_scores.sort(key=lambda x: x[1])
        
        return delta_scores
    
    def _calculate_delta(self, fp1: Dict, fp2: Dict) -> float:
        """
        Calculate Burrows' Delta between two fingerprints
        Lower scores indicate more similarity
        """
        total_delta = 0.0
        comparisons = 0
        
        # Compare word z-scores (most important for Delta)
        common_words = set(fp1['word_zscores'].keys()) & set(fp2['word_zscores'].keys())
        
        for word in common_words:
            z1 = fp1['word_zscores'][word]
            z2 = fp2['word_zscores'][word]
            total_delta += abs(z1 - z2)
            comparisons += 1
        
        # Compare character n-grams
        common_ngrams = set(fp1['char_ngrams'].keys()) & set(fp2['char_ngrams'].keys())
        
        for ngram in common_ngrams:
            z1 = fp1['char_ngrams'][ngram]
            z2 = fp2['char_ngrams'][ngram]
            total_delta += abs(z1 - z2) * 0.5  # Weight less than words
            comparisons += 1
        
        # Normalize by number of comparisons
        if comparisons > 0:
            return total_delta / comparisons
        else:
            return float('inf')
    
    def get_confidence_level(self, delta_score: float) -> Tuple[str, float]:
        """
        Convert delta score to confidence level and description
        Returns: (confidence_level, percentage)
        """
        if delta_score < -3.0:
            return ("very_high", 0.95)
        elif delta_score < -2.0:
            return ("high", 0.85)
        elif delta_score < -1.0:
            return ("moderate", 0.70)
        elif delta_score < 0.0:
            return ("low", 0.55)
        else:
            return ("very_low", 0.40)
    
    def analyze_fragment_collection(self, fragments: List[Dict]) -> List[Dict]:
        """
        Analyze collection of fragments and attribute each to likely author
        """
        results = []
        
        for fragment in fragments:
            text = fragment.get('text', '')
            fragment_id = fragment.get('id', 'unknown')
            
            if not text:
                continue
            
            # Attribute fragment
            attributions = self.attribute_fragment(text)
            
            if not attributions:
                continue
            
            top_author, delta_score = attributions[0]
            confidence_level, confidence_pct = self.get_confidence_level(delta_score)
            
            # Get top 3 candidates
            candidates = []
            for author, delta in attributions[:3]:
                level, pct = self.get_confidence_level(delta)
                candidates.append({
                    'author': author,
                    'delta_score': delta,
                    'confidence_level': level,
                    'confidence': pct
                })
            
            result = {
                'fragment_id': fragment_id,
                'top_attribution': top_author,
                'confidence_level': confidence_level,
                'confidence': confidence_pct,
                'delta_score': delta_score,
                'candidates': candidates,
                'text_preview': text[:100] + "..." if len(text) > 100 else text,
                'analyzed': datetime.now().isoformat()
            }
            
            results.append(result)
        
        return results
    
    def save_attribution_report(self, results: List[Dict], filename: str = None):
        """Save stylometric attribution results"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/Volumes/VIXinSSD/callimachina/pinakes/stylometric_attributions_{timestamp}.yml"
        
        report = {
            'report_timestamp': datetime.now().isoformat(),
            'fragments_analyzed': len(results),
            'methodology': 'Burrows Delta (z-score normalized)',
            'features': '50 most common words + 50 char n-grams (3-7)',
            'results': results
        }
        
        with open(filename, 'w') as f:
            yaml.dump(report, f, default_flow_style=False, allow_unicode=True)
        
        print(f"[STYLOMETRIC REPORT] Saved {len(results)} attributions to {filename}")
        return filename
    
    # Simulated corpus data for demonstration
    # In production, would load from TLG/Perseus
    
    def _get_posidippus_corpus(self) -> str:
        """Simulated Posidippus extant epigrams"""
        return """
        The weary traveler finds rest at last
        And dreams of seas now past
        The statue stands in morning light
        A dedication to eternal night
        
        On the rock the words are clear
        Here lies one we held so dear
        The poet's voice rings through the stone
        These verses mark his final home
        
        The athlete's glory fades with time
        But verses keep his name sublime
        A crown of olive, wreath of bay
        Honor those who've won the day
        """
    
    def _get_callimachina_corpus(self) -> str:
        """Simulated Callimachus hymns"""
        return """
        Hail to the goddess of the dawn
        Whose light brings forth the newborn fawn
        From Delos born, the sacred isle
        Where Apollo first did smile
        
        The golden lyre rings out clear
        Bringing music to the ear
        Of Zeus the king, the thunder's lord
        Whose wisdom is our last resort
        
        Athena wise with eyes of grey
        Guides us through the darkest day
        The owl her symbol, wisdom's bird
        In every line her voice is heard
        """
    
    def _get_theocritus_corpus(self) -> str:
        """Simulated Theocritus idylls"""
        return """
        In the field the shepherds play
        Their pipes at dawn and end of day
        The goats they graze on mountain high
        While sheep beneath the oaks do lie
        
        Thyrsis sings of Daphnis fair
        Whose beauty caused the nymphs to stare
        The cyclops blind laments his loss
        While Galatea counts the cost
        
        The harvest comes, the grapes are pressed
        The farmers take their well-earned rest
        The seasons turn, the years go by
        Beneath the bright Mediterranean sky
        """
    
    def _get_hippolytus_corpus(self) -> str:
        """Simulated Hippolytus Refutation"""
        return """
        The heretics claim the world is made
        Of elements in conflict laid
        But truth reveals a single source
        From which all things maintain their course
        
        The doctrines false must be exposed
        And truth in clarity disclosed
        The philosophers of ancient days
        Have wandered from the narrow ways
        
        The Word of God, the sacred flame
        Reveals the truth and ends the game
        Of speculation and of doubt
        Showing what the faith's about
        """
    
    def _get_eratosthenes_corpus(self) -> str:
        """Simulated Eratosthenes geographical fragments"""
        return """
        The earth is measured circle round
        Two hundred fifty thousand stadia found
        From Syene to the northern sea
        The distance calculated carefully
        
        The Nile it flows from southern lands
        And brings fertility to desert sands
        The mountains rise, the valleys fall
        The earth is shaped like a great ball
        
        The stars above in circles move
        Their paths the careful mind can prove
        The sun at solstice casts its ray
        Showing the tilt of earth's great way
        """

if __name__ == "__main__":
    print("=" * 60)
    print("CALLIMACHINA STYLOMETRIC FINGERPRINTING ENGINE")
    print("=" * 60)
    
    engine = StylometricEngine()
    
    # Test fragment attributions
    test_fragments = [
        {
            'id': 'fragment_001',
            'text': """
            The weary traveler finds rest at last
            And dreams of seas now past
            The statue stands in morning light
            A dedication to eternal night
            """
        },
        {
            'id': 'fragment_002',
            'text': """
            Hail to the goddess of the dawn
            Whose light brings forth the newborn fawn
            From Delos born, the sacred isle
            Where Apollo first did smile
            """
        },
        {
            'id': 'papyri.oxy.4.654',
            'text': "...on the statue of the queen, a dedication..."
        }
    ]
    
    print("\n[ATTRIBUTION TEST] Analyzing fragment collection...")
    results = engine.analyze_fragment_collection(test_fragments)
    
    for result in results:
        print(f"\nFragment: {result['fragment_id']}")
        print(f"Top Attribution: {result['top_attribution']}")
        print(f"Confidence: {result['confidence']:.1%} ({result['confidence_level']})")
        print(f"Preview: {result['text_preview']}")
    
    # Save report
    engine.save_attribution_report(results)
    
    print(f"\n[STYLOMETRIC ANALYSIS COMPLETE] {len(results)} fragments attributed")
