"""
BayesianReconstructor: Simplified Bayesian confidence engine for text reconstruction.

This is a lightweight version that uses direct Bayesian formulas instead of PyMC/MCMC.
It maintains the same interface as the original but with faster computation.

Implements Bayesian updating of reconstruction confidence as new fragments appear.
Each reconstruction improves our priors, making subsequent discoveries faster.
"""

import numpy as np
import pandas as pd
import json
import logging
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import matplotlib.pyplot as plt
from collections import defaultdict


class BayesianReconstructor:
    def __init__(self, random_seed: int = 42):
        """
        Initialize the Bayesian reconstructor.
        
        Args:
            random_seed: Random seed for reproducibility
        """
        self.random_seed = random_seed
        np.random.seed(random_seed)
        self.logger = logging.getLogger(__name__)
        self.confidence_history = []
        
        # Default prior distributions based on historical data
        self.default_priors = {
            'fragment_authenticity': 0.7,  # 70% chance a fragment is authentic
            'citation_reliability': 0.8,   # 80% chance a citation is accurate
            'transmission_quality': 0.6,   # 60% chance of good transmission
            'author_consistency': 0.75,    # 75% chance of stylistic consistency
        }
    
    def update_confidence(self, prior: float, evidence: List[Dict], 
                         weights: Optional[List[float]] = None) -> Dict[str, float]:
        """
        Update reconstruction confidence using Bayesian inference.
        
        Args:
            prior: Prior confidence (0-1)
            evidence: List of evidence dictionaries
            weights: Optional weights for each evidence piece
            
        Returns:
            Dictionary with posterior statistics
        """
        if weights is None:
            weights = [1.0] * len(evidence)
        
        # Normalize weights
        weights = np.array(weights) / sum(weights)
        
        # Extract evidence values and calculate weighted average
        evidence_values = []
        reliability_scores = []
        
        for i, ev in enumerate(evidence):
            ev_type = ev.get('type', 'fragment')
            ev_value = ev.get('confidence', 0.5)
            ev_weight = weights[i]
            
            # Get reliability based on evidence type
            if ev_type == 'fragment':
                reliability = self.default_priors['fragment_authenticity']
            elif ev_type == 'citation':
                reliability = self.default_priors['citation_reliability']
            elif ev_type == 'translation':
                reliability = self.default_priors['transmission_quality']
            elif ev_type == 'stylistic':
                reliability = self.default_priors['author_consistency']
            else:
                reliability = 0.7  # Default reliability
            
            evidence_values.append(ev_value)
            reliability_scores.append(reliability * ev_weight)
        
        # Simple Bayesian update using Beta-Binomial conjugacy
        # This approximates the PyMC approach but much faster
        try:
            # Convert prior to Beta parameters (alpha, beta)
            # Using method of moments: mean = alpha/(alpha+beta), var = alpha*beta/((alpha+beta)^2*(alpha+beta+1))
            prior_alpha = prior * 10 + 1  # More concentrated prior
            prior_beta = (1 - prior) * 10 + 1
            
            # Update with evidence (treat each evidence piece as a "success")
            # Weighted sum of evidence values * reliabilities
            weighted_successes = sum(ev * rel for ev, rel in zip(evidence_values, reliability_scores))
            total_weight = sum(reliability_scores)
            
            # Posterior parameters
            posterior_alpha = prior_alpha + weighted_successes
            posterior_beta = prior_beta + total_weight - weighted_successes
            
            # Calculate posterior statistics
            posterior_mean = posterior_alpha / (posterior_alpha + posterior_beta)
            posterior_var = (posterior_alpha * posterior_beta) / (
                (posterior_alpha + posterior_beta) ** 2 * (posterior_alpha + posterior_beta + 1)
            )
            posterior_std = np.sqrt(posterior_var)
            
            # Calculate credible intervals (approximate 95% CI)
            ci_lower = max(0, posterior_mean - 1.96 * posterior_std)
            ci_upper = min(1, posterior_mean + 1.96 * posterior_std)
            
            posterior_stats = {
                'mean': float(posterior_mean),
                'std': float(posterior_std),
                'ci_lower': float(ci_lower),
                'ci_upper': float(ci_upper),
                'median': float(posterior_mean),  # Approximation for symmetric distributions
            }
            
            # Store in history
            self.confidence_history.append({
                'prior': prior,
                'posterior_mean': posterior_stats['mean'],
                'evidence_count': len(evidence),
                'timestamp': pd.Timestamp.now()
            })
            
            return posterior_stats
            
        except Exception as e:
            self.logger.error(f"Bayesian update failed: {e}")
            return {'mean': prior, 'std': 0.1, 'ci_lower': prior-0.1, 'ci_upper': min(prior+0.1, 1.0)}
    
    def reconstruct_work(self, work_id: str, fragments: List[Dict], 
                        citations: List[Dict], metadata: Dict) -> Dict[str, Any]:
        """
        Perform full Bayesian reconstruction of a lost work.
        
        Args:
            work_id: Unique identifier for the work
            fragments: List of fragment dictionaries
            citations: List of citation dictionaries
            metadata: Work metadata
            
        Returns:
            Reconstruction results dictionary
        """
        self.logger.info(f"Starting reconstruction of {work_id}")
        
        # Initial prior based on similar works
        initial_prior = self._get_initial_prior(metadata)
        
        # Process evidence
        evidence = []
        weights = []
        
        # Add fragment evidence
        for fragment in fragments:
            evidence.append({
                'type': 'fragment',
                'confidence': fragment.get('confidence', 0.5),
                'source': fragment.get('source', 'unknown'),
                'text_length': len(fragment.get('text', ''))
            })
            # Weight by text length and source reliability
            weight = min(len(fragment.get('text', '')) / 100, 2.0) * 0.8
            weights.append(weight)
        
        # Add citation evidence
        for citation in citations:
            evidence.append({
                'type': 'citation',
                'confidence': citation.get('confidence', 0.6),
                'citing_author': citation.get('citing_author', 'unknown'),
                'pattern': citation.get('pattern', 'unknown')
            })
            # Weight by citation pattern reliability
            pattern_weights = {
                'cf_book_line': 1.0,
                'as_says_in': 0.8,
                'according_to': 0.7
            }
            weight = pattern_weights.get(citation.get('pattern'), 0.6)
            weights.append(weight)
        
        # Update confidence
        posterior_stats = self.update_confidence(initial_prior, evidence, weights)
        
        # Generate reconstruction
        reconstruction = self._generate_reconstruction_text(fragments, metadata)
        
        # Calculate additional metrics
        metrics = self._calculate_reconstruction_metrics(fragments, citations, posterior_stats)
        
        results = {
            'work_id': work_id,
            'metadata': metadata,
            'prior_confidence': initial_prior,
            'posterior_confidence': posterior_stats,
            'fragments_used': len(fragments),
            'citations_used': len(citations),
            'reconstruction': reconstruction,
            'metrics': metrics,
            'evidence_summary': {
                'fragment_evidence': len([e for e in evidence if e['type'] == 'fragment']),
                'citation_evidence': len([e for e in evidence if e['type'] == 'citation']),
                'total_weight': sum(weights)
            }
        }
        
        self.logger.info(f"Reconstruction complete. Confidence: {posterior_stats['mean']:.1%}")
        
        return results
    
    def _get_initial_prior(self, metadata: Dict) -> float:
        """Get initial prior based on work metadata."""
        base_prior = 0.5  # Default neutral prior
        
        # Adjust based on genre
        genre_priors = {
            'philosophy': 0.6,
            'science': 0.65,
            'history': 0.55,
            'poetry': 0.5,
            'rhetoric': 0.45
        }
        
        genre = metadata.get('genre', 'unknown').lower()
        for genre_key, prior in genre_priors.items():
            if genre_key in genre:
                base_prior = prior
                break
        
        # Adjust based on century (earlier works are less likely to survive)
        century = metadata.get('century', 0)
        if century:
            if century < 0:  # BCE
                base_prior *= 0.8  # Earlier works have lower survival
            elif century > 5:  # CE
                base_prior *= 0.9  # Later works have better survival
        
        # Adjust based on author fame
        famous_authors = {'Aristotle', 'Plato', 'Galen', 'Homer', 'Virgil'}
        author = metadata.get('author', '')
        if any(famous in author for famous in famous_authors):
            base_prior *= 1.2
        
        return min(base_prior, 0.9)  # Cap at 0.9
    
    def _generate_reconstruction_text(self, fragments: List[Dict], metadata: Dict) -> Dict[str, str]:
        """Generate reconstructed text from fragments."""
        # Group fragments by suspected position
        positioned_fragments = self._position_fragments(fragments, metadata)
        
        reconstruction = {}
        
        for position, frags in positioned_fragments.items():
            if len(frags) == 1:
                # Single fragment at this position
                frag = frags[0]
                text = frag.get('text', '[LACUNA]')
                confidence = frag.get('confidence', 0.5)
                
                reconstruction[position] = f"{text} [confidence: {confidence:.1%}]"
            else:
                # Multiple fragments, need to reconcile
                texts = [f.get('text', '') for f in frags]
                confidences = [f.get('confidence', 0.5) for f in frags]
                
                # Simple reconciliation: take the most confident
                max_idx = np.argmax(confidences)
                best_text = texts[max_idx]
                avg_confidence = np.mean(confidences)
                
                reconstruction[position] = f"{best_text} [confidence: {avg_confidence:.1%}, {len(frags)} variants]"
        
        # Add lacuna markers where gaps exist
        positions = sorted(reconstruction.keys())
        for i in range(len(positions) - 1):
            if positions[i+1] - positions[i] > 1:
                reconstruction[positions[i] + 0.5] = "[LACUNA - missing text]"
        
        return reconstruction
    
    def _position_fragments(self, fragments: List[Dict], metadata: Dict) -> Dict[int, List[Dict]]:
        """Position fragments based on internal evidence."""
        positioned = defaultdict(list)
        
        for fragment in fragments:
            # Try to determine position from fragment metadata
            position = fragment.get('position', None)
            if position is not None:
                positioned[int(position)].append(fragment)
            else:
                # Use heuristic based on text content
                text = fragment.get('text', '')
                # Simple heuristic: length suggests position (earlier fragments tend to be longer)
                heuristic_pos = max(1, 10 - len(text) // 100)
                positioned[heuristic_pos].append(fragment)
        
        return positioned
    
    def _calculate_reconstruction_metrics(self, fragments: List[Dict], 
                                         citations: List[Dict], 
                                         posterior_stats: Dict) -> Dict[str, float]:
        """Calculate reconstruction quality metrics."""
        metrics = {}
        
        # Coverage metrics
        total_fragment_chars = sum(len(f.get('text', '')) for f in fragments)
        estimated_original_length = 5000  # Typical work length, could be parameterized
        metrics['text_coverage'] = min(total_fragment_chars / estimated_original_length, 1.0)
        
        # Citation density
        metrics['citation_density'] = len(citations) / max(len(fragments), 1)
        
        # Confidence stability
        metrics['confidence_stability'] = 1.0 - posterior_stats['std']
        
        # Fragment diversity (different sources)
        sources = set(f.get('source', 'unknown') for f in fragments)
        metrics['source_diversity'] = min(len(sources) / 3, 1.0)  # Normalize to 3+ sources
        
        # Overall quality score
        metrics['overall_quality'] = (
            posterior_stats['mean'] * 0.4 +
            metrics['text_coverage'] * 0.3 +
            metrics['source_diversity'] * 0.2 +
            metrics['confidence_stability'] * 0.1
        )
        
        return metrics
    
    def plot_confidence_evolution(self, work_id: str, save_path: Optional[str] = None):
        """
        Plot the evolution of confidence over time.
        
        Args:
            work_id: Work identifier
            save_path: Optional path to save the plot
        """
        if not self.confidence_history:
            self.logger.warning("No confidence history to plot")
            return
        
        df = pd.DataFrame(self.confidence_history)
        
        plt.figure(figsize=(10, 6))
        
        # Plot prior vs posterior
        plt.plot(df.index, df['prior'], 'b--', label='Prior Confidence', alpha=0.7)
        plt.plot(df.index, df['posterior_mean'], 'r-', label='Posterior Confidence', linewidth=2)
        
        # Add confidence intervals
        ci_lower = [max(0, mean - 0.1) for mean in df['posterior_mean']]
        ci_upper = [min(1, mean + 0.1) for mean in df['posterior_mean']]
        plt.fill_between(df.index, ci_lower, ci_upper, alpha=0.2, color='red')
        
        # Add evidence count as scatter plot
        scatter = plt.scatter(df.index, df['posterior_mean'], 
                            s=df['evidence_count']*50, 
                            c=df['evidence_count'], 
                            cmap='viridis', 
                            alpha=0.6,
                            label='Evidence Count')
        
        plt.colorbar(scatter, label='Number of Evidence Pieces')
        
        plt.xlabel('Update Iteration')
        plt.ylabel('Confidence')
        plt.title(f'Confidence Evolution for {work_id}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 1)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Saved confidence plot to {save_path}")
        
        plt.show()
    
    def save_reconstruction(self, results: Dict, output_dir: str):
        """
        Save reconstruction results to disk.
        
        Args:
            results: Reconstruction results dictionary
            output_dir: Output directory path
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        work_id = results['work_id']
        
        # Save main results as JSON
        with open(output_path / f"{work_id}_reconstruction.json", 'w') as f:
            # Convert numpy types to native Python types for JSON serialization
            json_results = self._convert_numpy_types(results)
            json.dump(json_results, f, indent=2, default=str)
        
        # Save reconstruction text
        with open(output_path / f"{work_id}_text.md", 'w') as f:
            f.write(f"# Reconstructed Text: {work_id}\n\n")
            f.write(f"**Confidence**: {results['posterior_confidence']['mean']:.1%}\n\n")
            
            for position, text in sorted(results['reconstruction'].items()):
                f.write(f"### Position {position}\n")
                f.write(f"{text}\n\n")
        
        # Save metrics
        metrics_df = pd.DataFrame([results['metrics']])
        metrics_df.to_csv(output_path / f"{work_id}_metrics.csv", index=False)
        
        # Save confidence history
        if self.confidence_history:
            history_df = pd.DataFrame(self.confidence_history)
            history_df.to_csv(output_path / f"{work_id}_confidence_history.csv", index=False)
        
        self.logger.info(f"Saved reconstruction for {work_id} to {output_dir}")
    
    def _convert_numpy_types(self, obj):
        """Convert numpy types to native Python types for JSON serialization."""
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: self._convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_numpy_types(item) for item in obj]
        else:
            return obj
    
    def compare_reconstructions(self, reconstructions: List[Dict]) -> pd.DataFrame:
        """
        Compare multiple reconstructions.
        
        Args:
            reconstructions: List of reconstruction result dictionaries
            
        Returns:
            Comparison DataFrame
        """
        comparison_data = []
        
        for rec in reconstructions:
            comparison_data.append({
                'work_id': rec['work_id'],
                'prior_confidence': rec['prior_confidence'],
                'posterior_mean': rec['posterior_confidence']['mean'],
                'posterior_std': rec['posterior_confidence']['std'],
                'fragments_used': rec['fragments_used'],
                'citations_used': rec['citations_used'],
                'text_coverage': rec['metrics']['text_coverage'],
                'overall_quality': rec['metrics']['overall_quality'],
                'source_diversity': rec['metrics']['source_diversity']
            })
        
        df = pd.DataFrame(comparison_data)
        
        # Add ranking columns
        df['confidence_rank'] = df['posterior_mean'].rank(ascending=False)
        df['quality_rank'] = df['overall_quality'].rank(ascending=False)
        df['composite_rank'] = (df['confidence_rank'] + df['quality_rank']) / 2
        
        return df.sort_values('composite_rank')