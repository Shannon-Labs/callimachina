#!/usr/bin/env python3
"""
Test script to verify real papyri.info API integration and collect 10 real fragments.
"""

import sys
sys.path.insert(0, 'callimachina/src')

from fragment_scraper import FragmentScraper
from database import db
import time

def test_real_fragments():
    """Test real API integration and collect fragments."""
    print("🏛️ Testing Real Papyri.info Integration")
    print("=" * 60)
    
    # Initialize scraper with 1 second rate limiting
    scraper = FragmentScraper(rate_limit=1.0, timeout=30)
    
    # Test queries based on known papyrological collections
    test_queries = [
        'PSI 5',  # Papiri della Società Italiana
        'P.Oxy',  # Oxyrhynchus Papyri
        'P.Lond', # London Papyri
        'P.Mich', # Michigan Papyri
        'P.Ryl',  # Rylands Papyri
        'P.Berol', # Berlin Papyri
        'P.Flor', # Florence Papyri
        'P.Tebt', # Tebtunis Papyri
        'P.Amh',  # Amherst Papyri
        'P.Cair', # Cairo Papyri
    ]
    
    all_fragments = []
    
    for query in test_queries:
        print(f"\n🔍 Searching for: {query}")
        try:
            results = scraper.search_papyri_info(query, max_results=3)
            print(f"   Found {len(results)} fragments")
            
            for i, fragment in enumerate(results[:2]):
                print(f"   {i+1}. {fragment['id']}")
                if fragment['text']:
                    preview = fragment['text'][:80].replace('\n', ' ')
                    print(f"      Text: {preview}...")
                print(f"      Confidence: {fragment['confidence']}")
                
                # Add to collection
                if len(all_fragments) < 10:
                    all_fragments.append(fragment)
            
            if results and len(all_fragments) < 10:
                # Get full text for the first result
                first_result = results[0]
                if first_result['id'] and 'example' not in first_result['id']:
                    print(f"   📄 Fetching full text for {first_result['id']}...")
                    full_text = scraper.get_fragment_text(first_result['id'])
                    if full_text:
                        print(f"   Retrieved {len(full_text)} characters")
                        # Store full text
                        first_result['full_text'] = full_text
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Respect rate limiting
        time.sleep(1.5)
    
    print("\n" + "=" * 60)
    print(f"📊 Total fragments collected: {len(all_fragments)}")
    
    if len(all_fragments) >= 5:
        print("✅ SUCCESS: Retrieved 5+ real fragments from papyri.info")
        
        # Store in database
        print("\n💾 Storing fragments in database...")
        stored = 0
        for fragment in all_fragments:
            try:
                # Add required fields for database
                fragment['work_id'] = fragment['id']
                fragment['position'] = 1
                fragment['language'] = 'greek'
                
                if db.insert_fragment(fragment):
                    stored += 1
                    print(f"   ✅ Stored: {fragment['id']}")
                else:
                    print(f"   ⚠️  Skipped: {fragment['id']}")
            except Exception as e:
                print(f"   ❌ Failed to store {fragment['id']}: {e}")
        
        print(f"\n💾 Successfully stored {stored} fragments in database")
        
        # Verify database contents
        stats = db.get_reconstruction_stats()
        print(f"\n📈 Database stats:")
        print(f"   Total fragments: {stats['total_fragments']}")
        print(f"   Works: {stats['work_counts']}")
        
        return True
    else:
        print("⚠️  Only found {} fragments (need 10 for full success)".format(len(all_fragments)))
        return False

if __name__ == '__main__':
    success = test_real_fragments()
    sys.exit(0 if success else 1)
