"""
CALLIMACHINA CLI: Command-line interface for autonomous digital archaeology.

Usage:
    python -m src.cli reconstruct --work "Apollodorus.Chronicle"
    python -m src.cli network --mode excavation --output discoveries/priority_queue.csv
    python -m src.cli stylometry --author "TestAuthor" --texts path/to/texts/
"""

import click
import sys
import os
from pathlib import Path
from typing import Optional
import pandas as pd

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from fragment_scraper import FragmentScraper
from citation_network import CitationNetwork
from bayesian_reconstructor import BayesianReconstructor
from stylometric_engine import StylometricEngine
from cross_lingual import CrossLingualMapper


@click.group()
@click.version_option(version="3.0.0")
def callimachina():
    """Autonomous digital archaeology for classical texts."""
    pass


@callimachina.command()
@click.option('--work', required=True, help='Target work (e.g., Apollodorus.Chronicle)')
@click.option('--output-dir', default='discoveries/', help='Output directory for reconstruction')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
@click.option('--random-seed', default=42, help='Random seed for reproducibility')
def reconstruct(work: str, output_dir: str, verbose: bool, random_seed: int):
    """Reconstruct a lost work with confidence intervals."""
    if verbose:
        click.echo(f"🚀 Starting reconstruction of {work}")
    
    # Initialize components
    scraper = FragmentScraper(rate_limit=0.1, timeout=10)
    network = CitationNetwork()
    reconstructor = BayesianReconstructor(random_seed=random_seed)
    
    # Create output directory
    work_safe = work.replace('.', '_').replace(' ', '_')
    output_path = Path(output_dir) / f"{work_safe}_{pd.Timestamp.now().strftime('%Y-%m-%d')}"
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Mock fragments for now (in production, this would scrape real data)
    fragments = [
        {
            'id': f'{work}_fragment_1',
            'text': f'Fragment of {work} mentioning key concepts.',
            'source': 'papyri.info',
            'source_author': 'Unknown',
            'confidence': 0.8,
            'position': 1
        },
        {
            'id': f'{work}_fragment_2',
            'text': f'Another fragment of {work} with citations.',
            'source': 'oxyrhynchus',
            'source_author': 'Unknown2',
            'confidence': 0.75,
            'position': 2
        }
    ]
    
    # Extract citations
    for fragment in fragments:
        citations = scraper.extract_citation_patterns(fragment['text'])
        fragment['citations'] = citations
    
    if verbose:
        click.echo(f"📜 Found {len(fragments)} fragments")
    
    # Build metadata
    metadata = {
        "author": work.split('.')[0],
        "title": work.split('.')[1] if '.' in work else work,
        "genre": "unknown",
        "century": -1
    }
    
    # Reconstruct
    try:
        results = reconstructor.reconstruct_work(
            work_id=work,
            fragments=fragments,
            citations=[c for f in fragments for c in f.get('citations', [])],
            metadata=metadata
        )
        
        # Save results
        reconstructor.save_reconstruction(results, str(output_path))
        
        confidence = results['posterior_confidence']['mean']
        click.echo(f"✅ Reconstruction complete: {confidence:.1%} confidence")
        click.echo(f"📁 Results saved to {output_path}")
        
        if verbose:
            click.echo(f"\n📊 Metrics:")
            for key, value in results['metrics'].items():
                click.echo(f"   {key}: {value:.3f}")
        
    except Exception as e:
        click.echo(f"❌ Reconstruction failed: {e}", err=True)
        sys.exit(1)


@callimachina.command()
@click.option('--mode', default='excavation', help='Analysis mode (excavation, network, or full)')
@click.option('--output', default='discoveries/priority_queue.csv', help='Output file for priority queue')
@click.option('--min-citations', default=1, help='Minimum citations for gap detection')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def network(mode: str, output: str, min_citations: int, verbose: bool):
    """Build citation network and identify gaps."""
    if verbose:
        click.echo(f"🕸️ Building citation network in {mode} mode")
    
    network = CitationNetwork()
    
    # Mock data for demonstration
    sample_fragments = [
        {
            'id': 'sample_1',
            'text': 'As Aristotle says in his Physics...',
            'source': 'papyri.info',
            'source_author': 'Author1',
            'confidence': 0.8,
            'citations': [
                {
                    'cited_author': 'Aristotle',
                    'cited_work': 'Physics',
                    'pattern': 'as_says_in',
                    'confidence': 0.85
                }
            ]
        }
    ]
    
    try:
        # Build network
        G = network.build_network(sample_fragments)
        
        if verbose:
            click.echo(f"📊 Network built with {len(G.nodes())} nodes and {len(G.edges())} edges")
        
        # Identify gaps
        gaps = network.identify_citation_gaps(min_citations=min_citations)
        
        if verbose:
            click.echo(f"🔍 Found {len(gaps)} citation gaps")
        
        # Identify load-bearing nodes
        critical_nodes = network.identify_load_bearing_nodes()
        
        if verbose:
            click.echo(f"⚠️  Found {len(critical_nodes)} critical nodes")
        
        # Map translation chains
        chains = network.map_translation_chains()
        
        if verbose:
            click.echo(f"🌐 Mapped {len(chains)} translation chains")
        
        # Calculate priority queue
        priority_df = network.calculate_priority_queue(gaps, critical_nodes)
        
        # Save priority queue
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        priority_df.to_csv(output_path, index=False)
        
        click.echo(f"✅ Priority queue saved to {output}")
        
        # Display top priorities
        if verbose and not priority_df.empty:
            click.echo(f"\n🏆 Top 5 priorities:")
            for idx, row in priority_df.head().iterrows():
                click.echo(f"   {row.get('work', 'Unknown')}: {row.get('priority_score', 0):.2f}")
        
    except Exception as e:
        click.echo(f"❌ Network analysis failed: {e}", err=True)
        sys.exit(1)


@callimachina.command()
@click.option('--author', required=True, help='Author name')
@click.option('--texts', required=True, help='Path to text files (directory or single file)')
@click.option('--language', default='greek', help='Language code (greek, latin, arabic)')
@click.option('--output', help='Output file for author profile')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def stylometry(author: str, texts: str, language: str, output: Optional[str], verbose: bool):
    """Fingerprint authorial style."""
    if verbose:
        click.echo(f"🎨 Creating stylometric profile for {author}")
    
    engine = StylometricEngine(language=language)
    
    # Load texts
    text_path = Path(texts)
    texts_list = []
    
    if text_path.is_dir():
        for text_file in text_path.glob('*.txt'):
            with open(text_file, 'r', encoding='utf-8') as f:
                texts_list.append(f.read())
    elif text_path.is_file():
        with open(text_path, 'r', encoding='utf-8') as f:
            texts_list.append(f.read())
    else:
        click.echo(f"❌ Text path not found: {texts}", err=True)
        sys.exit(1)
    
    if not texts_list:
        click.echo("❌ No texts found", err=True)
        sys.exit(1)
    
    if verbose:
        click.echo(f"📚 Loaded {len(texts_list)} text(s)")
    
    try:
        # Create author profile
        profile = engine.create_author_profile(author, texts_list)
        
        reliability = profile['reliability_score']
        click.echo(f"✅ Author profile created: {reliability:.2f} reliability score")
        
        # Save profile if output specified
        if output:
            import json
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                json.dump(profile, f, indent=2)
            
            click.echo(f"📁 Profile saved to {output}")
        
        # Show feature summary if verbose
        if verbose:
            features = engine.extract_features(texts_list[:5])  # Limit for display
            click.echo(f"\n📊 Extracted {len(features.columns)} features:")
            for col in list(features.columns)[:10]:  # Show first 10
                click.echo(f"   {col}")
            if len(features.columns) > 10:
                click.echo(f"   ... and {len(features.columns) - 10} more")
        
    except Exception as e:
        click.echo(f"❌ Stylometric analysis failed: {e}", err=True)
        sys.exit(1)


@callimachina.command()
@click.option('--work', required=True, help='Work to analyze (e.g., Aristotle.Metaphysics)')
@click.option('--output', help='Output file for translation chain')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def translate_chain(work: str, output: Optional[str], verbose: bool):
    """Map translation chain for a work."""
    if verbose:
        click.echo(f"🌐 Mapping translation chain for {work}")
    
    mapper = CrossLingualMapper(rate_limit=0.1, timeout=10)
    
    try:
        # Map translation chain
        chain = mapper.map_translation_chain(work)
        
        transmission_score = chain.get('transmission_score', 0)
        confidence = chain.get('confidence', 0)
        
        click.echo(f"✅ Translation chain mapped:")
        click.echo(f"   Greek: {chain.get('greek_original', 'N/A')}")
        click.echo(f"   Syriac: {chain.get('syriac_intermediary', 'N/A')}")
        click.echo(f"   Arabic: {chain.get('arabic_translation', 'N/A')}")
        click.echo(f"   Latin: {chain.get('latin_translation', 'N/A')}")
        click.echo(f"   Score: {transmission_score:.2f}, Confidence: {confidence:.2f}")
        
        # Save if output specified
        if output:
            import json
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                json.dump(chain, f, indent=2)
            
            click.echo(f"📁 Chain saved to {output}")
        
        # Show translation centers if verbose
        if verbose:
            centers = mapper.identify_translation_centers()
            click.echo(f"\n🏛️ Translation centers:")
            for center, info in centers.items():
                works = info.get('works_translated', [])
                click.echo(f"   {center}: {len(works)} works")
        
    except Exception as e:
        click.echo(f"❌ Translation chain mapping failed: {e}", err=True)
        sys.exit(1)


@callimachina.command()
@click.option('--target', help='Specific work to excavate')
@click.option('--output-dir', default='discoveries/', help='Output directory')
@click.option('--priority-file', default='discoveries/priority_queue.csv', help='Priority queue file')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def excavate(target: Optional[str], output_dir: str, priority_file: str, verbose: bool):
    """Run full excavation pipeline."""
    if verbose:
        click.echo("🏛️ Starting autonomous excavation pipeline")
    
    try:
        # Initialize all components
        scraper = FragmentScraper(rate_limit=0.1, timeout=10)
        network = CitationNetwork()
        reconstructor = BayesianReconstructor(random_seed=42)
        mapper = CrossLingualMapper(rate_limit=0.1, timeout=10)
        
        # Determine target works
        if target:
            works = [target]
        else:
            # Use priority queue if available
            priority_path = Path(priority_file)
            if priority_path.exists():
                df = pd.read_csv(priority_path)
                # Check for 'work' or 'target' column
                if 'work' in df.columns:
                    works = df['work'].head(3).tolist()  # Top 3 priorities
                elif 'target' in df.columns:
                    works = df['target'].head(3).tolist()
                else:
                    works = []
            else:
                # Default test works
                works = [
                    "Apollodorus.Chronicle",
                    "Euphorion.Hyacinthus", 
                    "Unknown.TragicPoet1"
                ]
        
        click.echo(f"🎯 Excavating {len(works)} work(s)")
        
        # Process each work
        for i, work in enumerate(works, 1):
            click.echo(f"\n[{i}/{len(works)}] Processing {work}...")
            
            # Reconstruct
            work_safe = work.replace('.', '_').replace(' ', '_')
            work_output = Path(output_dir) / f"{work_safe}_{pd.Timestamp.now().strftime('%Y-%m-%d')}"
            work_output.mkdir(parents=True, exist_ok=True)
            
            # Mock fragments
            fragments = [
                {
                    'id': f'{work}_fragment_1',
                    'text': f'Fragment of {work}...',
                    'source': 'papyri.info',
                    'source_author': 'Unknown',
                    'confidence': 0.8,
                    'position': 1
                }
            ]
            
            for fragment in fragments:
                citations = scraper.extract_citation_patterns(fragment['text'])
                fragment['citations'] = citations
            
            metadata = {
                "author": work.split('.')[0],
                "title": work.split('.')[1] if '.' in work else work,
                "genre": "unknown",
                "century": -1
            }
            
            results = reconstructor.reconstruct_work(
                work_id=work,
                fragments=fragments,
                citations=[c for f in fragments for c in f.get('citations', [])],
                metadata=metadata
            )
            
            reconstructor.save_reconstruction(results, str(work_output))
            
            confidence = results['posterior_confidence']['mean']
            click.echo(f"   ✅ {work}: {confidence:.1%} confidence")
            
            # Map translation chain
            try:
                chain = mapper.map_translation_chain(work)
                click.echo(f"   🌐 Translation chain: {chain.get('transmission_score', 0):.2f}")
            except:
                pass
        
        click.echo(f"\n🏛️ Excavation complete! Results in {output_dir}")
        
    except Exception as e:
        click.echo(f"❌ Excavation failed: {e}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    callimachina()