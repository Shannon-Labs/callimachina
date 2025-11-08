#!/usr/bin/env python3
"""
Test script to verify confidence enhancement features.
"""

import sys
sys.path.insert(0, 'callimachina/src')

from bayesian_reconstructor import BayesianReconstructor
import pandas as pd

def test_confidence_enhancement():
    """Test temporal decay and cross-cultural bonuses."""
    print("🎯 Testing Confidence Enhancement Features")
    print("=" * 60)
    
    reconstructor = BayesianReconstructor(random_seed=42)
    
    # Test 1: Basic confidence update (baseline)
    print("\n1️⃣ Basic Confidence Update:")
    prior = 0.5
    evidence = [
        {'type': 'fragment', 'confidence': 0.8},
        {'type': 'citation', 'confidence': 0.7, 'citing_author': 'Strabo'},
        {'type': 'citation', 'confidence': 0.6, 'citing_author': 'Plutarch'}
    ]
    
    result = reconstructor.update_confidence(prior, evidence)
    print(f"   Prior: {prior:.1%}")
    print(f"   Posterior: {result['mean']:.1%}")
    print(f"   Improvement: {result['mean'] - prior:.1%}")
    
    # Test 2: Temporal decay weighting
    print("\n2️⃣ Temporal Decay Weighting:")
    metadata = {
        'author': 'Aristotle',
        'century': -4,  # 4th century BCE
        'genre': 'philosophy'
    }
    
    # Strabo (1st century BCE) - only 3 centuries later = high weight
    # Plutarch (1st century CE) - 4 centuries later = medium weight
    evidence_with_temporal = [
        {'type': 'fragment', 'confidence': 0.8},
        {'type': 'citation', 'confidence': 0.7, 'citing_author': 'Strabo'},
        {'type': 'citation', 'confidence': 0.6, 'citing_author': 'Plutarch'}
    ]
    
    result_with_temporal = reconstructor.update_confidence(prior, evidence_with_temporal, metadata=metadata)
    print(f"   With temporal weighting: {result_with_temporal['mean']:.1%}")
    print(f"   vs without: {result['mean']:.1%}")
    print(f"   Temporal boost: {result_with_temporal['mean'] - result['mean']:.1%}")
    
    # Test 3: Cross-cultural bonuses
    print("\n3️⃣ Cross-Cultural Bonuses:")
    
    # Test Arabic translation bonus
    metadata_arabic = {
        'author': 'Galen',
        'century': 2,  # 2nd century CE
        'genre': 'medicine',
        'arabic_translation': True
    }
    
    result_arabic = reconstructor.update_confidence(prior, evidence, metadata=metadata_arabic)
    print(f"   With Arabic translation: {result_arabic['mean']:.1%}")
    print(f"   Arabic bonus: {result_arabic['mean'] - result['mean']:.1%}")
    
    # Test Latin translation bonus
    metadata_latin = {
        'author': 'Aristotle',
        'century': -4,
        'genre': 'philosophy',
        'latin_translation': True
    }
    
    result_latin = reconstructor.update_confidence(prior, evidence, metadata=metadata_latin)
    print(f"   With Latin translation: {result_latin['mean']:.1%}")
    print(f"   Latin bonus: {result_latin['mean'] - result['mean']:.1%}")
    
    # Test multiple translation paths (should get +20% instead of cumulative)
    metadata_multiple = {
        'author': 'Aristotle',
        'century': -4,
        'genre': 'philosophy',
        'arabic_translation': True,
        'latin_translation': True,
        'syriac_intermediary': True
    }
    
    result_multiple = reconstructor.update_confidence(prior, evidence, metadata=metadata_multiple)
    print(f"   With multiple translations: {result_multiple['mean']:.1%}")
    print(f"   Multiple paths bonus: {result_multiple['mean'] - result['mean']:.1%}")
    print(f"   (Should be ~+20%): {'✅' if abs((result_multiple['mean'] - result['mean']) - 0.20) < 0.05 else '❌'}")
    
    # Test 4: Combined effects
    print("\n4️⃣ Combined Effects:")
    metadata_combined = {
        'author': 'Aristotle',
        'century': -4,
        'genre': 'philosophy',
        'arabic_translation': True,
        'latin_translation': True
    }
    
    evidence_rich = [
        {'type': 'fragment', 'confidence': 0.9},
        {'type': 'citation', 'confidence': 0.8, 'citing_author': 'Strabo'},
        {'type': 'citation', 'confidence': 0.7, 'citing_author': 'Plutarch'},
        {'type': 'citation', 'confidence': 0.75, 'citing_author': 'Athenaeus'},
        {'type': 'translation', 'confidence': 0.8}
    ]
    
    result_combined = reconstructor.update_confidence(0.5, evidence_rich, metadata=metadata_combined)
    print(f"   Rich evidence + bonuses: {result_combined['mean']:.1%}")
    print(f"   Total improvement: {result_combined['mean'] - 0.5:.1%}")
    
    # Test 5: Verify confidence cap
    print("\n5️⃣ Confidence Cap:")
    metadata_max_bonus = {
        'author': 'Aristotle',
        'century': -4,
        'genre': 'philosophy',
        'arabic_translation': True,
        'latin_translation': True,
        'syriac_intermediary': True
    }
    
    # Start with high prior and strong evidence
    result_capped = reconstructor.update_confidence(0.9, evidence_rich, metadata=metadata_max_bonus)
    print(f"   High prior with max bonuses: {result_capped['mean']:.1%}")
    print(f"   Capped at 1.0: {'✅' if result_capped['mean'] <= 1.0 else '❌'}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"   Basic update: {result['mean']:.1%}")
    print(f"   With temporal weighting: {result_with_temporal['mean']:.1%}")
    print(f"   With Arabic translation: {result_arabic['mean']:.1%}")
    print(f"   With multiple translations: {result_multiple['mean']:.1%}")
    print(f"   Combined effects: {result_combined['mean']:.1%}")
    
    improvements = [
        result_with_temporal['mean'] - result['mean'],
        result_arabic['mean'] - result['mean'],
        result_multiple['mean'] - result['mean'],
        result_combined['mean'] - 0.5
    ]
    
    print(f"\n   Average improvement: {sum(improvements)/len(improvements):.1%}")
    print(f"   Max improvement: {max(improvements):.1%}")
    
    return True

if __name__ == '__main__':
    success = test_confidence_enhancement()
    sys.exit(0 if success else 1)
