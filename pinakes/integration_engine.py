#!/usr/bin/env python3
"""
Integration Engine for CALLIMACHINA Protocol
Connects all modules into unified reconstruction pipeline

Orchestrates: papyri scraping → citation triangulation → stylometry → translation hunting → confidence enhancement → alerts
"""

import os
import sys
import yaml
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path

# Import all CALLIMACHINA modules
sys.path.append('/Volumes/VIXinSSD/callimachina/pinakes/scrapers')
sys.path.append('/Volumes/VIXinSSD/callimachina/pinakes')

from papyri_scraper_enhanced import PapyriScraperEnhanced
from citation_triangulator import CitationTriangulator
from reconstruction_engine import ReconstructionEngine
from stylometry_enhanced import StylometricEnhanced
from network_builder import NetworkBuilder
from translation_hunter import TranslationHunter
from confidence_enhancer import ConfidenceEnhancer

class IntegrationEngine:
    def __init__(self):
        print("=" * 80)
        print("CALLIMACHINA INTEGRATION ENGINE v2.0")
        print("Full Alexandria Reconstruction Pipeline")
        print("=" * 80)
        
        # Initialize all subsystems
        self.scraper = PapyriScraperEnhanced()
        self.triangulator = CitationTriangulator()
        self.reconstructor = ReconstructionEngine()
        self.stylometer = StylometricEnhanced()
        self.network_builder = NetworkBuilder()
        self.translation_hunter = TranslationHunter()
        self.confidence_enhancer = ConfidenceEnhancer()
        
        print("[INTEGRATION] All subsystems initialized and ready")
        self.activation_time = datetime.now()
    
    def run_full_pipeline(self, target_works: List[str] = None, 
                         enable_stylometry: bool = True,
                         enable_translations: bool = True,
                         enable_network: bool = True) -> Dict:
        """
        Run complete reconstruction pipeline from fragments to alerts
        """
        print("\n" + "=" * 80)
        print("[PIPELINE START] Full Alexandria Reconstruction Sequence")
        print("=" * 80)
        
        results = {
            'pipeline_timestamp': datetime.now().isoformat(),
            'phases_completed': [],
            'fragments_found': 0,
            'ghosts_confirmed': 0,
            'reconstructions_completed': 0,
            'stylometric_analyses': 0,
            'translation_discoveries': 0,
            'networks_built': 0,
            'enhanced_confidences': 0,
            'alerts_issued': 0,
            'enhanced_alerts': 0,
            'works_processed': []
        }
        
        # PHASE 1: Papyrus Hunt
        print("\n[PHASE 1] PAPYRUS HUNT")
        print("-" * 80)
        fragments = self._run_papyrus_hunt()
        results['fragments_found'] = len(fragments)
        results['phases_completed'].append('papyrus_hunt')
        
        # PHASE 2: Citation Triangulation
        print("\n[PHASE 2] CITATION TRIANGULATION")
        print("-" * 80)
        if target_works:
            lost_works = self._run_targeted_triangulation(target_works)
        else:
            lost_works = self._run_full_triangulation()
        
        results['ghosts_confirmed'] = len(lost_works)
        results['phases_completed'].append('citation_triangulation')
        
        # PHASE 3: Reconstruction
        print("\n[PHASE 3] RECONSTRUCTION")
        print("-" * 80)
        reconstructions = self._run_reconstruction_batch(lost_works)
        results['reconstructions_completed'] = len(reconstructions)
        results['phases_completed'].append('reconstruction')
        
        # PHASE 4: Stylometric Analysis (optional)
        stylometric_results = {}
        if enable_stylometry:
            print("\n[PHASE 4] STYLOMETRIC FINGERPRINTING")
            print("-" * 80)
            stylometric_results = self._run_stylometric_analysis(fragments)
            results['stylometric_analyses'] = len(stylometric_results)
            results['phases_completed'].append('stylometry')
        
        # PHASE 5: Translation Hunting (optional)
        translation_results = []
        if enable_translations:
            print("\n[PHASE 5] TRANSLATION HUNTING")
            print("-" * 80)
            translation_results = self._run_translation_hunt(lost_works)
            results['translation_discoveries'] = sum(len(t['translations_found']) for t in translation_results)
            results['phases_completed'].append('translation_hunt')
        
        # PHASE 6: Network Building (optional)
        network_data = {}
        if enable_network:
            print("\n[PHASE 6] NETWORK VISUALIZATION")
            print("-" * 80)
            network_data = self._run_network_building(lost_works)
            results['networks_built'] = 1
            results['phases_completed'].append('network_building')
        
        # PHASE 7: Confidence Enhancement
        print("\n[PHASE 7] CONFIDENCE ENHANCEMENT")
        print("-" * 80)
        enhanced_results = self._run_confidence_enhancement(
            reconstructions, lost_works, stylometric_results, translation_results, network_data
        )
        results['enhanced_confidences'] = len(enhanced_results)
        results['phases_completed'].append('confidence_enhancement')
        
        # PHASE 8: Alert Generation
        print("\n[PHASE 8] FRAGMENT ALERT GENERATION")
        print("-" * 80)
        alerts = self._run_alert_generation(enhanced_results, reconstructions)
        results['enhanced_alerts'] = len(alerts)
        results['phases_completed'].append('alert_generation')
        
        # Compile final results
        results['works_processed'] = self._compile_work_summaries(
            lost_works, reconstructions, enhanced_results, stylometric_results, translation_results
        )
        
        # Save comprehensive report
        self._save_pipeline_report(results)
        
        # Print summary
        self._print_pipeline_summary(results)
        
        return results
    
    def _run_papyrus_hunt(self) -> List[Dict]:
        """Run papyrus scraping phase"""
        print("Scraping papyri.info for new fragments...")
        
        # Get fragments from major collections
        oxy_fragments = self.scraper.get_oxyrhynchus_batch(limit=20)
        herc_fragments = self.scraper.get_herculaneum_batch(limit=15)
        
        # Search for specific authors
        posidippus_fragments = self.scraper.search_by_author("Posidippus", limit=10)
        callimachina_fragments = self.scraper.search_by_author("Callimachus", limit=10)
        
        all_fragments = oxy_fragments + herc_fragments + posidippus_fragments + callimachina_fragments
        
        print(f"  → Found {len(oxy_fragments)} Oxyrhynchus fragments")
        print(f"  → Found {len(herc_fragments)} Herculaneum fragments")
        print(f"  → Found {len(posidippus_fragments)} Posidippus fragments")
        print(f"  → Found {len(callimachina_fragments)} Callimachus fragments")
        print(f"  → Total: {len(all_fragments)} fragments catalogued")
        
        # Save combined batch
        if all_fragments:
            self.scraper.save_fragments(all_fragments, 
                "/Volumes/VIXinSSD/callimachina/pinakes/fragments/pipeline_batch.yml")
        
        return all_fragments
    
    def _run_targeted_triangulation(self, target_works: List[str]) -> List[Dict]:
        """Run citation triangulation for specific works"""
        print(f"Triangulating {len(target_works)} target works...")
        
        lost_works = []
        for work_title in target_works:
            result = self.triangulator.triangulate_lost_work(work_title)
            if result:
                lost_works.append(result)
                print(f"  ✓ {work_title}: {result['citation_count']} citations, priority {result['priority_score']}")
            else:
                print(f"  ✗ {work_title}: Insufficient citations")
        
        # Save results
        if lost_works:
            self.triangulator.save_triangulation_results(lost_works,
                "/Volumes/VIXinSSD/callimachina/pinakes/pipeline_triangulation.yml")
        
        return lost_works
    
    def _run_full_triangulation(self) -> List[Dict]:
        """Run full ghost hunting on high-priority targets"""
        print("Running full ghost hunting on high-priority targets...")
        
        lost_works = self.triangulator.hunt_high_priority_targets()
        
        print(f"  → Confirmed {len(lost_works)} high-priority ghosts")
        for work in lost_works:
            print(f"    - {work['title']}: priority {work['priority_score']}")
        
        return lost_works
    
    def _run_reconstruction_batch(self, lost_works: List[Dict]) -> List[Dict]:
        """Reconstruct all confirmed lost works"""
        print(f"Reconstructing {len(lost_works)} lost works...")
        
        reconstructions = []
        for work in lost_works:
            reconstruction = self.reconstructor.reconstruct_work(work)
            reconstructions.append(reconstruction)
            
            # Save individual reconstruction
            self.reconstructor.save_reconstruction(reconstruction)
            
            print(f"  ✓ {work['title']}: {len(reconstruction['confidence_map'])} fragments, {reconstruction['overall_confidence']:.1%} confidence")
        
        return reconstructions
    
    def _run_stylometric_analysis(self, fragments: List[Dict]) -> Dict:
        """Run stylometric analysis on fragments"""
        print(f"Analyzing {len(fragments)} fragments with stylometry...")
        
        # Filter fragments with sufficient text
        analyzable_fragments = [f for f in fragments if len(f.get('text', '')) > 50]
        
        print(f"  → {len(analyzable_fragments)} fragments suitable for analysis")
        
        if not analyzable_fragments:
            return {}
        
        # Run attribution
        results = self.stylometer.analyze_fragment_collection(analyzable_fragments)
        
        # Save results
        self.stylometer.save_attribution_report(results, 
            "/Volumes/VIXinSSD/callimachina/pinakes/pipeline_stylometric.yml")
        
        # Create lookup dict by fragment ID
        stylometric_dict = {}
        for result in results:
            fragment_id = result['fragment_id']
            stylometric_dict[fragment_id] = result['confidence']
        
        print(f"  → Attributed {len(results)} fragments to likely authors")
        
        return stylometric_dict
    
    def _run_translation_hunt(self, lost_works: List[Dict]) -> List[Dict]:
        """Hunt for translations of lost works"""
        print(f"Hunting for translations of {len(lost_works)} works...")
        
        translation_results = []
        for work in lost_works:
            result = self.translation_hunter.hunt_translations(work['title'])
            translation_results.append(result)
            
            # Save individual report
            self.translation_hunter.save_translation_report(result)
            
            if result['translations_found']:
                print(f"  ✓ {work['title']}: {len(result['translations_found'])} translations found")
            else:
                print(f"  - {work['title']}: No translations found")
        
        return translation_results
    
    def _run_network_building(self, lost_works: List[Dict]) -> Dict:
        """Build citation network"""
        print(f"Building citation network for {len(lost_works)} works...")
        
        network = self.network_builder.build_transmission_network(lost_works)
        
        # Export all formats
        gexf_file = self.network_builder.export_gephi()
        json_file = self.network_builder.export_cytoscape()
        report_file = self.network_builder.generate_network_report()
        
        print(f"  → Network: {len(network['nodes'])} nodes, {len(network['edges'])} edges")
        print(f"  → Gephi export: {Path(gexf_file).name}")
        print(f"  → Cytoscape export: {Path(json_file).name}")
        print(f"  → Analysis report: {Path(report_file).name}")
        
        # Create lookup dict by work title
        network_dict = {}
        for work in lost_works:
            work_id = work['title'].replace(' ', '_').lower()
            node = network['nodes'].get(work_id, {})
            network_dict[work['title']] = {
                'degree_centrality': node.get('degree_centrality', 0),
                'is_key_transmitter': node.get('role') == 'key_transmitter',
                'independent_lines': work.get('citation_count', 0)
            }
        
        return network_dict
    
    def _run_confidence_enhancement(self, reconstructions: List[Dict], 
                                   lost_works: List[Dict],
                                   stylometric_data: Dict,
                                   translation_data: List[Dict],
                                   network_data: Dict) -> List[Dict]:
        """Run confidence enhancement on all reconstructions"""
        print(f"Enhancing confidence for {len(reconstructions)} reconstructions...")
        
        enhanced_results = []
        for reconstruction, lost_work in zip(reconstructions, lost_works):
            # Get associated data
            stylometric = stylometric_data.get(lost_work['title'], 0.0)
            translation = next((t for t in translation_data if t['work_title'] == lost_work['title']), None)
            network = network_data.get(lost_work['title'], {})
            
            # Enhance confidence
            result = self.confidence_enhancer.calculate_enhanced_confidence(
                reconstruction, lost_work, stylometric, translation, network
            )
            
            enhanced_results.append(result)
            
            print(f"  → {lost_work['title']}: {reconstruction['overall_confidence']:.1%} → {result['enhanced_confidence']:.1%}")
        
        # Save enhancement report
        self.confidence_enhancer.save_enhancement_report(enhanced_results,
            "/Volumes/VIXinSSD/callimachina/pinakes/pipeline_enhancement.yml")
        
        return enhanced_results
    
    def _run_alert_generation(self, enhanced_results: List[Dict], reconstructions: List[Dict]) -> List[Dict]:
        """Generate Fragment Alerts for high-confidence reconstructions"""
        print(f"Generating alerts for {len(enhanced_results)} enhanced results...")
        
        alerts = []
        for i, (enhanced, reconstruction) in enumerate(zip(enhanced_results, reconstructions)):
            if enhanced['alert_recommended']:
                # Generate enhanced alert
                alert = {
                    'alert_type': 'ENHANCED_RECONSTRUCTION',
                    'timestamp': datetime.now().isoformat(),
                    'work_title': enhanced['work_title'],
                    'confidence': enhanced['enhanced_confidence'],
                    'confidence_level': enhanced['confidence_level'],
                    'base_confidence': reconstruction['overall_confidence'],
                    'enhancement_magnitude': enhanced['components']['enhancement_magnitude'],
                    'components': enhanced['components'],
                    'fragments_mapped': len(reconstruction['confidence_map']),
                    'critical_notes': len(reconstruction['critical_apparatus']),
                    'next_steps': enhanced['recommendations'],
                    'message': f"High-confidence reconstruction with Bayesian enhancement: {enhanced['work_title']}"
                }
                
                alert_file = f"/Volumes/VIXinSSD/callimachina/pinakes/alerts/enhanced_alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.yml"
                with open(alert_file, 'w') as f:
                    yaml.dump(alert, f, default_flow_style=False)
                
                print(f"  🚨 ENHANCED ALERT: {enhanced['work_title']} - {enhanced['enhanced_confidence']:.1%} confidence")
                alerts.append(alert)
        
        print(f"  → Generated {len(alerts)} enhanced alerts")
        
        return alerts
    
    def _compile_work_summaries(self, lost_works: List[Dict], reconstructions: List[Dict],
                               enhanced_results: List[Dict], stylometric_data: Dict,
                               translation_data: List[Dict]) -> List[Dict]:
        """Compile comprehensive summaries for each work"""
        summaries = []
        
        for i, (work, reconstruction, enhanced) in enumerate(zip(lost_works, reconstructions, enhanced_results)):
            summary = {
                'work_title': work['title'],
                'status': 'reconstructed',
                'citation_confidence': work.get('confidence', 0),
                'base_reconstruction_confidence': reconstruction['overall_confidence'],
                'enhanced_confidence': enhanced['enhanced_confidence'],
                'fragments_mapped': len(reconstruction['confidence_map']),
                'citation_count': work.get('citation_count', 0),
                'priority_score': work.get('priority_score', 0),
                'survival_paths': work.get('survival_paths', []),
                'alert_issued': enhanced['alert_recommended'],
                'confidence_level': enhanced['confidence_level']
            }
            
            # Add stylometric data if available
            if work['title'] in stylometric_data:
                summary['stylometric_confidence'] = stylometric_data[work['title']]
            
            # Add translation data if available
            translation = next((t for t in translation_data if t['work_title'] == work['title']), None)
            if translation:
                summary['translations_found'] = len(translation['translations_found'])
                summary['translation_chains'] = len(translation['translation_chains'])
            
            summaries.append(summary)
        
        return summaries
    
    def _save_pipeline_report(self, results: Dict):
        """Save comprehensive pipeline report"""
        report_file = "/Volumes/VIXinSSD/callimachina/pinakes/pipeline_report.yml"
        
        with open(report_file, 'w') as f:
            yaml.dump(results, f, default_flow_style=False, allow_unicode=True)
        
        print(f"\n[PIPELINE REPORT] Saved to {report_file}")
    
    def _print_pipeline_summary(self, results: Dict):
        """Print pipeline execution summary"""
        print("\n" + "=" * 80)
        print("CALLIMACHINA PIPELINE EXECUTION SUMMARY")
        print("=" * 80)
        
        print(f"\n📊 OVERALL STATISTICS")
        print(f"  Pipeline runtime: {(datetime.now() - self.activation_time).total_seconds():.2f} seconds")
        print(f"  Phases completed: {len(results['phases_completed'])}/8")
        print(f"  Works processed: {len(results['works_processed'])}")
        
        print(f"\n📜 RECONSTRUCTION ACHIEVEMENTS")
        print(f"  Fragments catalogued: {results['fragments_found']}")
        print(f"  Ghosts confirmed: {results['ghosts_confirmed']}")
        print(f"  Reconstructions completed: {results['reconstructions_completed']}")
        print(f"  Stylometric analyses: {results['stylometric_analyses']}")
        print(f"  Translation discoveries: {results['translation_discoveries']}")
        
        print(f"\n🚨 ALERTS GENERATED")
        print(f"  Enhanced confidence analyses: {results['enhanced_confidences']}")
        print(f"  Fragment alerts issued: {results['alerts_issued']}")
        print(f"  Enhanced alerts: {results['enhanced_alerts']}")
        
        print(f"\n🌐 NETWORK ANALYSIS")
        print(f"  Networks built: {results['networks_built']}")
        
        print(f"\n✅ PIPELINE STATUS: SUCCESS")
        print(f"📁 All reports saved to /Volumes/VIXinSSD/callimachina/pinakes/")
        
        print("\n" + "=" * 80)

def main():
    """Main execution"""
    engine = IntegrationEngine()
    
    # Run targeted pipeline on high-value works
    high_priority_targets = [
        "Eratosthenes Geographika",
        "Hippolytus On Heraclitus",
        "Posidippus Epigrams",
        "Callimachus Aetia"
    ]
    
    print("\n🚀 LAUNCHING INTEGRATED RECONSTRUCTION PIPELINE")
    print("Target: High-priority lost works with cross-cultural transmission")
    print("=" * 80)
    
    results = engine.run_full_pipeline(
        target_works=high_priority_targets,
        enable_stylometry=True,
        enable_translations=True,
        enable_network=True
    )
    
    print("\n🏛️  PIPELINE COMPLETE")
    print("The Alexandria Reconstruction Protocol continues the hunt...")

if __name__ == "__main__":
    main()
