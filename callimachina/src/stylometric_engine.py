"""
StylometricEngine: Author fingerprinting and attribution for classical texts.

Uses machine learning and statistical analysis to:
- Identify authors of anonymous fragments
- Verify authenticity of disputed works
- Detect stylistic patterns unique to authors
- Quantify stylistic similarity between texts
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
import logging
from typing import Dict, List, Tuple, Optional, Any
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import seaborn as sns

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class StylometricEngine:
    def __init__(self, language: str = 'greek'):
        """
        Initialize the stylometric engine.
        
        Args:
            language: Language of texts ('greek', 'latin', 'arabic', 'syriac')
        """
        self.language = language
        self.logger = logging.getLogger(__name__)
        
        # Feature extractors
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 3),
            min_df=2,
            max_df=0.8
        )
        
        self.count_vectorizer = CountVectorizer(
            max_features=500,
            ngram_range=(1, 2),
            min_df=1
        )
        
        # Author profiles database
        self.author_profiles = {}
        
        # Feature importance for interpretability
        self.feature_importance = {}
        
        # Language-specific patterns
        self._setup_language_patterns()
    
    def _setup_language_patterns(self):
        """Setup language-specific patterns and stopwords."""
        if self.language == 'greek':
            # Common Greek particles and conjunctions
            self.stopwords = {
                'και', 'δε', 'τε', 'γαρ', 'ουν', 'αλλα', 'ως', 'οτι',
                'εν', 'εις', 'εκ', 'κατα', 'υπο', 'προς', 'μετα', 'παρα'
            }
            
            # Greek-specific morphological patterns
            self.morphological_patterns = {
                'verb_endings': ['ω', 'εις', 'ει', 'ομεν', 'ετε', 'ουσι'],
                'case_endings': ['ος', 'ου', 'ι', 'ον', 'οι', 'ων', 'οις', 'ας'],
                'augment': ['ε', 'η'],
            }
            
        elif self.language == 'latin':
            self.stopwords = set(stopwords.words('latin')) if 'latin' in stopwords.fileids() else set()
            self.morphological_patterns = {
                'verb_endings': ['o', 's', 't', 'mus', 'tis', 'nt'],
                'case_endings': ['us', 'i', 'o', 'um', 'a', 'ae', 'am'],
            }
            
        else:
            self.stopwords = set()
            self.morphological_patterns = {}
    
    def extract_features(self, texts: List[str]) -> pd.DataFrame:
        """
        Extract comprehensive stylometric features from texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            DataFrame with stylometric features
        """
        features = []
        
        for i, text in enumerate(texts):
            feature_vector = {}
            
            # Basic statistics
            feature_vector.update(self._extract_basic_stats(text))
            
            # Lexical features
            feature_vector.update(self._extract_lexical_features(text))
            
            # Syntactic features
            feature_vector.update(self._extract_syntactic_features(text))
            
            # Morphological features
            feature_vector.update(self._extract_morphological_features(text))
            
            # Character-level features
            feature_vector.update(self._extract_character_features(text))
            
            features.append(feature_vector)
        
        return pd.DataFrame(features)
    
    def _extract_basic_stats(self, text: str) -> Dict[str, float]:
        """Extract basic text statistics."""
        chars = len(text)
        words = len(text.split())
        sentences = len(sent_tokenize(text)) if text.strip() else 1
        
        return {
            'char_count': chars,
            'word_count': words,
            'sentence_count': sentences,
            'avg_word_length': chars / words if words > 0 else 0,
            'avg_sentence_length': words / sentences if sentences > 0 else 0,
            'lexical_density': len(set(text.split())) / words if words > 0 else 0,
        }
    
    def _extract_lexical_features(self, text: str) -> Dict[str, float]:
        """Extract lexical features."""
        words = text.split()
        word_lengths = [len(word) for word in words]
        
        # Vocabulary richness
        unique_words = len(set(words))
        total_words = len(words)
        
        # Hapax legomena (words appearing only once)
        word_counts = Counter(words)
        hapax = sum(1 for count in word_counts.values() if count == 1)
        
        # Type-token ratio
        ttr = unique_words / total_words if total_words > 0 else 0
        
        # Yule's K measure
        if total_words > 0:
            yules_k = 10000 * (sum(count**2 for count in word_counts.values()) - total_words) / (total_words ** 2)
        else:
            yules_k = 0
        
        return {
            'vocabulary_richness': ttr,
            'hapax_legomena': hapax,
            'hapax_ratio': hapax / total_words if total_words > 0 else 0,
            'yules_k': yules_k,
            'word_length_mean': np.mean(word_lengths) if word_lengths else 0,
            'word_length_std': np.std(word_lengths) if word_lengths else 0,
        }
    
    def _extract_syntactic_features(self, text: str) -> Dict[str, float]:
        """Extract syntactic features."""
        sentences = sent_tokenize(text)
        
        # Sentence length distribution
        sentence_lengths = [len(sent.split()) for sent in sentences]
        
        # Punctuation patterns
        punctuation_counts = {
            'period': text.count('.'),
            'comma': text.count(','),
            'semicolon': text.count(';'),
            'colon': text.count(':'),
            'question': text.count('?'),
            'exclamation': text.count('!'),
        }
        
        # Conjunction usage
        conjunctions = ['and', 'but', 'or', 'so', 'because', 'however']
        conj_counts = sum(text.lower().count(conj) for conj in conjunctions)
        
        return {
            'sentence_length_mean': np.mean(sentence_lengths) if sentence_lengths else 0,
            'sentence_length_std': np.std(sentence_lengths) if sentence_lengths else 0,
            'punctuation_density': sum(punctuation_counts.values()) / len(text) if text else 0,
            'conjunction_frequency': conj_counts / len(sentences) if sentences else 0,
            **{f'punct_{k}': v / len(sentences) if sentences else 0 
               for k, v in punctuation_counts.items()}
        }
    
    def _extract_morphological_features(self, text: str) -> Dict[str, float]:
        """Extract morphological features."""
        features = {}
        
        # Apply language-specific patterns
        for pattern_name, patterns in self.morphological_patterns.items():
            count = sum(text.lower().endswith(pattern) for pattern in patterns)
            features[f'{pattern_name}_frequency'] = count / len(text.split()) if text.split() else 0
        
        # Part-of-speech patterns (simplified)
        if self.language == 'greek':
            # Greek article frequency
            article_pattern = r'\b(ο|η|το|οι|αι|τα)\b'
            article_matches = len(re.findall(article_pattern, text.lower()))
            features['article_frequency'] = article_matches / len(text.split()) if text.split() else 0
            
            # Greek particle frequency
            particles = ['γε', 'τοι', 'περ', 'ουν', 'δη', 'ναί', 'ου']
            particle_count = sum(text.lower().count(particle) for particle in particles)
            features['particle_frequency'] = particle_count / len(text.split()) if text.split() else 0
        
        return features
    
    def _extract_character_features(self, text: str) -> Dict[str, float]:
        """Extract character-level features."""
        chars = list(text.lower())
        char_counts = Counter(chars)
        
        # Character diversity
        char_diversity = len(char_counts) / len(chars) if chars else 0
        
        # Vowel-consonant ratio
        vowels = 'aeiouαειουηω'
        vowel_count = sum(char_counts[c] for c in char_counts if c in vowels)
        consonant_count = sum(char_counts[c] for c in char_counts if c.isalpha() and c not in vowels)
        
        vowel_ratio = vowel_count / (vowel_count + consonant_count) if (vowel_count + consonant_count) > 0 else 0
        
        # Character bigram frequencies
        bigrams = [text[i:i+2] for i in range(len(text)-1)]
        bigram_counts = Counter(bigrams)
        
        # Most common bigrams
        top_bigrams = bigram_counts.most_common(5)
        bigram_features = {}
        for i, (bigram, count) in enumerate(top_bigrams):
            bigram_features[f'top_bigram_{i+1}'] = count / len(bigrams) if bigrams else 0
        
        return {
            'char_diversity': char_diversity,
            'vowel_ratio': vowel_ratio,
            **bigram_features
        }
    
    def create_author_profile(self, author: str, texts: List[str], 
                            metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create a stylometric profile for an author.
        
        Args:
            author: Author name
            texts: List of known authentic texts
            metadata: Additional metadata
            
        Returns:
            Author profile dictionary
        """
        self.logger.info(f"Creating stylometric profile for {author}")
        
        # Extract features from all texts
        features_df = self.extract_features(texts)
        
        # Calculate author signature (mean and std of features)
        author_signature = {}
        for column in features_df.columns:
            author_signature[f'{column}_mean'] = features_df[column].mean()
            author_signature[f'{column}_std'] = features_df[column].std()
        
        # Extract n-gram signatures
        ngram_signature = self._extract_ngram_signature(texts)
        
        # Build TF-IDF model for this author
        self.tfidf_vectorizer.fit(texts)
        author_tfidf = self.tfidf_vectorizer.transform(texts)
        
        # Calculate feature importance using Random Forest
        feature_importance = self._calculate_feature_importance(features_df, author)
        
        profile = {
            'author': author,
            'signature': author_signature,
            'ngram_signature': ngram_signature,
            'feature_importance': feature_importance,
            'text_count': len(texts),
            'total_word_count': sum(len(text.split()) for text in texts),
            'language': self.language,
            'metadata': metadata or {},
            'reliability_score': self._calculate_profile_reliability(features_df)
        }
        
        # Store profile
        self.author_profiles[author] = profile
        
        self.logger.info(f"Created profile for {author} with {len(texts)} texts")
        
        return profile
    
    def _extract_ngram_signature(self, texts: List[str]) -> Dict[str, List[Tuple[str, float]]]:
        """Extract characteristic n-grams for the author."""
        # Combine all texts
        combined_text = ' '.join(texts)
        
        # Extract n-grams of different lengths
        signatures = {}
        
        for n in [1, 2, 3]:
            self.count_vectorizer.ngram_range = (n, n)
            ngram_matrix = self.count_vectorizer.fit_transform([combined_text])
            
            # Get feature names and frequencies
            feature_names = self.count_vectorizer.get_feature_names_out()
            frequencies = ngram_matrix.toarray()[0]
            
            # Sort by frequency and get top n-grams
            top_ngrams = sorted(zip(feature_names, frequencies), 
                              key=lambda x: x[1], reverse=True)[:50]
            
            signatures[f'{n}grams'] = top_ngrams
        
        return signatures
    
    def _calculate_feature_importance(self, features_df: pd.DataFrame, 
                                     author: str) -> Dict[str, float]:
        """Calculate feature importance using Random Forest."""
        # Create synthetic negative examples by shuffling features
        # This is a simplified approach; in practice, you'd use genuine non-author texts
        
        # For demonstration, we'll use a simple correlation-based approach
        feature_correlations = {}
        
        for column in features_df.columns:
            # Calculate how consistent this feature is across the author's texts
            consistency = 1.0 / (1.0 + features_df[column].std())
            feature_correlations[column] = consistency
        
        # Normalize to sum to 1
        total = sum(feature_correlations.values())
        if total > 0:
            feature_correlations = {k: v/total for k, v in feature_correlations.items()}
        
        return feature_correlations
    
    def _calculate_profile_reliability(self, features_df: pd.DataFrame) -> float:
        """Calculate reliability score for the author profile."""
        # Based on consistency of features across texts
        consistency_scores = []
        
        for column in features_df.columns:
            cv = features_df[column].std() / features_df[column].mean() if features_df[column].mean() != 0 else 0
            consistency = 1.0 / (1.0 + cv)  # Higher consistency = higher reliability
            consistency_scores.append(consistency)
        
        # Also consider number of texts and total word count
        text_count_score = min(len(features_df) / 5, 1.0)  # More texts = better
        length_score = min(features_df['word_count'].sum() / 10000, 1.0)  # More words = better
        
        reliability = (
            np.mean(consistency_scores) * 0.5 +
            text_count_score * 0.3 +
            length_score * 0.2
        )
        
        return reliability
    
    def attribute_text(self, text: str, candidates: Optional[List[str]] = None) -> List[Tuple[str, float]]:
        """
        Attribute an anonymous text to potential authors.
        
        Args:
            text: Text to attribute
            candidates: List of candidate authors (uses all profiles if None)
            
        Returns:
            List of (author, confidence) tuples sorted by confidence
        """
        if not self.author_profiles:
            raise ValueError("No author profiles available. Create profiles first.")
        
        if candidates is None:
            candidates = list(self.author_profiles.keys())
        
        # Extract features from the text
        text_features = self.extract_features([text]).iloc[0]
        
        # Compare with each candidate
        similarities = []
        
        for author in candidates:
            if author not in self.author_profiles:
                continue
            
            profile = self.author_profiles[author]
            similarity = self._calculate_similarity(text_features, profile)
            similarities.append((author, similarity))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities
    
    def _calculate_similarity(self, text_features: pd.Series, 
                             author_profile: Dict) -> float:
        """Calculate similarity between text and author profile."""
        signature = author_profile['signature']
        
        similarity_scores = []
        
        for feature_name in text_features.index:
            mean_key = f'{feature_name}_mean'
            std_key = f'{feature_name}_std'
            
            if mean_key in signature and std_key in signature:
                # Z-score distance
                observed = text_features[feature_name]
                expected = signature[mean_key]
                std = signature[std_key]
                
                if std > 0:
                    z_score = abs(observed - expected) / std
                    # Convert to similarity (lower z-score = higher similarity)
                    similarity = 1.0 / (1.0 + z_score)
                    similarity_scores.append(similarity)
        
        # Weight by feature importance if available
        if author_profile.get('feature_importance'):
            weights = [author_profile['feature_importance'].get(f, 1.0) 
                      for f in text_features.index]
            # Normalize weights
            weights = np.array(weights) / sum(weights)
            similarity_scores = [score * weight for score, weight in zip(similarity_scores, weights)]
        
        # Average similarity
        avg_similarity = np.mean(similarity_scores) if similarity_scores else 0
        
        # Adjust by profile reliability
        reliability = author_profile.get('reliability_score', 0.5)
        weighted_similarity = avg_similarity * reliability
        
        return weighted_similarity
    
    def verify_authenticity(self, text: str, claimed_author: str) -> Dict[str, Any]:
        """
        Verify if a text is authentic to a claimed author.
        
        Args:
            text: Text to verify
            claimed_author: Alleged author
            
        Returns:
            Verification results dictionary
        """
        if claimed_author not in self.author_profiles:
            return {
                'authentic': False,
                'confidence': 0.0,
                'reason': f"No profile available for {claimed_author}"
            }
        
        # Get attribution scores
        attributions = self.attribute_text(text, [claimed_author])
        
        if not attributions:
            return {
                'authentic': False,
                'confidence': 0.0,
                'reason': "Attribution failed"
            }
        
        claimed_score = attributions[0][1]
        
        # Get scores for other authors for comparison
        other_authors = [a for a in self.author_profiles.keys() if a != claimed_author]
        other_attributions = self.attribute_text(text, other_authors[:5])  # Top 5 other candidates
        
        # Calculate relative confidence
        if other_attributions:
            best_other_score = other_attributions[0][1]
            relative_confidence = claimed_score - best_other_score
        else:
            relative_confidence = claimed_score
        
        # Decision threshold
        is_authentic = claimed_score > 0.6 and relative_confidence > 0.1
        
        return {
            'authentic': is_authentic,
            'confidence': claimed_score,
            'relative_confidence': relative_confidence,
            'claimed_author_score': claimed_score,
            'best_alternative': other_attributions[0] if other_attributions else None,
            'feature_analysis': self._detailed_feature_analysis(text, claimed_author)
        }
    
    def _detailed_feature_analysis(self, text: str, author: str) -> Dict[str, Any]:
        """Perform detailed feature-by-feature analysis."""
        text_features = self.extract_features([text]).iloc[0]
        profile = self.author_profiles[author]
        signature = profile['signature']
        
        analysis = {}
        
        for feature_name in text_features.index:
            mean_key = f'{feature_name}_mean'
            std_key = f'{feature_name}_std'
            
            if mean_key in signature and std_key in signature:
                observed = text_features[feature_name]
                expected = signature[mean_key]
                std = signature[std_key]
                
                if std > 0:
                    z_score = (observed - expected) / std
                    
                    analysis[feature_name] = {
                        'observed': observed,
                        'expected': expected,
                        'z_score': z_score,
                        'deviation': 'normal' if abs(z_score) < 2 else 'significant'
                    }
        
        return analysis
    
    def detect_stylistic_outliers(self, texts: List[str], 
                                 metadata: List[Dict]) -> List[Dict]:
        """
        Detect stylistic outliers that may indicate different authors.
        
        Args:
            texts: List of texts to analyze
            metadata: List of metadata dictionaries
            
        Returns:
            List of outlier detection results
        """
        # Extract features
        features_df = self.extract_features(texts)
        
        # Handle missing values - fill NaNs with column means
        features_df = features_df.fillna(features_df.mean())
        
        # Normalize features
        normalized_features = (features_df - features_df.mean()) / features_df.std()
        
        # Handle any remaining NaNs (if std is 0)
        normalized_features = normalized_features.fillna(0)
        
        # Use DBSCAN for outlier detection
        dbscan = DBSCAN(eps=2, min_samples=2)
        clusters = dbscan.fit_predict(normalized_features)
        
        # Identify outliers (cluster -1)
        outliers = []
        
        for i, (text, meta, cluster) in enumerate(zip(texts, metadata, clusters)):
            if cluster == -1:
                # Calculate outlier score (distance to nearest core point)
                distances = dbscan.components_ if hasattr(dbscan, 'components_') else []
                outlier_score = 1.0  # Default for outliers
                
                outliers.append({
                    'index': i,
                    'metadata': meta,
                    'outlier_score': outlier_score,
                    'reason': 'Stylistic deviation from cluster',
                    'suggested_action': 'Flag for manual review or separate authorship analysis'
                })
        
        return outliers
    
    def visualize_author_signatures(self, authors: Optional[List[str]] = None, 
                                   save_path: Optional[str] = None):
        """
        Visualize author signatures using PCA.
        
        Args:
            authors: List of authors to visualize (uses all if None)
            save_path: Path to save the visualization
        """
        if authors is None:
            authors = list(self.author_profiles.keys())
        
        # Collect signature data
        signature_data = []
        labels = []
        
        for author in authors:
            if author in self.author_profiles:
                profile = self.author_profiles[author]
                signature = profile['signature']
                
                # Extract mean values
                means = [v for k, v in signature.items() if k.endswith('_mean')]
                signature_data.append(means)
                labels.append(author)
        
        if not signature_data:
            self.logger.warning("No signature data available for visualization")
            return
        
        # Convert to DataFrame for consistency
        feature_names = [k.replace('_mean', '') for k in signature[0].keys() if k.endswith('_mean')]
        df = pd.DataFrame(signature_data, columns=feature_names)
        
        # Perform PCA
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(df)
        
        # Create visualization
        plt.figure(figsize=(12, 8))
        
        # Plot author signatures
        scatter = plt.scatter(pca_result[:, 0], pca_result[:, 1], 
                            c=range(len(labels)), cmap='tab10', s=100, alpha=0.7)
        
        # Annotate points
        for i, label in enumerate(labels):
            plt.annotate(label, (pca_result[i, 0], pca_result[i, 1]), 
                       xytext=(5, 5), textcoords='offset points', fontsize=9)
        
        plt.xlabel(f'First Principal Component ({pca.explained_variance_ratio_[0]:.1%} variance)')
        plt.ylabel(f'Second Principal Component ({pca.explained_variance_ratio_[1]:.1%} variance)')
        plt.title('Author Stylometric Signatures (PCA)')
        plt.grid(True, alpha=0.3)
        
        # Add colorbar
        cbar = plt.colorbar(scatter)
        cbar.set_label('Author')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Saved author signature visualization to {save_path}")
        
        plt.show()
    
    def export_profiles(self, output_dir: str):
        """
        Export author profiles to disk.
        
        Args:
            output_dir: Output directory path
        """
        import json
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for author, profile in self.author_profiles.items():
            # Convert numpy types for JSON serialization
            json_profile = {}
            for key, value in profile.items():
                if isinstance(value, np.ndarray):
                    json_profile[key] = value.tolist()
                elif isinstance(value, (np.integer, np.floating)):
                    json_profile[key] = value.item()
                else:
                    json_profile[key] = value
            
            with open(output_path / f"{author}_profile.json", 'w') as f:
                json.dump(json_profile, f, indent=2, default=str)
        
        self.logger.info(f"Exported {len(self.author_profiles)} author profiles to {output_dir}")