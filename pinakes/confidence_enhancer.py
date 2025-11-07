#!/usr/bin/env python3
"""
Confidence Enhancement Engine for CALLIMACHINA Protocol
Implements Bayesian updating, temporal weighting, and cross-cultural bonuses

Integrates stylometry, translations, and network analysis for unified confidence scores
"""

import math
import re
import yaml
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict
import numpy as np

class ConfidenceEnhancer:
    def __init__(self):
        self.confidence_threshold = 0.60  # Lower bound for alerts
        self.bayesian_priors = {}
        self.temporal_weights = {}
        self.cross_cultural_bonuses = {}
        
        print("[CONFIDENCE ENHANCER] Initializing Bayesian confidence system...")
        self._load_historical_data()
    
    def _load_historical_data(self):
        """Load historical reconstruction data for Bayesian priors"""
        # Historical success rates by genre and period
        self.bayesian_priors = {
            'genre': {
                'geography': 0.75,
                'philosophy': 0.68,
                'epigram': 0.82,
                'tragedy': 0.55,
                'science': 0.72,
                'theology': 0.70
            },
            'period': {
                'classical': 0.65,      # 5th-4th BCE
                'hellenistic': 0.78,    # 3rd-1st BCE
                'early_roman': 0.70,    # 1st-3rd CE
                'late_antique': 0.60,   # 4th-7th CE
                'byzantine': 0.55       # 8th-15th CE
            },
            'survival_path': {
                'greek_direct': 0.70,
                'greek_indirect': 0.60,
                'arabic_translation': 0.85,
                'latin_translation': 0.75,
                'syriac_translation': 0.80,
                'cross_cultural': 0.90
            }
        }
    
    def calculate_enhanced_confidence(self, 
                                    reconstruction: Dict,
                                    lost_work: Dict,
                                    stylometric_score: float = 0.0,
                                    translation_data: Dict = None,
                                    network_position: Dict = None) -> Dict:
        """
        Calculate enhanced confidence using Bayesian updating and multi-factor weighting
        """
        work_title = lost_work['title']
        print(f"[CONFIDENCE ENHANCEMENT] Analyzing '{work_title}'...")
        
        # Base confidence from reconstruction
        base_confidence = reconstruction.get('overall_confidence', 0.0)
        
        # Extract work characteristics
        genre = self._extract_genre(work_title)
        period = self._estimate_period(lost_work.get('citations', []))
        survival_paths = lost_work.get('survival_paths', [])
        
        # Step 1: Bayesian Prior
        bayesian_prior = self._calculate_bayesian_prior(genre, period, survival_paths)
        print(f"  Bayesian prior: {bayesian_prior:.3f}")
        
        # Step 2: Citation Quality Weighting
        citation_quality = self._weight_citations(lost_work.get('citations', []))
        print(f"  Citation quality: {citation_quality:.3f}")
        
        # Step 3: Temporal Weighting
        temporal_weight = self._calculate_temporal_weight(lost_work.get('citations', []))
        print(f"  Temporal weight: {temporal_weight:.3f}")
        
        # Step 4: Cross-Cultural Bonus
        cultural_bonus = self._calculate_cultural_bonus(survival_paths, translation_data)
        print(f"  Cultural bonus: {cultural_bonus:.3f}")
        
        # Step 5: Stylometric Integration
        stylometric_bonus = self._integrate_stylometry(stylometric_score, base_confidence)
        print(f"  Stylometric bonus: {stylometric_bonus:.3f}")
        
        # Step 6: Network Centrality
        network_bonus = self._calculate_network_bonus(network_position)
        print(f"  Network bonus: {network_bonus:.3f}")
        
        # Combine all factors using Bayesian updating
        enhanced_confidence = self._bayesian_update(
            base_confidence,
            bayesian_prior,
            citation_quality,
            temporal_weight,
            cultural_bonus,
            stylometric_bonus,
            network_bonus
        )
        
        # Calculate confidence components for reporting
        components = {
            'base_confidence': base_confidence,
            'bayesian_prior': bayesian_prior,
            'citation_quality': citation_quality,
            'temporal_weight': temporal_weight,
            'cultural_bonus': cultural_bonus,
            'stylometric_bonus': stylometric_bonus,
            'network_bonus': network_bonus,
            'enhancement_magnitude': enhanced_confidence - base_confidence
        }
        
        print(f"  → Enhanced confidence: {enhanced_confidence:.3f} ({enhanced_confidence*100:.1f}%)")
        print(f"  → Improvement: +{(enhanced_confidence - base_confidence)*100:.1f}%")
        
        return {
            'work_title': work_title,
            'enhanced_confidence': enhanced_confidence,
            'confidence_level': self._get_confidence_level(enhanced_confidence),
            'components': components,
            'recommendations': self._generate_recommendations(components, enhanced_confidence),
            'alert_recommended': enhanced_confidence >= self.confidence_threshold,
            'calculated': datetime.now().isoformat()
        }
    
    def _extract_genre(self, work_title: str) -> str:
        """Extract genre from work title"""
        genre_keywords = {
            'geograph': 'geography',
            'geographika': 'geography',
            'epigram': 'epigram',
            'epigrams': 'epigram',
            'tragedy': 'tragedy',
            'tragedies': 'tragedy',
            'hymn': 'hymn',
            'hymns': 'hymn',
            'philosoph': 'philosophy',
            'theology': 'theology',
            'theolog': 'theology',
            'science': 'science',
            'phenomena': 'science'
        }
        
        title_lower = work_title.lower()
        for keyword, genre in genre_keywords.items():
            if keyword in title_lower:
                return genre
        
        return 'unknown'
    
    def _estimate_period(self, citations: List[Dict]) -> str:
        """Estimate work's original period from citations"""
        if not citations:
            return 'unknown'
        
        date_ranges = {
            'Strabo': 'hellenistic',
            'Cleomedes': 'early_roman',
            'Ptolemy': 'early_roman',
            'Stobaeus': 'late_antique',
            'Athenaeus': 'early_roman',
            'Plutarch': 'early_roman',
            'Diogenes Laertius': 'late_antique',
            'Eusebius': 'late_antique',
            'Aristotle': 'classical',
            'Sophocles': 'classical',
            'Euripides': 'classical',
            'Aeschylus': 'classical'
        }
        
        periods = []
        for citation in citations:
            source = citation.get('source', '')
            for author, period in date_ranges.items():
                if author in source:
                    periods.append(period)
                    break
        
        if periods:
            # Return most common period
            return max(set(periods), key=periods.count)
        
        return 'unknown'
    
    def _calculate_bayesian_prior(self, genre: str, period: str, survival_paths: List[str]) -> float:
        """Calculate Bayesian prior probability"""
        genre_prior = self.bayesian_priors['genre'].get(genre, 0.65)
        period_prior = self.bayesian_priors['period'].get(period, 0.65)
        
        # Survival path prior (use best available path)
        path_priors = [self.bayesian_priors['survival_path'].get(path, 0.60) 
                      for path in survival_paths]
        path_prior = max(path_priors) if path_priors else 0.60
        
        # Combine using weighted average
        # Genre and period are more fundamental than survival path
        combined_prior = (genre_prior * 0.4 + period_prior * 0.4 + path_prior * 0.2)
        
        return combined_prior
    
    def _weight_citations(self, citations: List[Dict]) -> float:
        """Weight citations by independence and quality"""
        if not citations:
            return 0.0
        
        total_weight = 0.0
        
        for citation in citations:
            # Base weight by citation type
            type_weights = {
                'direct_quote': 1.0,
                'fragment': 0.9,
                'paraphrase': 0.7,
                'citation': 0.6,
                'extensive_paraphrase': 0.85,
                'possible_attribution': 0.4
            }
            
            base_weight = type_weights.get(citation.get('citation_type', ''), 0.5)
            
            # Independence bonus
            independence = citation.get('independence_score', 0.5)
            
            # Language factor (Greek primary sources weighted higher)
            language = citation.get('language', 'greek')
            language_factor = 1.0 if language == 'greek' else 0.8
            
            citation_weight = base_weight * independence * language_factor
            total_weight += citation_weight
        
        # Normalize by number of citations (diminishing returns)
        return min(total_weight / len(citations), 1.0)
    
    def _calculate_temporal_weight(self, citations: List[Dict]) -> float:
        """Weight by temporal spread and antiquity"""
        if not citations:
            return 0.0
        
        # Extract centuries from date ranges
        centuries = []
        for citation in citations:
            date_range = citation.get('date_range', '')
            century = self._extract_century(date_range)
            if century:
                centuries.append(century)
        
        if not centuries:
            return 0.5
        
        # Temporal spread bonus (more centuries = better)
        unique_centuries = len(set(centuries))
        spread_bonus = min(unique_centuries * 0.15, 0.3)
        
        # Antiquity bonus (older sources weighted higher)
        avg_century = sum(centuries) / len(centuries)
        # Earlier centuries are more negative (BCE) or smaller (CE)
        if avg_century < 0:  # BCE
            antiquity_bonus = min(abs(avg_century) * 0.02, 0.2)
        else:  # CE
            antiquity_bonus = max((5 - avg_century) * 0.02, 0)  # Bonus for pre-5th century
        
        return 0.5 + spread_bonus + antiquity_bonus
    
    def _extract_century(self, date_range: str) -> int:
        """Extract century from date range string"""
        if not date_range or date_range == 'unknown':
            return None
        
        patterns = [
            r'(\d+)(?:st|nd|rd|th)\s+century',
            r'c\.\s*(\d+)\s+century',
            r'(\d+)(?:st|nd|rd|th)\s+century\s+(BCE|CE)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, date_range, re.IGNORECASE)
            if match:
                century = int(match.group(1))
                if 'BCE' in date_range:
                    return -century
                return century
        
        return None
    
    def _calculate_cultural_bonus(self, survival_paths: List[str], translation_data: Dict = None) -> float:
        """Calculate cross-cultural transmission bonus"""
        bonus = 0.0
        
        # Base bonus for each survival path
        path_bonuses = {
            'greek_direct': 0.0,
            'greek_indirect': 0.05,
            'arabic_translation': 0.15,
            'latin_translation': 0.10,
            'syriac_translation': 0.12,
            'armenian_translation': 0.08
        }
        
        for path in survival_paths:
            bonus += path_bonuses.get(path, 0)
        
        # Additional bonus for multiple paths
        if len(survival_paths) > 1:
            bonus += 0.05 * (len(survival_paths) - 1)
        
        # Translation data bonus
        if translation_data:
            translations = translation_data.get('translations_found', [])
            if len(translations) >= 2:
                bonus += 0.10  # Bonus for multiple translations
            
            chains = translation_data.get('translation_chains', [])
            if chains:
                bonus += 0.08  # Bonus for documented chains
        
        return min(bonus, 0.25)  # Cap at 25%
    
    def _integrate_stylometry(self, stylometric_score: float, base_confidence: float) -> float:
        """Integrate stylometric confidence score"""
        if stylometric_score <= 0:
            return 0.0
        
        # Stylometric score is 0-1, but only trust if high
        if stylometric_score >= 0.70:
            # High stylometric confidence significantly boosts reconstruction
            return 0.15
        elif stylometric_score >= 0.60:
            return 0.08
        elif stylometric_score >= 0.50:
            return 0.03
        
        return 0.0
    
    def _calculate_network_bonus(self, network_position: Dict = None) -> float:
        """Calculate bonus based on network centrality"""
        if not network_position:
            return 0.0
        
        bonus = 0.0
        
        # Degree centrality bonus
        centrality = network_position.get('degree_centrality', 0)
        if centrality > 5:
            bonus += 0.05
        elif centrality > 3:
            bonus += 0.03
        
        # Key transmitter bonus
        if network_position.get('is_key_transmitter', False):
            bonus += 0.08
        
        # Multiple independent lines bonus
        independent_lines = network_position.get('independent_lines', 0)
        if independent_lines >= 3:
            bonus += 0.10
        elif independent_lines == 2:
            bonus += 0.05
        
        return min(bonus, 0.15)
    
    def _bayesian_update(self, base_confidence: float, *factors) -> float:
        """
        Bayesian update of confidence with multiple evidence factors
        Uses log-odds space for proper probability combination
        """
        # Convert to log-odds
        def prob_to_logodds(p):
            if p <= 0:
                return -10
            if p >= 1:
                return 10
            return math.log(p / (1 - p))
        
        def logodds_to_prob(lo):
            return 1 / (1 + math.exp(-lo))
        
        # Start with base confidence in log-odds
        logodds = prob_to_logodds(base_confidence)
        
        # Add each factor as evidence
        for factor in factors:
            # Convert factor to evidence weight (factor is 0-1, but can be >1 for bonuses)
            evidence_weight = max(min(factor, 1.0), -0.5)  # Cap evidence
            logodds += evidence_weight * 2  # Multiply by 2 for impact
        
        # Convert back to probability
        updated_prob = logodds_to_prob(logodds)
        
        # Ensure reasonable bounds
        return max(0.0, min(1.0, updated_prob))
    
    def _get_confidence_level(self, confidence: float) -> str:
        """Convert confidence score to descriptive level"""
        if confidence >= 0.85:
            return "very_high"
        elif confidence >= 0.70:
            return "high"
        elif confidence >= 0.55:
            return "moderate"
        elif confidence >= 0.40:
            return "low"
        else:
            return "very_low"
    
    def _generate_recommendations(self, components: Dict, final_confidence: float) -> List[str]:
        """Generate recommendations based on confidence components"""
        recommendations = []
        
        if components['citation_quality'] < 0.6:
            recommendations.append("Search for higher-quality citations (direct quotes, fragments)")
        
        if components['temporal_weight'] < 0.6:
            recommendations.append("Find citations from additional centuries for temporal spread")
        
        if components['cultural_bonus'] < 0.1:
            recommendations.append("Investigate Arabic/Latin translations for cross-cultural attestation")
        
        if components['network_bonus'] < 0.05:
            recommendations.append("Identify key transmitter sources for network centrality")
        
        if final_confidence >= 0.70:
            recommendations.append("Confidence sufficient for Fragment Alert - issue to scholarly community")
            recommendations.append("Prepare reconstruction for peer review")
        else:
            recommendations.append("Continue fragment hunting before issuing alert")
        
        return recommendations
    
    def enhance_all_reconstructions(self, 
                                  reconstructions: List[Dict],
                                  lost_works: List[Dict],
                                  stylometric_data: Dict = None,
                                  translation_data: List[Dict] = None,
                                  network_data: Dict = None) -> List[Dict]:
        """Enhance confidence for all reconstructions"""
        print("=" * 60)
        print("CONFIDENCE ENHANCEMENT: BATCH PROCESSING")
        print("=" * 60)
        
        enhanced_results = []
        alerts_triggered = 0
        
        for i, (reconstruction, lost_work) in enumerate(zip(reconstructions, lost_works)):
            print(f"\n[{i+1}/{len(reconstructions)}] Enhancing '{lost_work['title']}'...")
            
            # Get associated data
            stylometric = stylometric_data.get(lost_work['title'], 0.0) if stylometric_data else 0.0
            translation = next((t for t in translation_data if t['work_title'] == lost_work['title']), None) if translation_data else None
            network = network_data.get(lost_work['title'], {}) if network_data else {}
            
            # Enhance confidence
            result = self.calculate_enhanced_confidence(
                reconstruction, lost_work, stylometric, translation, network
            )
            
            enhanced_results.append(result)
            
            if result['alert_recommended']:
                alerts_triggered += 1
                print(f"  🚨 ALERT TRIGGERED: {result['enhanced_confidence']:.1%} confidence")
        
        print(f"\n[ENHANCEMENT COMPLETE] {alerts_triggered}/{len(reconstructions)} alerts triggered")
        
        return enhanced_results
    
    def save_enhancement_report(self, results: List[Dict], filename: str = None) -> str:
        """Save comprehensive enhancement report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/Volumes/VIXinSSD/callimachina/pinakes/confidence_enhancement_{timestamp}.yml"
        
        # Ensure directory exists
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        report = {
            'report_timestamp': datetime.now().isoformat(),
            'enhancement_summary': {
                'total_reconstructions': len(results),
                'alerts_triggered': sum(1 for r in results if r['alert_recommended']),
                'average_confidence': sum(r['enhanced_confidence'] for r in results) / len(results) if results else 0,
                'average_improvement': sum(r['components']['enhancement_magnitude'] for r in results) / len(results) if results else 0
            },
            'confidence_distribution': self._calculate_distribution(results),
            'results': results
        }
        
        with open(filename, 'w') as f:
            yaml.dump(report, f, default_flow_style=False, allow_unicode=True)
        
        print(f"[ENHANCEMENT REPORT] Saved to {filename}")
        return filename
    
    def _calculate_distribution(self, results: List[Dict]) -> Dict:
        """Calculate confidence distribution"""
        distribution = {
            'very_high': 0,
            'high': 0,
            'moderate': 0,
            'low': 0,
            'very_low': 0
        }
        
        for result in results:
            level = result['confidence_level']
            distribution[level] += 1
        
        return distribution

if __name__ == "__main__":
    print("=" * 60)
    print("CALLIMACHINA CONFIDENCE ENHANCEMENT ENGINE")
    print("=" * 60)
    
    enhancer = ConfidenceEnhancer()
    
    # Test with Eratosthenes
    test_reconstruction = {
        'overall_confidence': 0.63,
        'confidence_map': [],
        'critical_apparatus': []
    }
    
    test_lost_work = {
        'title': 'Eratosthenes Geographika',
        'citations': [
            {'source': 'Strabo', 'citation_type': 'direct_quote', 'language': 'greek', 'date_range': 'c. 64 BCE-24 CE', 'independence_score': 0.8},
            {'source': 'Cleomedes', 'citation_type': 'paraphrase', 'language': 'greek', 'date_range': 'c. 1st century CE', 'independence_score': 0.7},
            {'source': 'Ptolemy', 'citation_type': 'citation', 'language': 'greek', 'date_range': 'c. 100-170 CE', 'independence_score': 0.9},
            {'source': 'Stobaeus', 'citation_type': 'fragment', 'language': 'greek', 'date_range': 'c. 5th century CE', 'independence_score': 0.6}
        ],
        'survival_paths': ['greek_direct', 'arabic_translation', 'latin_translation'],
        'priority_score': 98
    }
    
    test_translation = {
        'translations_found': [
            {'language': 'arabic', 'confidence': 0.85},
            {'language': 'latin', 'confidence': 0.80}
        ],
        'translation_chains': [
            {'chain_type': 'greek_to_arabic', 'confidence': 0.75},
            {'chain_type': 'greek_to_latin', 'confidence': 0.80}
        ]
    }
    
    test_network = {
        'degree_centrality': 4,
        'independent_lines': 3,
        'is_key_transmitter': False
    }
    
    print("\n[Test] Enhancing Eratosthenes Geographika confidence...")
    result = enhancer.calculate_enhanced_confidence(
        test_reconstruction,
        test_lost_work,
        stylometric_score=0.0,  # No stylometric data
        translation_data=test_translation,
        network_position=test_network
    )
    
    print(f"\n[RESULT] Enhanced confidence: {result['enhanced_confidence']:.1%}")
    print(f"[RESULT] Alert recommended: {result['alert_recommended']}")
    print(f"[RESULT] Confidence level: {result['confidence_level']}")
    
    # Save test report
    enhancer.save_enhancement_report([result], '/Volumes/VIXinSSD/callimachina/pinakes/test_enhancement.yml')
    
    print("\n[CONFIDENCE ENHANCEMENT] Test complete")
