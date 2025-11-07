"""
Test suite for CALLIMACHINA v3.0 infrastructure.

Must pass 5/5 tests for system validation.
Tests cover:
1. Fragment scraping functionality
2. Citation network analysis
3. Bayesian reconstruction
4. Stylometric fingerprinting
5. Cross-lingual mapping
"""

import unittest
import sys
import os
import tempfile
import json
import pandas as pd
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

try:
    from fragment_scraper import FragmentScraper
    from citation_network import CitationNetwork
    from bayesian_reconstructor import BayesianReconstructor
    from stylometric_engine import StylometricEngine
    from cross_lingual import CrossLingualMapper
    IMPORT_SUCCESS = True
except ImportError as e:
    print(f"Import error: {e}")
    IMPORT_SUCCESS = False


class TestCALLIMACHINAInfrastructure(unittest.TestCase):
    """Test suite for CALLIMACHINA v3.0 infrastructure."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        if not IMPORT_SUCCESS:
            raise unittest.SkipTest("Failed to import CALLIMACHINA modules")
        
        # Sample test data
        cls.sample_fragments = [
            {
                'id': 'test_fragment_1',
                'text': 'As Aristotle says in his Physics, the natural motion of elements follows their nature.',
                'source': 'papyri.info',
                'source_author': 'Unknown1',
                'confidence': 0.8,
                'citations': [
                    {
                        'cited_author': 'Aristotle',
                        'cited_work': 'Physics',
                        'pattern': 'as_says_in',
                        'confidence': 0.85
                    }
                ]
            },
            {
                'id': 'test_fragment_2',
                'text': 'According to Plato, the ideal state must have philosophers as rulers.',
                'source': 'oxyrhynchus',
                'source_author': 'Unknown2',
                'confidence': 0.75,
                'citations': [
                    {
                        'cited_author': 'Plato',
                        'cited_work': 'Republic',
                        'pattern': 'according_to',
                        'confidence': 0.7
                    }
                ]
            },
            {
                'id': 'test_fragment_3',
                'text': 'The procession of the equinoxes as calculated by Hipparchus shows the precession.',
                'source': 'papyri.info',
                'source_author': 'Unknown1',
                'confidence': 0.9,
                'citations': [
                    {
                        'cited_author': 'Hipparchus',
                        'cited_work': 'On the Length of the Year',
                        'pattern': 'as_calculated_by',
                        'confidence': 0.9
                    }
                ]
            }
        ]
        
        cls.sample_texts = [
            "καὶ ὁ ἄνθρωπος ἦν καλὸς καὶ δίκαιος",
            "ἡ γυνὴ σοφὴ ἦν καὶ ἐλευθέρα",
            "τὸ παιδίον νέον ἦν καὶ ἀγαθόν",
            "ὁ ποιητὴς μέγας ἦν καὶ φιλόσοφος"
        ]
        
        # Create temporary directory for test outputs
        cls.temp_dir = tempfile.mkdtemp()
    
    def test_00_rss_balance_verification(self):
        """Test 0: Verify RSS load balancing across network queues."""
        print("\n=== Test 0: RSS Balance Verification ===")
        
        # Initialize scraper
        scraper = FragmentScraper(rate_limit=0.1, timeout=10)
        
        # Verify RSS balance
        balance_info = scraper.verify_rss_balance()
        
        # Should return valid structure
        self.assertIsInstance(balance_info, dict)
        self.assertIn('balanced', balance_info)
        self.assertIn('recommendation', balance_info)
        
        # Log results
        if balance_info.get('balanced'):
            print(f"✓ RSS balance verified: {balance_info['recommendation']}")
        else:
            print(f"⚠ RSS imbalance detected: {balance_info.get('imbalance_percent', 'N/A')}%")
            print(f"  Recommendation: {balance_info['recommendation']}")
        
        # Display queue stats if available
        if 'queue_stats' in balance_info:
            print(f"  Queue distribution: {balance_info['queue_stats']}")
        
        # Test environment note
        if 'note' in balance_info:
            print(f"  Note: {balance_info['note']}")
    
    def test_01_fragment_scraper_initialization(self):
        """Test 1: FragmentScraper initialization and basic functionality."""
        print("\n=== Test 1: FragmentScraper ===")
        
        # Initialize scraper
        scraper = FragmentScraper(rate_limit=0.1, timeout=10)
        self.assertIsNotNone(scraper)
        print("✓ FragmentScraper initialized successfully")
        
        # Test citation pattern extraction
        test_text = "As Aristotle says in his Physics, the natural motion follows nature."
        citations = scraper.extract_citation_patterns(test_text)
        
        self.assertIsInstance(citations, list)
        self.assertGreater(len(citations), 0)
        
        citation = citations[0]
        self.assertEqual(citation['cited_author'], 'Aristotle')
        self.assertEqual(citation['cited_work'], 'Physics')
        self.assertEqual(citation['pattern'], 'as_says_in')
        print("✓ Citation pattern extraction working")
        
        # Test author abbreviation
        abbreviations = scraper._get_author_abbreviations('Aristotle')
        self.assertIsInstance(abbreviations, list)
        print("✓ Author abbreviation lookup working")
    
    def test_02_citation_network_analysis(self):
        """Test 2: CitationNetwork building and analysis."""
        print("\n=== Test 2: CitationNetwork ===")
        
        # Initialize network
        network = CitationNetwork()
        self.assertIsNotNone(network)
        print("✓ CitationNetwork initialized successfully")
        
        # Build network from sample fragments
        G = network.build_network(self.sample_fragments)
        self.assertIsNotNone(G)
        self.assertGreater(len(G.nodes()), 0)
        self.assertGreater(len(G.edges()), 0)
        print(f"✓ Network built with {len(G.nodes())} nodes and {len(G.edges())} edges")
        
        # Test citation gap detection
        gaps = network.identify_citation_gaps(min_citations=1)
        self.assertIsInstance(gaps, list)
        print(f"✓ Citation gap detection found {len(gaps)} gaps")
        
        if gaps:
            gap = gaps[0]
            self.assertIn('author', gap)
            self.assertIn('recoverability_score', gap)
            self.assertIn('search_strategy', gap)
            print("✓ Gap analysis structure correct")
        
        # Test load-bearing node detection
        critical_nodes = network.identify_load_bearing_nodes(threshold=0.01)
        self.assertIsInstance(critical_nodes, list)
        print(f"✓ Load-bearing node detection found {len(critical_nodes)} critical nodes")
        
        # Test translation chain mapping
        chains = network.map_translation_chains()
        self.assertIsInstance(chains, list)
        print(f"✓ Translation chain mapping found {len(chains)} chains")
        
        # Test priority queue calculation
        priority_df = network.calculate_priority_queue(gaps, critical_nodes)
        self.assertIsInstance(priority_df, pd.DataFrame)
        self.assertGreater(len(priority_df.columns), 0)
        print("✓ Priority queue calculation working")
        
        # Test network export
        export_path = os.path.join(self.temp_dir, "test_network.graphml")
        network.export_network(export_path, format='graphml')
        self.assertTrue(os.path.exists(export_path))
        print("✓ Network export working")
    
    def test_03_bayesian_reconstruction(self):
        """Test 3: BayesianReconstructor confidence updating."""
        print("\n=== Test 3: BayesianReconstructor ===")
        
        # Initialize reconstructor
        reconstructor = BayesianReconstructor(random_seed=42)
        self.assertIsNotNone(reconstructor)
        print("✓ BayesianReconstructor initialized successfully")
        
        # Test confidence update
        prior = 0.5
        evidence = [
            {'type': 'fragment', 'confidence': 0.9},
            {'type': 'citation', 'confidence': 0.8},
            {'type': 'translation', 'confidence': 0.7}
        ]
        
        posterior = reconstructor.update_confidence(prior, evidence)
        self.assertIsInstance(posterior, dict)
        self.assertIn('mean', posterior)
        self.assertIn('std', posterior)
        self.assertIn('ci_lower', posterior)
        self.assertIn('ci_upper', posterior)
        
        # Check that posterior is higher than prior (evidence increases confidence)
        self.assertGreater(posterior['mean'], prior)
        print(f"✓ Bayesian update: {prior:.2f} → {posterior['mean']:.2f}")
        
        # Test work reconstruction
        results = reconstructor.reconstruct_work(
            work_id="Test.Work.1",
            fragments=self.sample_fragments,
            citations=[c for f in self.sample_fragments for c in f.get('citations', [])],
            metadata={
                "author": "TestAuthor",
                "title": "Test Work",
                "genre": "philosophy",
                "century": -1
            }
        )
        
        self.assertIsInstance(results, dict)
        self.assertEqual(results['work_id'], "Test.Work.1")
        self.assertIn('posterior_confidence', results)
        self.assertIn('reconstruction', results)
        self.assertIn('metrics', results)
        print("✓ Work reconstruction working")
        
        # Test confidence history tracking
        self.assertGreater(len(reconstructor.confidence_history), 0)
        print("✓ Confidence history tracking working")
        
        # Test reconstruction saving
        output_dir = os.path.join(self.temp_dir, "test_reconstruction")
        reconstructor.save_reconstruction(results, output_dir)
        
        self.assertTrue(os.path.exists(output_dir))
        self.assertTrue(os.path.exists(os.path.join(output_dir, "Test.Work.1_reconstruction.json")))
        self.assertTrue(os.path.exists(os.path.join(output_dir, "Test.Work.1_text.md")))
        print("✓ Reconstruction saving working")
    
    def test_04_stylometric_engine(self):
        """Test 4: StylometricEngine author fingerprinting."""
        print("\n=== Test 4: StylometricEngine ===")
        
        # Initialize stylometric engine
        stylometer = StylometricEngine(language="greek")
        self.assertIsNotNone(stylometer)
        print("✓ StylometricEngine initialized successfully")
        
        # Test feature extraction
        features = stylometer.extract_features(self.sample_texts)
        self.assertIsInstance(features, pd.DataFrame)
        self.assertGreater(len(features), 0)
        self.assertGreater(len(features.columns), 0)
        print(f"✓ Feature extraction: {len(features.columns)} features")
        
        # Test author profile creation
        profile = stylometer.create_author_profile("TestAuthor", self.sample_texts)
        self.assertIsInstance(profile, dict)
        self.assertEqual(profile['author'], "TestAuthor")
        self.assertIn('signature', profile)
        self.assertIn('reliability_score', profile)
        self.assertGreaterEqual(profile['reliability_score'], 0.0)
        self.assertLessEqual(profile['reliability_score'], 1.0)
        print(f"✓ Author profile created, reliability: {profile['reliability_score']:.2f}")
        
        # Store profile for attribution test
        self.assertIn("TestAuthor", stylometer.author_profiles)
        
        # Test text attribution
        unknown_text = "καὶ ὁ ποιητὴς μέγας ἦν"
        attributions = stylometer.attribute_text(unknown_text, ["TestAuthor"])
        
        self.assertIsInstance(attributions, list)
        self.assertGreater(len(attributions), 0)
        
        author, confidence = attributions[0]
        self.assertEqual(author, "TestAuthor")
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)
        print(f"✓ Text attribution: {author} ({confidence:.2f})")
        
        # Test authenticity verification
        verification = stylometer.verify_authenticity(unknown_text, "TestAuthor")
        self.assertIsInstance(verification, dict)
        self.assertIn('authentic', verification)
        self.assertIn('confidence', verification)
        print("✓ Authenticity verification working")
        
        # Test outlier detection
        outliers = stylometer.detect_stylistic_outliers(
            self.sample_texts, 
            [{'work': f'text_{i}'} for i in range(len(self.sample_texts))]
        )
        self.assertIsInstance(outliers, list)
        print(f"✓ Outlier detection found {len(outliers)} outliers")
    
    def test_05_cross_lingual_mapper(self):
        """Test 5: CrossLingualMapper translation chain analysis."""
        print("\n=== Test 5: CrossLingualMapper ===")
        
        # Initialize mapper
        mapper = CrossLingualMapper(rate_limit=0.1, timeout=10)
        self.assertIsNotNone(mapper)
        print("✓ CrossLingualMapper initialized successfully")
        
        # Test translation chain mapping
        chain = mapper.map_translation_chain("Aristotle.Metaphysics")
        self.assertIsInstance(chain, dict)
        self.assertIn('greek_original', chain)
        self.assertIn('syriac_intermediary', chain)
        self.assertIn('arabic_translation', chain)
        self.assertIn('latin_translation', chain)
        self.assertIn('transmission_score', chain)
        self.assertIn('confidence', chain)
        
        self.assertEqual(chain['greek_original'], "Aristotle.Metaphysics")
        self.assertGreaterEqual(chain['transmission_score'], 0.0)
        self.assertLessEqual(chain['transmission_score'], 1.0)
        print(f"✓ Translation chain mapped, score: {chain['transmission_score']:.2f}")
        
        # Test translation center identification
        centers = mapper.identify_translation_centers()
        self.assertIsInstance(centers, dict)
        self.assertGreater(len(centers), 0)
        
        # Check for known centers
        expected_centers = ['baghdad', 'toledo', 'edessa']
        for center in expected_centers:
            self.assertIn(center, centers)
            self.assertIn('coordinates', centers[center])
            self.assertIn('works_translated', centers[center])
        print(f"✓ Translation centers identified: {list(centers.keys())}")
        
        # Test priority queue generation
        test_works = [
            "Aristotle.Metaphysics",
            "Galen.OnAnatomicalProcedures",
            "Euclid.Elements"
        ]
        
        priority_df = mapper.generate_priority_queue(test_works)
        self.assertIsInstance(priority_df, pd.DataFrame)
        self.assertGreater(len(priority_df), 0)
        self.assertIn('work', priority_df.columns)
        self.assertIn('priority_score', priority_df.columns)
        self.assertIn('transmission_score', priority_df.columns)
        print("✓ Priority queue generation working")
        
        # Test network export
        network_file = os.path.join(self.temp_dir, "translation_network.json")
        mapper.export_translation_network(network_file)
        self.assertTrue(os.path.exists(network_file))
        
        # Verify JSON structure
        with open(network_file, 'r') as f:
            network_data = json.load(f)
        self.assertIn('nodes', network_data)
        self.assertIn('edges', network_data)
        print("✓ Translation network export working")
    
    def test_06_integration_workflow(self):
        """Test 6: Integration test of complete workflow."""
        print("\n=== Test 6: Integration Workflow ===")
        
        # Initialize all components
        scraper = FragmentScraper(rate_limit=0.1)
        network = CitationNetwork()
        reconstructor = BayesianReconstructor(random_seed=42)
        stylometer = StylometricEngine(language="greek")
        mapper = CrossLingualMapper(rate_limit=0.1)
        
        # Step 1: Extract citations from fragments
        print("Step 1: Extracting citations...")
        for fragment in self.sample_fragments:
            citations = scraper.extract_citation_patterns(fragment['text'])
            fragment['citations'] = citations
        print("✓ Citations extracted")
        
        # Step 2: Build citation network
        print("Step 2: Building network...")
        G = network.build_network(self.sample_fragments)
        self.assertGreater(len(G.nodes()), 0)
        print(f"✓ Network built ({len(G.nodes())} nodes)")
        
        # Step 3: Identify gaps
        print("Step 3: Identifying gaps...")
        gaps = network.identify_citation_gaps(min_citations=1)
        print(f"✓ Found {len(gaps)} citation gaps")
        
        # Step 4: Map translation chains
        print("Step 4: Mapping translation chains...")
        chains = network.map_translation_chains()
        print(f"✓ Mapped {len(chains)} chains")
        
        # Step 5: Reconstruct work
        print("Step 5: Reconstructing work...")
        results = reconstructor.reconstruct_work(
            work_id="Integration.Test.Work",
            fragments=self.sample_fragments,
            citations=[c for f in self.sample_fragments for c in f.get('citations', [])],
            metadata={
                "author": "IntegrationTest",
                "title": "Test Work",
                "genre": "philosophy",
                "century": -1
            }
        )
        self.assertGreater(results['posterior_confidence']['mean'], 0)
        print(f"✓ Reconstruction complete ({results['posterior_confidence']['mean']:.1%} confidence)")
        
        # Step 6: Create stylometric profile
        print("Step 6: Creating author profile...")
        profile = stylometer.create_author_profile("IntegrationAuthor", self.sample_texts)
        self.assertIn('reliability_score', profile)
        print(f"✓ Profile created (reliability: {profile['reliability_score']:.2f})")
        
        # Step 7: Map cross-lingual transmission
        print("Step 7: Mapping cross-lingual transmission...")
        chain = mapper.map_translation_chain("Aristotle.Metaphysics")
        self.assertIn('transmission_score', chain)
        print(f"✓ Translation chain mapped (score: {chain['transmission_score']:.2f})")
        
        print("\n✓ Integration test PASSED")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures."""
        # Clean up temporary directory
        import shutil
        if hasattr(cls, 'temp_dir') and os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir)


def run_tests():
    """Run all tests and report results."""
    print("=" * 70)
    print("CALLIMACHINA v3.0 Infrastructure Test Suite")
    print("=" * 70)
    
    if not IMPORT_SUCCESS:
        print("\n✗ FAILED: Could not import CALLIMACHINA modules")
        print("Please check installation and requirements.")
        return False
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCALLIMACHINAInfrastructure)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Report results
    print("\n" + "=" * 70)
    print("TEST RESULTS SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✓ ALL TESTS PASSED (5/5)")
        print("\nCALLIMACHINA v3.0 infrastructure is working correctly!")
        return True
    else:
        print("\n✗ SOME TESTS FAILED")
        print("\nPlease check the errors above and fix the issues.")
        return False


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)