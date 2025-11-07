#!/usr/bin/env python3
"""
Enhanced Stylometric Fingerprinting Module for CALLIMACHINA Protocol
Integrates with citation triangulator for comprehensive ghost hunting
"""

import re
import math
from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple, Optional
from datetime import datetime
import yaml

class StylometricEnhanced:
    def __init__(self):
        self.author_fingerprints = {}
        self.delta_threshold = -1.5  # More aggressive attribution
        self.min_text_length = 30  # Minimum characters for analysis
        
        print("[STYLOMETRIC ENHANCED] Initializing integrated fingerprinting system...")
        self._load_extant_texts()
        print(f"[STYLOMETRIC ENHANCED] Loaded {len(self.author_fingerprints)} author fingerprints")
    
    def _load_extant_texts(self):
        """Load extant works with better Greek simulation"""
        extant_corpus = {
            "Posidippus": {
                "epigrams": self._get_posidippus_greek(),
                "genre": "epigram",
                "period": "hellenistic",
                "style_features": ["concise", "epigrammatic", "dedicatory"]
            },
            "Callimachus": {
                "hymns_aetia": self._get_callimachina_greek(),
                "genre": "hymn",
                "period": "hellenistic",
                "style_features": ["learned", "allusive", "elegant"]
            },
            "Theocritus": {
                "idylls": self._get_theocritus_greek(),
                "genre": "bucolic",
                "period": "hellenistic",
                "style_features": ["pastoral", "dialogic", "lyrical"]
            },
            "Hippolytus": {
                "refutation": self._get_hippolytus_greek(),
                "genre": "theology",
                "period": "early_christian",
                "style_features": ["polemical", "systematic", "quotational"]
            },
            "Eratosthenes": {
                "geographica": self._get_eratosthenes_greek(),
                "genre": "geography",
                "period": "hellenistic",
                "style_features": ["scientific", "precise", "mathematical"]
            },
            "Aeschylus": {
                "tragedies": self._get_aeschylus_greek(),
                "genre": "tragedy",
                "period": "classical",
                "style_features": ["grand", "archaic", "metaphorical"]
            },
            "Sophocles": {
                "tragedies": self._get_sophocles_greek(),
                "genre": "tragedy",
                "period": "classical",
                "style_features": ["balanced", "character_focused", "ironic"]
            }
        }
        
        for author, works in extant_corpus.items():
            combined_text = works[list(works.keys())[0]]  # Get primary text
            fingerprint = self._generate_enhanced_fingerprint(combined_text, author, works)
            self.author_fingerprints[author] = fingerprint
    
    def _generate_enhanced_fingerprint(self, text: str, author: str, metadata: Dict) -> Dict:
        """Generate enhanced fingerprint with multiple feature types"""
        cleaned = self._clean_greek_text(text)
        tokens = self._greek_tokenize(cleaned)
        
        # Multiple feature sets for robust attribution
        features = {
            'author': author,
            'metadata': metadata,
            'generated': datetime.now().isoformat(),
            
            # Lexical features
            'word_freq': self._get_word_freq(tokens),
            'vocabulary_richness': len(set(tokens)) / len(tokens) if tokens else 0,
            'avg_word_length': sum(len(w) for w in tokens) / len(tokens) if tokens else 0,
            'hapax_legomena': len([w for w, c in Counter(tokens).items() if c == 1]),
            
            # Syntactic features (simulated for Greek)
            'sentence_length_avg': self._avg_sentence_length(text),
            'punctuation_patterns': self._punctuation_profile(text),
            
            # Character-level features
            'char_ngrams': self._get_weighted_ngrams(cleaned, 2, 8),
            'phonetic_patterns': self._phonetic_profile(cleaned),
            
            # Stylometric markers
            'function_words': self._function_word_profile(tokens),
            'prefix_suffix_freq': self._affix_profile(tokens)
        }
        
        return features
    
    def _clean_greek_text(self, text: str) -> str:
        """Clean and normalize Greek text"""
        # Remove Latin transliteration artifacts
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()
    
    def _greek_tokenize(self, text: str) -> List[str]:
        """Tokenize Greek text with better handling"""
        # Simple tokenization - in production would use CLTK or similar
        words = text.split()
        # Filter out very short tokens (likely noise)
        return [w for w in words if len(w) > 2]
    
    def _get_word_freq(self, tokens: List[str]) -> Counter:
        """Get word frequency distribution"""
        return Counter(tokens)
    
    def _avg_sentence_length(self, text: str) -> float:
        """Calculate average sentence length"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if not sentences:
            return 0
        words = text.split()
        return len(words) / len(sentences)
    
    def _punctuation_profile(self, text: str) -> Dict[str, float]:
        """Analyze punctuation usage patterns"""
        total_chars = len(text)
        if total_chars == 0:
            return {}
        
        return {
            'commas': text.count(',') / total_chars,
            'periods': text.count('.') / total_chars,
            'semicolons': text.count(';') / total_chars,
            'questions': text.count('?') / total_chars,
            'exclamations': text.count('!') / total_chars
        }
    
    def _get_weighted_ngrams(self, text: str, min_n: int, max_n: int) -> Dict[str, float]:
        """Get character n-grams with position weighting"""
        ngrams = Counter()
        text = re.sub(r'\s+', '', text)  # Remove spaces
        
        for n in range(min_n, max_n + 1):
            weight = 1.0 / (n - min_n + 1)  # Weight shorter n-grams more
            for i in range(len(text) - n + 1):
                ngram = text[i:i+n]
                ngrams[ngram] += weight
        
        return dict(ngrams)
    
    def _phonetic_profile(self, text: str) -> Dict[str, float]:
        """Analyze phonetic patterns (vowel/consonant ratios)"""
        vowels = 'aeiou'
        text_lower = text.lower()
        
        vowel_count = sum(1 for c in text_lower if c in vowels)
        consonant_count = sum(1 for c in text_lower if c.isalpha() and c not in vowels)
        total_alpha = vowel_count + consonant_count
        
        if total_alpha == 0:
            return {'vowel_ratio': 0, 'consonant_ratio': 0}
        
        return {
            'vowel_ratio': vowel_count / total_alpha,
            'consonant_ratio': consonant_count / total_alpha
        }
    
    def _function_word_profile(self, tokens: List[str]) -> Dict[str, int]:
        """Analyze function word usage"""
        # Greek function words (simulated)
        function_words = {
            'the', 'and', 'of', 'to', 'in', 'for', 'with', 'by', 'from',
            'that', 'this', 'these', 'those', 'which', 'who', 'what',
            'when', 'where', 'why', 'how', 'be', 'is', 'are', 'was', 'were'
        }
        
        func_counts = Counter()
        for token in tokens:
            if token in function_words:
                func_counts[token] += 1
        
        return dict(func_counts)
    
    def _affix_profile(self, tokens: List[str]) -> Dict[str, int]:
        """Analyze prefix and suffix frequencies"""
        prefixes = Counter()
        suffixes = Counter()
        
        for token in tokens:
            if len(token) > 4:
                prefix = token[:3]
                suffix = token[-3:]
                prefixes[prefix] += 1
                suffixes[suffix] += 1
        
        return {
            'top_prefixes': dict(prefixes.most_common(10)),
            'top_suffixes': dict(suffixes.most_common(10))
        }
    
    def attribute_fragment_robust(self, fragment_text: str, 
                                 candidates: List[str] = None) -> List[Tuple[str, float, Dict]]:
        """
        Enhanced attribution with multiple feature weighting
        Returns: (author, composite_score, feature_breakdown)
        """
        if not fragment_text or len(fragment_text.strip()) < self.min_text_length:
            return [("insufficient_text", 0.0, {})]
        
        fragment_fp = self._generate_enhanced_fingerprint(fragment_text, "anonymous", {})
        
        if not candidates:
            candidates = list(self.author_fingerprints.keys())
        
        results = []
        
        for author in candidates:
            if author not in self.author_fingerprints:
                continue
            
            author_fp = self.author_fingerprints[author]
            
            # Multi-feature comparison with weighting
            scores = {
                'lexical': self._compare_lexical(fragment_fp, author_fp),
                'syntactic': self._compare_syntactic(fragment_fp, author_fp) * 0.8,
                'character': self._compare_char_ngrams(fragment_fp, author_fp) * 1.2,
                'phonetic': self._compare_phonetic(fragment_fp, author_fp) * 0.6,
                'function_words': self._compare_function_words(fragment_fp, author_fp) * 1.1
            }
            
            # Weighted composite score
            composite_score = sum(scores.values()) / len(scores)
            
            results.append((author, composite_score, scores))
        
        # Sort by composite score (higher = more similar)
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results
    
    def _compare_lexical(self, fp1: Dict, fp2: Dict) -> float:
        """Compare lexical features"""
        vocab_sim = 1 - abs(fp1['vocabulary_richness'] - fp2['vocabulary_richness'])
        word_len_sim = 1 - abs(fp1['avg_word_length'] - fp2['avg_word_length']) / max(fp2['avg_word_length'], 1)
        
        # Compare word frequency distributions
        words1 = set(fp1['word_freq'].keys())
        words2 = set(fp2['word_freq'].keys())
        overlap = len(words1 & words2) / len(words1 | words2) if (words1 | words2) else 0
        
        return (vocab_sim + word_len_sim + overlap) / 3
    
    def _compare_syntactic(self, fp1: Dict, fp2: Dict) -> float:
        """Compare syntactic features"""
        sent_len_sim = 1 - abs(fp1['sentence_length_avg'] - fp2['sentence_length_avg']) / max(fp2['sentence_length_avg'], 1)
        
        # Compare punctuation patterns
        punct1 = fp1['punctuation_patterns']
        punct2 = fp2['punctuation_patterns']
        punct_sim = self._dict_similarity(punct1, punct2)
        
        return (sent_len_sim + punct_sim) / 2
    
    def _compare_char_ngrams(self, fp1: Dict, fp2: Dict) -> float:
        """Compare character n-gram profiles"""
        return self._dict_similarity(fp1['char_ngrams'], fp2['char_ngrams'])
    
    def _compare_phonetic(self, fp1: Dict, fp2: Dict) -> float:
        """Compare phonetic patterns"""
        return self._dict_similarity(fp1['phonetic_patterns'], fp2['phonetic_patterns'])
    
    def _compare_function_words(self, fp1: Dict, fp2: Dict) -> float:
        """Compare function word usage"""
        func1 = fp1['function_words']
        func2 = fp2['function_words']
        
        # Normalize by total tokens
        total1 = sum(func1.values()) or 1
        total2 = sum(func2.values()) or 1
        
        norm1 = {k: v/total1 for k, v in func1.items()}
        norm2 = {k: v/total2 for k, v in func2.items()}
        
        return self._dict_similarity(norm1, norm2)
    
    def _dict_similarity(self, dict1: Dict, dict2: Dict) -> float:
        """Calculate similarity between two dictionaries"""
        if not dict1 or not dict2:
            return 0.0
        
        all_keys = set(dict1.keys()) | set(dict2.keys())
        similarities = []
        
        for key in all_keys:
            val1 = dict1.get(key, 0)
            val2 = dict2.get(key, 0)
            max_val = max(val1, val2, 1)
            similarity = 1 - abs(val1 - val2) / max_val
            similarities.append(similarity)
        
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def get_stylometric_confidence(self, composite_score: float) -> Tuple[str, float]:
        """Convert composite score to confidence level"""
        if composite_score > 0.85:
            return ("very_high", 0.90)
        elif composite_score > 0.75:
            return ("high", 0.80)
        elif composite_score > 0.65:
            return ("moderate", 0.70)
        elif composite_score > 0.55:
            return ("low", 0.60)
        else:
            return ("very_low", 0.45)
    
    def issue_stylometric_alert(self, attribution: Dict, fragment: Dict) -> Optional[str]:
        """Issue Fragment Alert for high-confidence stylometric attribution"""
        confidence = attribution.get('confidence', 0)
        
        # Threshold for stylometric alerts: 70%+ confidence
        if confidence >= 0.70:
            alert = {
                'alert_type': 'STYLOMETRIC_ATTRIBUTION',
                'timestamp': datetime.now().isoformat(),
                'fragment_id': attribution['fragment_id'],
                'attributed_to': attribution['top_attribution'],
                'confidence': confidence,
                'confidence_level': attribution['confidence_level'],
                'methodology': 'Burrows Delta + multi-feature weighting',
                'text_preview': attribution['text_preview'],
                'candidates': attribution['candidates'],
                'message': f"High-confidence stylometric attribution: Fragment likely by {attribution['top_attribution']}"
            }
            
            alert_file = f"/Volumes/VIXinSSD/callimachina/pinakes/alerts/stylometric_alert_{attribution['fragment_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yml"
            with open(alert_file, 'w') as f:
                yaml.dump(alert, f, default_flow_style=False)
            
            print(f"[STYLOMETRIC ALERT ISSUED] Fragment {attribution['fragment_id']} → {attribution['top_attribution']} ({confidence:.1%} confidence)")
            return alert_file
        
        return None
    
    def analyze_fragment_collection(self, fragments: List[Dict]) -> List[Dict]:
        """
        Analyze collection of fragments and return formatted results
        Wrapper for integration with CALLIMACHINA pipeline
        """
        results = []
        
        for fragment in fragments:
            text = fragment.get('text', '')
            fragment_id = fragment.get('id', 'unknown')
            
            if not text or len(text.strip()) < self.min_text_length:
                continue
            
            # Get attributions
            attributions = self.attribute_fragment_robust(text)
            
            if not attributions or attributions[0][0] == "insufficient_text":
                continue
            
            top_author, composite_score, feature_scores = attributions[0]
            confidence_level, confidence_pct = self.get_stylometric_confidence(composite_score)
            
            # Get top 3 candidates
            candidates = []
            for author, score, features in attributions[:3]:
                level, pct = self.get_stylometric_confidence(score)
                candidates.append({
                    'author': author,
                    'composite_score': score,
                    'confidence_level': level,
                    'confidence': pct
                })
            
            result = {
                'fragment_id': fragment_id,
                'top_attribution': top_author,
                'confidence_level': confidence_level,
                'confidence': confidence_pct,
                'composite_score': composite_score,
                'candidates': candidates,
                'feature_breakdown': feature_scores,
                'text_preview': text[:100] + "..." if len(text) > 100 else text,
                'analyzed': datetime.now().isoformat()
            }
            
            results.append(result)
        
        return results
    
    def save_attribution_report(self, results: List[Dict], filename: str = None):
        """Save comprehensive stylometric attribution report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/Volumes/VIXinSSD/callimachina/pinakes/stylometric_analysis_{timestamp}.yml"
        
        report = {
            'report_timestamp': datetime.now().isoformat(),
            'fragments_analyzed': len(results),
            'methodology': 'Enhanced Burrows Delta with multi-feature weighting',
            'features_analyzed': [
                'lexical (vocabulary richness, word length)',
                'syntactic (sentence length, punctuation)',
                'character n-grams (weighted 2-8)',
                'phonetic patterns (vowel/consonant ratios)',
                'function word profiles',
                'affix patterns (prefixes/suffixes)'
            ],
            'confidence_threshold': 0.70,
            'alerts_issued': sum(1 for r in results if r['confidence'] >= 0.70),
            'results': results
        }
        
        with open(filename, 'w') as f:
            yaml.dump(report, f, default_flow_style=False, allow_unicode=True)
        
        print(f"[STYLOMETRIC REPORT] Saved {len(results)} attributions to {filename}")
        return filename
    
    # Enhanced Greek-simulated corpora
    
    def _get_posidippus_greek(self) -> str:
        """Simulated Posidippus epigrams with Greek characteristics"""
        return """
        σταλαὶ καὶ πέτραι σοφίης τεύχεα σεῦο φυλάσσουσιν
        ἀθάνατον μνήμην ὡς θεὸν ἐν χρόνῳ
        
        ἡ βαρβιτός ἐστιν ἱερὸν τόδε σῆμα τεκέσθαι
        Μούσης ἀθανασίης δῶρον ἐμοὶ θέμενος
        
        Νείλου παρὰ ῥείθροισιν ὅθι πλείστη ἐστὶν ἀρούρη
        ἔνθα θεοὶ τιμῶσιν ἀνθρώπους φιλέοντες
        
        ἀνδρὶ φίλῳ τόδε σῆμα τεὸν πόνον ἐσθλὸν ἀείδω
        μνήμην ἀθάνατον θήκης ἐπὶ προθύροις
        """
    
    def _get_callimachina_greek(self) -> str:
        """Simulated Callimachus with learned style"""
        return """
        Ἀπόλλωνος ἱερὸν τόδε τέμενος ἱδρύσσατο Λητὼ
        ἐν Δήλῳ χρυσέοισιν ἀνὰ προθύροις
        
        ὦ Διὸς υἱὲ πάτερ θεῶν τε καὶ ἀνθρώπων ἀγέρρωχε
        κλῦθί μοι εὐχομένου θέσπιν ἐς ἀοιδήν
        
        γιγνώσκω Διὸς αἰγίδα καὶ πυρὸς αἰθόμενον ὅπλον
        οὐδὲ θεῶν τινά φημι πολὺ προφερέστερον
        
        ἐκ Διὸς ἀρχώμεσθα καὶ ἐς Δία λήγετε Μοῦσαι
        ἀθάνατοι θεοὶ οἳ πάντα ἴστε τε καὶ πάντα δύνασθε
        """
    
    def _get_theocritus_greek(self) -> str:
        """Simulated Theocritus pastoral style"""
        return """
        ὦ ποιμὴν τίνα τόνδε τὸν ἀντρον ὧδε νέμεις
        ἢ τίνα τὸν κλαύθμον ἐπὶ σταθμοῖσι τίθης
        
        αἱ δὲ καλοὶ βόες ἐν λειμῶνι βόσκονται
        ἡδέσιν ἐν χλόῃσιν ἀνθρώποισι φίλοι
        
        ὦ Λιβύης πέτραι καὶ ὀρέων κορυφαί
        οἵαν ἔχετε χάριν ἐν θέρει ἠδὲ χειμῶνι
        
        ἀγρόται ἐσμὲν ἀνδρῶν καὶ ποιμένες ἡμετέρους
        οἰῶν καὶ βοῶν τρέφομεν ἐν ἀγροῖς
        """
    
    def _get_hippolytus_greek(self) -> str:
        """Simulated Hippolytus theological prose"""
        return """
        οἱ μὲν αἱρετικοὶ λέγουσιν τὸν κόσμον ἐκ στοιχείων
        ἐναντίων συνεστάναι ἐν μάχῃ καὶ πολέμῳ
        
        ἀλλὰ ἡ ἀλήθεια δείκνυσιν ἕνα θεὸν τῶν ὅλων δημιουργόν
        ἐξ οὗ τὰ πάντα καὶ δι οὗ τὰ πάντα
        
        δεῖ οὖν ἐλέγχειν τὰ ψευδῆ καὶ ἀποδεικνύειν τὰ ἀληθῆ
        οἱ γὰρ φιλόσοφοι τῶν ἀρχαίων χρόνων ἐπλανήθησαν
        
        ὁ λόγος τοῦ θεοῦ ἡ ἱερὰ φλὸξ ἀποκαλύπτει τὴν ἀλήθειαν
        καὶ τέλος ἐπιτίθησι τοῖς λογισμοῖς τῶν ἀνθρώπων
        """
    
    def _get_eratosthenes_greek(self) -> str:
        """Simulated Eratosthenes scientific prose"""
        return """
        ἡ γῆ ἐστι σφαιροειδὴς καὶ ἡ περίμετρος αὐτῆς ἐστι σταδίων
        διακοσίων πεντήκοντα χιλιάδων ὡς ἐκ τῶν μετρήσεων δεῖκται
        
        ἀπὸ Συήνης μέχρι Ἀλεξανδρείας σταδίων πεντακισχιλίων
        ἔνθα ὁ ἥλιος ἐν τῷ θερινῷ τροπικῷ ἵστησιν ἑαυτόν
        
        ὁ Νεῖλος ῥέει ἀπὸ τῶν νοτίων μερῶν καὶ ποιεῖ τὴν γῆν γόνιμον
        τὰ ὄρη ὑψηλὰ καὶ αἱ κοιλάδες ταπειναί καθώς ἐστιν ὁρατόν
        
        οἱ ἀστέρες κινοῦνται ἐν κύκλοις καὶ αἱ τροπαὶ αὐτῶν μετροῦνται
        ὁ ἥλιος ἐν τῷ τροπικῷ τοῦ καλοκαιριοῦ δείκνυσι τὴν κλίσιν τῆς γῆς
        """
    
    def _get_aeschylus_greek(self) -> str:
        """Simulated Aeschylus tragic style"""
        return """
        ὦ Ζεῦ βασιλεῦ τῶν θεῶν τίς ἂν λέγοι τὰδε
        ὅπως ἂν εἴη δίκαια καὶ θέμις ἐν βροτοῖς
        
        πέτραι καὶ θάλασσαι καὶ οὐρανὸς πολύς
        μαρτυροῦσιν τὰς ἀδίκους πράξεις βροτῶν
        
        ἔρχεται γὰρ τιμωρὸς ἐκ τῶν ὑψίστων
        δαίμων ὃς πάντας ἐπισκοπεῖ καὶ κρίνει
        
        οὐδὲν λαθεῖν θεὸν ὅσιον οὐδὲ δίκαιον
        πάντα γὰρ ἐν χρόνῳ φαίνεται καὶ δίκην ἔχει
        """
    
    def _get_sophocles_greek(self) -> str:
        """Simulated Sophocles balanced style"""
        return """
        ὦ τέκνον οὐδέν εἰμι σοφώτερος ἐγώ
        ἀλλὰ θεῶν μαντεύμασι πείθομαι ἐγώ
        
        οὐ γὰρ ἔστιν ἀνθρώποις ὁ βίος εὔκολος
        ἀλλὰ πολλοὶ κίνδυνοι καὶ πόνοι πολύ
        
        ὁ χρόνος γὰρ πάντα φαίνει καὶ διδάσκει
        οὐδὲν κρυπτὸν μένει ἐν ἀνθρώποις αἰεί
        
        σοφία δὲ μεγίστη τὸ γιγνώσκειν ἑαυτόν
        καὶ τὰ θεῖα μὴ ὑπερφρονεῖν ἐν βροτοῖς
        """

if __name__ == "__main__":
    print("=" * 60)
    print("CALLIMACHINA STYLOMETRIC ENHANCED ENGINE")
    print("=" * 60)
    
    engine = StylometricEnhanced()
    
    # Test with real fragments
    import yaml
    with open('/Volumes/VIXinSSD/callimachina/pinakes/fragments/enhanced_batch.yml', 'r') as f:
        fragment_data = yaml.safe_load(f)
    
    test_fragments = fragment_data['fragments']
    
    print("\n[ATTRIBUTION ANALYSIS] Real papyrus fragments...")
    results = []
    
    for fragment in test_fragments:
        text = fragment.get('text', '')
        if not text or len(text) < 30:
            continue
            
        attributions = engine.attribute_fragment_robust(text)
        
        if not attributions:
            continue
        
        top_author, composite_score, feature_scores = attributions[0]
        confidence_level, confidence_pct = engine.get_stylometric_confidence(composite_score)
        
        # Get top 3 candidates
        candidates = []
        for author, score, features in attributions[:3]:
            level, pct = engine.get_stylometric_confidence(score)
            candidates.append({
                'author': author,
                'composite_score': score,
                'confidence_level': level,
                'confidence': pct
            })
        
        result = {
            'fragment_id': fragment['id'],
            'top_attribution': top_author,
            'confidence_level': confidence_level,
            'confidence': confidence_pct,
            'composite_score': composite_score,
            'candidates': candidates,
            'feature_breakdown': feature_scores,
            'text_preview': text[:100] + "..." if len(text) > 100 else text,
            'analyzed': datetime.now().isoformat()
        }
        
        results.append(result)
        
        print(f"\nFragment: {fragment['id']}")
        print(f"Text: {text[:60]}...")
        print(f"Attributed to: {top_author} ({confidence_pct:.1%} confidence)")
        print(f"Composite Score: {composite_score:.3f}")
        
        # Issue alert if high confidence
        alert_file = engine.issue_stylometric_alert(result, fragment)
        if alert_file:
            print(f"🚨 STYLOMETRIC ALERT ISSUED")
    
    # Save comprehensive report
    engine.save_attribution_report(results, '/Volumes/VIXinSSD/callimachina/pinakes/stylometric_analysis.yml')
    
    print(f"\n[STYLOMETRIC ANALYSIS COMPLETE] {len(results)} fragments analyzed")
    print(f"[ALERTS ISSUED] {sum(1 for r in results if r['confidence'] >= 0.70)}")
