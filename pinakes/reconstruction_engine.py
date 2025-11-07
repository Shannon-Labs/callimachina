#!/usr/bin/env python3
"""
Reconstruction Engine for CALLIMACHINA Protocol
Builds probabilistic reconstructions from fragments and citations
"""

import re
import yaml
import json
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict
import random

class ReconstructionEngine:
    def __init__(self):
        self.reconstructions = {}
        self.confidence_threshold = 0.75
        
        # Reconstruction templates for different genres
        self.genre_templates = {
            'geography': ['measurement', 'location', 'distance', 'description'],
            'philosophy': ['argument', 'definition', 'example', 'conclusion'],
            'epigram': ['theme', 'wordplay', 'meter', 'structure'],
            'science': ['observation', 'calculation', 'hypothesis', 'conclusion']
        }
    
    def reconstruct_work(self, lost_work: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate probabilistic reconstruction of a lost work
        """
        title = lost_work['title']
        print(f"[RECONSTRUCTION BEGIN] '{title}'...")
        
        reconstruction = {
            'title': f"{title} (Probabilistic Reconstruction)",
            'fragments': len(lost_work['citations']),
            'confidence_map': [],
            'critical_apparatus': [],
            'authenticity_risk': self._assess_authenticity_risk(lost_work),
            'next_steps': [],
            'reconstructed_timestamp': datetime.now().isoformat()
        }
        
        # Process each citation as a potential fragment
        for i, citation in enumerate(lost_work['citations'], 1):
            fragment = self._process_citation_as_fragment(citation, i)
            if fragment:
                reconstruction['confidence_map'].append(fragment)
        
        # Add critical apparatus notes
        reconstruction['critical_apparatus'] = self._generate_critical_notes(lost_work)
        
        # Generate next steps for further research
        reconstruction['next_steps'] = self._generate_next_steps(lost_work)
        
        # Calculate overall reconstruction confidence
        avg_confidence = sum(f['confidence'] for f in reconstruction['confidence_map']) / len(reconstruction['confidence_map']) if reconstruction['confidence_map'] else 0
        reconstruction['overall_confidence'] = avg_confidence
        
        print(f"[RECONSTRUCTION COMPLETE] '{title}' - {len(reconstruction['confidence_map'])} fragments mapped")
        print(f"Overall Confidence: {avg_confidence:.2%}")
        
        return reconstruction
    
    def _process_citation_as_fragment(self, citation: Dict[str, Any], fragment_id: int) -> Optional[Dict[str, Any]]:
        """
        Process a single citation as a reconstructed fragment
        """
        source = citation['source']
        location = citation['location']
        confidence = citation.get('independence_score', 0.5)
        
        # Generate reconstructed text based on citation type
        if citation['citation_type'] == 'direct_quote':
            text = self._reconstruct_direct_quote(source, location)
            confidence *= 0.95
        elif citation['citation_type'] == 'paraphrase':
            text = self._reconstruct_paraphrase(source, location)
            confidence *= 0.75
        elif citation['citation_type'] == 'fragment':
            text = self._reconstruct_fragment(source, location)
            confidence *= 0.85
        elif citation['citation_type'] == 'extensive_paraphrase':
            text = self._reconstruct_extensive_paraphrase(source, location)
            confidence *= 0.80
        else:
            text = self._reconstruct_generic(source, location)
            confidence *= 0.60
        
        return {
            'fragment_id': fragment_id,
            'text': text,
            'confidence': confidence,
            'sources': [f"{source} {location}"],
            'citation_type': citation['citation_type'],
            'language': citation['language']
        }
    
    def _reconstruct_direct_quote(self, source: str, location: str) -> str:
        """
        Reconstruct likely direct quote content
        """
        quote_templates = {
            'Strabo': {
                'geography': "...the distance between {location1} and {location2} is {distance} stadia...",
                'mathematics': "...according to the calculation of {author}, the {measurement} is {value}..."
            },
            'Cleomedes': {
                'astronomy': "...as {author} demonstrated, the {celestial_body} {observation}..."
            },
            'Ptolemy': {
                'geography': "...{author} states that the {location} lies at {coordinates}..."
            }
        }
        
        # Simplified reconstruction - would use actual content analysis in production
        if 'Strabo' in source:
            return f"...according to the ancient measurement recorded by {source}, the location in question demonstrates significant geographical relationships..."
        elif 'Cleomedes' in source:
            return f"...the astronomical observation as transmitted through {source} indicates..."
        elif 'Ptolemy' in source:
            return f"...{source} preserves the original calculation that..."
        else:
            return f"...direct quotation preserved in {source} {location}..."
    
    def _reconstruct_paraphrase(self, source: str, location: str) -> str:
        """Reconstruct likely paraphrased content"""
        return f"[PARAPHRASED CONTENT: The original meaning as preserved in {source} {location} suggests...]"
    
    def _reconstruct_fragment(self, source: str, location: str) -> str:
        """Reconstruct fragmentary content"""
        return f"...fragmentary text preserved in {source} {location}..."
    
    def _reconstruct_extensive_paraphrase(self, source: str, location: str) -> str:
        """Reconstruct extensive paraphrase"""
        return f"[EXTENSIVE PARAPHRASE: Detailed summary of original arguments as transmitted through {source} {location}]"
    
    def _reconstruct_generic(self, source: str, location: str) -> str:
        """Generic reconstruction placeholder"""
        return f"[CONTENT RECONSTRUCTION: Material cited in {source} {location}]"
    
    def _assess_authenticity_risk(self, lost_work: Dict[str, Any]) -> str:
        """
        Assess risk of authenticity issues
        """
        risk_factors = []
        
        # Check for single-source dependencies
        sources = [c['source'] for c in lost_work['citations']]
        if len(set(sources)) == 1:
            risk_factors.append("Single source dependency")
        
        # Check for late attestation
        late_sources = [c for c in lost_work['citations'] if 'Stobaeus' in c['source'] or 'Suda' in c['source']]
        if len(late_sources) > len(lost_work['citations']) / 2:
            risk_factors.append("Predominantly late attestation")
        
        # Check for translation dependencies
        non_greek = [c for c in lost_work['citations'] if c['language'] != 'greek']
        if len(non_greek) > 0:
            risk_factors.append("Translation dependencies")
        
        if not risk_factors:
            return "Low"
        elif len(risk_factors) == 1:
            return f"Moderate ({risk_factors[0]})"
        else:
            return f"High ({'; '.join(risk_factors)})"
    
    def _generate_critical_notes(self, lost_work: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate critical apparatus notes
        """
        notes = []
        
        # Note on textual variants
        if len(lost_work['citations']) > 2:
            notes.append({
                'note': 'Multiple citation sources suggest textual variants in transmission',
                'impact': 'Reconstruction may contain alternative readings'
            })
        
        # Note on measurement ambiguities (for scientific works)
        if 'Eratosthenes' in lost_work['title'] or 'geograph' in lost_work['title'].lower():
            notes.append({
                'note': 'Stadium length ambiguous: Attic (185m) vs Egyptian (157m)',
                'impact': 'Earth size estimate range: 39,690-46,620 km'
            })
        
        # Note on lacunae
        total_coverage = len(lost_work['citations']) * 0.1  # Assume ~10% coverage per citation
        if total_coverage < 0.5:
            lacuna_size = "large" if total_coverage < 0.2 else "moderate"
            notes.append({
                'note': f'Significant lacunae expected ({lacuna_size} portions of text missing)',
                'impact': 'Reconstruction represents partial preservation only'
            })
        
        return notes
    
    def _generate_next_steps(self, lost_work: Dict[str, Any]) -> List[str]:
        """
        Generate next steps for further research
        """
        steps = []
        
        # Always include papyrus search
        steps.append("Query multispectral imaging of relevant codices for undertext")
        
        # Cross-reference with unpublished papyri
        steps.append("Cross-reference with unpublished Oxyrhynchus papyri in Sackler inventory")
        
        # Check for Arabic/Latin translations
        if any('greek' in c['language'] for c in lost_work['citations']):
            steps.append("Search for Arabic and Latin translation variants")
        
        # Collaborative calls
        if lost_work['priority_score'] > 150:
            steps.append("Issue collaborative call for related fragments across collections")
        
        # Specific recommendations based on work type
        if 'Eratosthenes' in lost_work['title']:
            steps.append("Check Armenian geographical treatises for parallel calculations")
        elif 'Posidippus' in lost_work['title']:
            steps.append("Scan Milan papyrus for additional epigrammatic fragments")
        
        return steps
    
    def save_reconstruction(self, reconstruction: Dict[str, Any], filename: str = None):
        """Save reconstruction to file"""
        if not filename:
            title_slug = reconstruction['title'].split('(')[0].strip().replace(' ', '_').lower()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/Volumes/VIXinSSD/callimachina/pinakes/reconstructions/{title_slug}_{timestamp}.yml"
        
        with open(filename, 'w') as f:
            yaml.dump(reconstruction, f, default_flow_style=False, allow_unicode=True)
        
        print(f"[RECONSTRUCTION SAVED] {filename}")
        return filename
    
    def issue_fragment_alert(self, reconstruction: Dict[str, Any], priority_score: int = 0):
        """Issue Fragment Alert for high-confidence reconstructions (weighted by priority)"""
        # Weighted threshold: base 55% for major works, more aggressive scaling
        # High priority (90+) can trigger alerts at 55-65% confidence
        weighted_threshold = max(0.55, min(0.70, 0.55 + (priority_score / 2000)))
        
        # Special case: Priority >95 triggers at 50% confidence
        if priority_score >= 95:
            weighted_threshold = 0.50
        
        if reconstruction['overall_confidence'] >= weighted_threshold:
            alert = {
                'alert_type': 'FRAGMENT_ALERT',
                'timestamp': datetime.now().isoformat(),
                'work_title': reconstruction['title'],
                'confidence': reconstruction['overall_confidence'],
                'priority_score': priority_score,
                'weighted_threshold': weighted_threshold,
                'fragments_mapped': len(reconstruction['confidence_map']),
                'critical_notes': len(reconstruction['critical_apparatus']),
                'next_steps': reconstruction['next_steps'],
                'message': f"High-priority reconstruction available for {reconstruction['title']}"
            }
            
            alert_file = f"/Volumes/VIXinSSD/callimachina/pinakes/alerts/fragment_alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yml"
            with open(alert_file, 'w') as f:
                yaml.dump(alert, f, default_flow_style=False)
            
            print(f"[FRAGMENT ALERT ISSUED] {reconstruction['title']} - Confidence: {reconstruction['overall_confidence']:.2%} (Threshold: {weighted_threshold:.2%})")
            return alert_file
        else:
            print(f"[ALERT SKIPPED] Confidence {reconstruction['overall_confidence']:.2%} below weighted threshold {weighted_threshold:.2%}")
            return None

if __name__ == "__main__":
    engine = ReconstructionEngine()
    
    print("=" * 60)
    print("CALLIMACHINA RECONSTRUCTION ENGINE INITIALIZATION")
    print("=" * 60)
    
    # Example reconstructions would be triggered by actual triangulation results
    print("[READY] Reconstruction engine initialized and awaiting triangulation data...")
