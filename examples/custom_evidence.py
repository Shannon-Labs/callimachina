#!/usr/bin/env python3
"""
Custom Evidence Weighting Example

Demonstrates how to adjust Bayesian evidence factors
for specific research questions.
"""

from pinakes.integration_engine import IntegrationEngine
from pinakes.reconstruction_engine import BayesianReconstructor

def main():
    """Demonstrate custom evidence weighting."""
    
    print("🏛️  CALLIMACHINA: Custom Evidence Weighting Example")
    print("=" * 60)
    
    target_work = "Hippolytus On Heraclitus"
    
    # Standard reconstruction (balanced weights)
    print("\n1. Standard Reconstruction (Balanced Weights)")
    print("-" * 60)
    
    engine = IntegrationEngine(verbose=False)
    standard_results = engine.reconstruct_work(target_work)
    
    if standard_results:
        print(f"Confidence: {standard_results['confidence']:.1%}")
        print("\nEvidence Factors:")
        for factor, weight in standard_results['evidence_factors'].items():
            print(f"   {factor:<25} {weight:.1%}")
    
    # Custom reconstruction (emphasizing source quality)
    print("\n2. Custom Reconstruction (Emphasizing Source Quality)")
    print("-" * 60)
    
    custom_weights = {
        'citation_quality': 0.4,      # Increased from 0.3
        'temporal_distribution': 0.1,  # Decreased from 0.2
        'translation_path': 0.3,       # Increased from 0.2
        'stylometric_score': 0.1,      # Decreased from 0.15
        'network_centrality': 0.05,    # Decreased from 0.1
        'genre_base_rate': 0.05        # Same
    }
    
    reconstructor = BayesianReconstructor(
        prior_strength=0.5,
        evidence_weights=custom_weights
    )
    
    # Get fragments for reconstruction
    print("\n   Scraping fragments...")
    from pinakes.scrapers.papyri_scraper import FragmentScraper
    scraper = FragmentScraper()
    fragments = scraper.scrape_work(target_work)
    
    print(f"   Found {len(fragments)} fragments")
    
    # Build citation network
    print("   Building citation network...")
    from pinakes.network_builder import CitationNetwork
    network = CitationNetwork()
    network.build_from_fragments(fragments)
    
    # Custom reconstruction
    custom_results = reconstructor.reconstruct(
        fragments=fragments,
        citations=network
    )
    
    if custom_results:
        print(f"\nConfidence: {custom_results['confidence']:.1%}")
        print("\nEvidence Factors:")
        for factor, weight in custom_results['evidence_factors'].items():
            print(f"   {factor:<25} {weight:.1%}")
    
    # Compare results
    print("\n3. Comparison")
    print("-" * 60)
    
    if standard_results and custom_results:
        std_conf = standard_results['confidence']
        cust_conf = custom_results['confidence']
        diff = cust_conf - std_conf
        
        print(f"Standard Confidence:    {std_conf:.1%}")
        print(f"Custom Confidence:      {cust_conf:.1%}")
        print(f"Difference:             {diff:+.1%}")
        
        if diff > 0:
            print("\n✅ Custom weights improved confidence!")
        else:
            print("\n⚠️  Custom weights decreased confidence")
            print("   Consider adjusting weights or research question")
    
    print("\n" + "=" * 60)
    print("Example completed!")
    return 0

if __name__ == "__main__":
    exit(main())