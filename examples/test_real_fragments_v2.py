#!/usr/bin/env python3
"""
Test script to verify real papyri.info API integration and collect 10 real fragments.
This version tries direct document access instead of search.
"""

import sys
sys.path.insert(0, 'callimachina/src')

from fragment_scraper import FragmentScraper
from database import db
import time

def test_real_fragments():
    """Test real API integration and collect fragments via direct document access."""
    print("🏛️ Testing Real Papyri.info Integration (Direct Access)")
    print("=" * 60)
    
    # Initialize scraper with 1 second rate limiting
    scraper = FragmentScraper(rate_limit=1.0, timeout=30)
    
    # Try a variety of document IDs that are likely to exist
    # Based on common papyrological collections
    test_ids = [
        # PSI (Papiri della Società Italiana)
        'psi;5;446', 'psi;5;447', 'psi;5;448', 'psi;5;449', 'psi;5;450',
        
        # P.Mich. (Michigan Papyri)
        'p.mich;1;1', 'p.mich;1;2', 'p.mich;1;3', 'p.mich;1;4', 'p.mich;1;5',
        
        # P.Oxy. (Oxyrhynchus Papyri) - try some later volumes that might exist
        'p.oxy;12;1501', 'p.oxy;12;1502', 'p.oxy;12;1503',
        
        # P.Lond. (London Papyri)
        'p.lond;2;141', 'p.lond;2;142', 'p.lond;2;143',
        
        # P.Ryl. (Rylands Papyri)
        'p.ryl;2;75', 'p.ryl;2;76', 'p.ryl;2;77',
        
        # P.Flor. (Florence Papyri)
        'p.flor;1;1', 'p.flor;1;2', 'p.flor;1;3',
        
        # P.Tebt. (Tebtunis Papyri)
        'p.tebt;2;275', 'p.tebt;2;276', 'p.tebt;2;277',
    ]
    
    fragments = []
    successful_ids = []
    
    print("📄 Attempting to retrieve documents...")
    for i, doc_id in enumerate(test_ids):
        if len(fragments) >= 10:
            break
            
        try:
            print(f"\n[{i+1}/{len(test_ids)}] Testing: {doc_id}")
            text = scraper.get_fragment_text(doc_id)
            
            if text and len(text) > 100:  # Only count substantial fragments
                print(f"   ✓ SUCCESS! Retrieved {len(text)} characters")
                
                # Create fragment record
                fragment = {
                    'id': doc_id,
                    'text': text,
                    'source': 'papyri.info',
                    'metadata': {
                        'collection': doc_id.split(';')[0],
                        'document_id': doc_id,
                        'access_date': time.strftime('%Y-%m-%d')
                    },
                    'url': f"https://papyri.info/ddbdp/{doc_id}",
                    'confidence': 0.8,  # High confidence for direct document access
                    'source_author': f"Papyri.info/{doc_id.split(';')[0]}",
                    'position': 1,
                    'work_id': doc_id
                }
                
                fragments.append(fragment)
                successful_ids.append(doc_id)
                
                preview = text.replace('\n', ' ')[:80]
                print(f"   Preview: {preview}...")
                
            else:
                print(f"   ✗ No substantial text retrieved")
                
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        # Respect rate limiting
        time.sleep(1.0)
    
    print("\n" + "=" * 60)
    print(f"📊 Results:")
    print(f"   Documents tried: {len(test_ids)}")
    print(f"   Successful retrievals: {len(fragments)}")
    print(f"   Success rate: {len(fragments)/len(test_ids)*100:.1f}%")
    
    if len(fragments) >= 5:
        print("\n✅ SUCCESS: Retrieved 5+ real fragments from papyri.info!")
        print("\n📋 Successful document IDs:")
        for doc_id in successful_ids:
            print(f"   - {doc_id}")
        
        # Store in database
        print("\n💾 Storing fragments in database...")
        stored = 0
        for fragment in fragments:
            try:
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
        print(f"\n⚠️  Only found {len(fragments)} fragments (need 5 for success)")
        return False

if __name__ == '__main__':
    success = test_real_fragments()
    sys.exit(0 if success else 1)
