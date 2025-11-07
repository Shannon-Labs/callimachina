#!/usr/bin/env python3
"""
Batch Processing Example

Demonstrates how to reconstruct multiple works efficiently
and compare their confidence scores.
"""

from pinakes.integration_engine import IntegrationEngine
import time

def main():
    """Process multiple works in batch."""
    
    print("🏛️  CALLIMACHINA: Batch Processing Example")
    print("=" * 60)
    
    # Works to reconstruct
    works = [
        "Eratosthenes Geographika",
        "Hippolytus On Heraclitus", 
        "Posidippus Epigrams",
        "Callimachus Aetia"
    ]
    
    print(f"\n📚 Processing {len(works)} works:")
    for i, work in enumerate(works, 1):
        print(f"   {i}. {work}")
    
    # Initialize engine
    print(f"\n⚙️  Initializing engine...")
    engine = IntegrationEngine(verbose=False)
    
    # Process all works
    start_time = time.time()
    
    try:
        results = engine.run_full_pipeline(
            target_works=works,
            confidence_threshold=0.90
        )
        
        elapsed = time.time() - start_time
        
        # Display summary
        print(f"\n✅ Batch processing complete in {elapsed:.2f} seconds")
        print("\n" + "=" * 60)
        print(f"{'Work':<35} {'Confidence':<12} {'Fragments'}")
        print("-" * 60)
        
        total_confidence = 0
        total_fragments = 0
        
        for work in works:
            if work in results:
                recon = results[work]
                conf = recon['confidence']
                frags = len(recon['fragments'])
                
                print(f"{work:<35} {conf:>8.1%}      {frags:>3}")
                
                total_confidence += conf
                total_fragments += frags
            else:
                print(f"{work:<35} {'FAILED':<12} {'N/A'}")
        
        print("-" * 60)
        print(f"{'AVERAGE':<35} {total_confidence/len(works):>8.1%}      {total_fragments:>3}")
        
        # Save comparison report
        print(f"\n💾 Detailed comparison saved to:")
        print(f"   callimachina/discoveries/batch_comparison_report.yml")
        
    except Exception as e:
        print(f"❌ Batch processing failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())