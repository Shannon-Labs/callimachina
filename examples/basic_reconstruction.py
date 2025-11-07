#!/usr/bin/env python3
"""
Basic CALLIMACHINA Reconstruction Example

This example demonstrates the simplest way to reconstruct a lost work
using the CALLIMACHINA pipeline.
"""

from pinakes.integration_engine import IntegrationEngine

def main():
    """Run a basic reconstruction of Eratosthenes' Geographika."""
    
    print("🏛️  CALLIMACHINA: Basic Reconstruction Example")
    print("=" * 50)
    
    # Initialize the integration engine
    print("\n1. Initializing Integration Engine...")
    engine = IntegrationEngine(verbose=True)
    
    # Reconstruct a specific work
    target_work = "Eratosthenes Geographika"
    print(f"\n2. Reconstructing: {target_work}")
    
    try:
        results = engine.run_full_pipeline(
            target_works=[target_work],
            confidence_threshold=0.95
        )
        
        # Display results
        if target_work in results:
            reconstruction = results[target_work]
            
            print(f"\n✅ Reconstruction Complete!")
            print(f"   Confidence: {reconstruction['confidence']:.1%}")
            print(f"   Fragments: {len(reconstruction['fragments'])}")
            print(f"   Sources: {len(reconstruction.get('citation_network', {}).get('nodes', []))}")
            
            print(f"\n📊 Evidence Factors:")
            for factor, score in reconstruction.get('evidence_factors', {}).items():
                print(f"   • {factor.replace('_', ' ').title()}: {score:.1%}")
            
            print(f"\n🌐 Translation Chains:")
            for chain in reconstruction.get('translation_chains', []):
                print(f"   • {chain['path']} (confidence: {chain['confidence']:.1%})")
            
            print(f"\n💾 Output saved to:")
            print(f"   - callimachina/discoveries/{target_work.replace(' ', '_')}/")
            
        else:
            print(f"❌ Reconstruction failed for {target_work}")
            
    except Exception as e:
        print(f"❌ Error during reconstruction: {e}")
        return 1
    
    print("\n" + "=" * 50)
    print("Example completed successfully!")
    return 0

if __name__ == "__main__":
    exit(main())