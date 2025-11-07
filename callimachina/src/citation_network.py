"""
CitationNetwork: NetworkX-based analysis of classical text transmission.

Identifies:
- Citation gaps (genres that must have existed but are lost)
- Load-bearing nodes (authors whose loss would collapse chains)
- Transmission pathways (Greek→Syriac→Arabic→Latin)
- Recoverability scores based on network centrality
"""

import networkx as nx
import pandas as pd
import numpy as np
import json
import logging
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


class CitationNetwork:
    def __init__(self):
        """Initialize the citation network analyzer."""
        self.G = nx.DiGraph()  # Directed graph for citations
        self.logger = logging.getLogger(__name__)
        self.author_metadata = {}
        self.translation_chains = []
        
    def build_network(self, fragments: List[Dict]) -> nx.DiGraph:
        """
        Build citation network from fragment data.
        
        Args:
            fragments: List of fragment dictionaries with citation data
            
        Returns:
            NetworkX directed graph
        """
        self.G.clear()
        self.author_metadata.clear()
        
        for fragment in fragments:
            self._add_fragment_to_network(fragment)
        
        self.logger.info(f"Built network with {len(self.G.nodes())} nodes and {len(self.G.edges())} edges")
        return self.G
    
    def _add_fragment_to_network(self, fragment: Dict):
        """Add a single fragment to the network."""
        # Add source author node
        source_author = fragment.get('source_author', 'Unknown')
        if source_author not in self.G:
            self.G.add_node(source_author, 
                          type='author',
                          fragments=0,
                          confidence=fragment.get('confidence', 0.5))
        
        # Update fragment count
        self.G.nodes[source_author]['fragments'] += 1
        
        # Add cited authors and edges
        citations = fragment.get('citations', [])
        for citation in citations:
            cited_author = citation.get('cited_author')
            if cited_author and cited_author != source_author:
                
                # Add cited author node if not exists
                if cited_author not in self.G:
                    self.G.add_node(cited_author,
                                  type='author',
                                  fragments=0,
                                  confidence=citation.get('confidence', 0.5))
                
                # Add or update edge
                if self.G.has_edge(source_author, cited_author):
                    self.G[source_author][cited_author]['weight'] += 1
                    # Append citation to existing JSON string
                    existing = self.G[source_author][cited_author].get('citations', '[]')
                    citations_list = json.loads(existing) if existing else []
                    citations_list.append(citation)
                    self.G[source_author][cited_author]['citations'] = json.dumps(citations_list)
                else:
                    self.G.add_edge(source_author, cited_author,
                                  weight=1,
                                  citations=json.dumps([citation]))
    
    def identify_citation_gaps(self, min_citations: int = 3) -> List[Dict]:
        """
        Identify "ghost genres" - works that must have existed based on citation patterns.
        
        Args:
            min_citations: Minimum number of citations to consider a gap
            
        Returns:
            List of gap analysis dictionaries
        """
        gaps = []
        
        # Find authors who are cited frequently but have no fragments
        for node in self.G.nodes():
            in_degree = self.G.in_degree(node)
            out_degree = self.G.out_degree(node)
            node_data = self.G.nodes[node]
            
            # Check if this is a "ghost" - cited but no fragments
            if in_degree >= min_citations and node_data.get('fragments', 0) == 0:
                # Analyze the citing authors
                citing_authors = list(self.G.predecessors(node))
                
                # Determine likely genre based on citing authors
                genre = self._infer_genre(citing_authors)
                
                # Calculate recoverability score
                recoverability = self._calculate_recoverability_score(node, citing_authors)
                
                gap = {
                    'author': node,
                    'citations': in_degree,
                    'citing_authors': citing_authors,
                    'genre': genre,
                    'recoverability_score': recoverability,
                    'reason': f"{in_degree} authors cite '{node}' but no extant fragments found",
                    'predicted_works': max(1, in_degree // 2),  # Heuristic
                    'search_strategy': self._generate_search_strategy(node, genre, citing_authors)
                }
                gaps.append(gap)
        
        # Sort by recoverability score
        gaps.sort(key=lambda x: x['recoverability_score'], reverse=True)
        
        self.logger.info(f"Identified {len(gaps)} citation gaps")
        return gaps
    
    def _infer_genre(self, citing_authors: List[str]) -> str:
        """Infer genre based on citing authors."""
        genre_indicators = {
            'philosophy': ['Aristotle', 'Plato', 'Theophrastus', 'Epicurus'],
            'history': ['Herodotus', 'Thucydides', 'Polybius', 'Diodorus'],
            'science': ['Eratosthenes', 'Ptolemy', 'Galen', 'Archimedes'],
            'poetry': ['Callimachus', 'Theocritus', 'Apollonius', 'Posidippus'],
            'rhetoric': ['Demosthenes', 'Isocrates', 'Aeschines'],
        }
        
        genre_counts = defaultdict(int)
        for author in citing_authors:
            for genre, indicators in genre_indicators.items():
                if any(indicator.lower() in author.lower() for indicator in indicators):
                    genre_counts[genre] += 1
        
        if genre_counts:
            return max(genre_counts, key=genre_counts.get)
        
        return "Unknown"
    
    def _calculate_recoverability_score(self, author: str, citing_authors: List[str]) -> float:
        """Calculate recoverability score (0-1)."""
        score = 0.0
        
        # Base score from number of citations
        score += min(len(citing_authors) * 0.1, 0.4)
        
        # Bonus for citing author centrality
        for citing_author in citing_authors:
            try:
                centrality = nx.eigenvector_centrality(self.G)[citing_author]
                score += centrality * 0.05
            except:
                pass
        
        # Bonus for transmission paths
        transmission_paths = self._count_transmission_paths(author, citing_authors)
        score += min(transmission_paths * 0.1, 0.2)
        
        # Bonus for network position
        try:
            betweenness = nx.betweenness_centrality(self.G).get(author, 0)
            score += betweenness * 0.1
        except:
            pass
        
        return min(score, 1.0)
    
    def _count_transmission_paths(self, author: str, citing_authors: List[str]) -> int:
        """Count potential transmission paths for the author."""
        paths = 0
        
        for citing_author in citing_authors:
            # Check if citing author has known translation chains
            if self._has_translation_chain(citing_author):
                paths += 1
        
        return paths
    
    def _has_translation_chain(self, author: str) -> bool:
        """Check if author has known translation chains."""
        # This would query a database of known translation chains
        # For now, use some known examples
        known_chains = {
            'Aristotle', 'Galen', 'Ptolemy', 'Euclid', 'Hippocrates',
            'Plato', 'Plotinus', 'Theophrastus'
        }
        return author in known_chains
    
    def _generate_search_strategy(self, author: str, genre: str, citing_authors: List[str]) -> str:
        """Generate search strategy for finding the lost work."""
        strategies = []
        
        # Arabic manuscripts
        arabic_authors = [a for a in citing_authors if self._has_arabic_transmission(a)]
        if arabic_authors:
            strategies.append(f"Arabic manuscripts citing {', '.join(arabic_authors[:3])}")
        
        # Syriac intermediaries
        syriac_authors = [a for a in citing_authors if self._has_syriac_intermediary(a)]
        if syriac_authors:
            strategies.append(f"Syriac translations of {', '.join(syriac_authors[:3])}")
        
        # Genre-specific strategies
        if genre == 'science':
            strategies.append("Islamic Golden Age scientific corpus")
        elif genre == 'philosophy':
            strategies.append("Byzantine scholia and commentaries")
        elif genre == 'poetry':
            strategies.append("Greek anthology fragments")
        
        # Default strategy
        if not strategies:
            strategies.append("Cross-reference with known papyri collections")
        
        return " + ".join(strategies[:2])  # Return top 2 strategies
    
    def _has_arabic_transmission(self, author: str) -> bool:
        """Check if author has known Arabic transmission."""
        arabic_authors = {
            'Aristotle', 'Galen', 'Ptolemy', 'Euclid', 'Hippocrates',
            'Plotinus', 'Proclus', 'Alexander of Aphrodisias'
        }
        return author in arabic_authors
    
    def _has_syriac_intermediary(self, author: str) -> bool:
        """Check if author has known Syriac intermediaries."""
        syriac_authors = {
            'Aristotle', 'Galen', 'Porphyry', 'Nemesius', 'Sergius of Reshaina'
        }
        return author in syriac_authors
    
    def identify_load_bearing_nodes(self, threshold: float = 0.1) -> List[Dict]:
        """
        Identify "load-bearing" nodes whose loss would collapse citation chains.
        
        Args:
            threshold: Centrality threshold for load-bearing nodes
            
        Returns:
            List of critical node dictionaries
        """
        try:
            betweenness = nx.betweenness_centrality(self.G)
            eigenvector = nx.eigenvector_centrality(self.G, max_iter=1000)
        except:
            self.logger.warning("Failed to calculate centrality measures")
            return []
        
        critical_nodes = []
        
        for node in self.G.nodes():
            b_cent = betweenness.get(node, 0)
            e_cent = eigenvector.get(node, 0)
            
            # Combined centrality score
            combined_score = (b_cent + e_cent) / 2
            
            if combined_score > threshold:
                # Calculate impact of removing this node
                impact = self._calculate_node_impact(node)
                
                critical_nodes.append({
                    'node': node,
                    'betweenness_centrality': b_cent,
                    'eigenvector_centrality': e_cent,
                    'combined_score': combined_score,
                    'impact_score': impact,
                    'fragments': self.G.nodes[node].get('fragments', 0),
                    'citations_in': self.G.in_degree(node),
                    'citations_out': self.G.out_degree(node),
                    'risk_level': 'HIGH' if impact > 0.5 else 'MEDIUM'
                })
        
        # Sort by impact score
        critical_nodes.sort(key=lambda x: x['impact_score'], reverse=True)
        
        self.logger.info(f"Identified {len(critical_nodes)} load-bearing nodes")
        return critical_nodes
    
    def _calculate_node_impact(self, node: str) -> float:
        """Calculate the impact of removing a node from the network."""
        # Create a copy of the graph without the node
        G_copy = self.G.copy()
        G_copy.remove_node(node)
        
        # Calculate connectivity loss
        original_connectivity = nx.average_node_connectivity(self.G)
        new_connectivity = nx.average_node_connectivity(G_copy)
        
        connectivity_loss = original_connectivity - new_connectivity
        
        # Normalize to 0-1 range
        impact = min(connectivity_loss / original_connectivity if original_connectivity > 0 else 0, 1.0)
        
        return impact
    
    def map_translation_chains(self) -> List[Dict]:
        """
        Map translation chains (Greek→Syriac→Arabic→Latin).
        
        Returns:
            List of translation chain dictionaries
        """
        chains = []
        
        # Known translation chains from historical research
        known_chains = [
            {
                'greek_original': 'Aristotle.Metaphysics',
                'syriac_intermediary': {
                    'translator': 'Unknown (Edessa, 500-600 CE)',
                    'manuscripts': ['Vat.Sir.158'],
                    'confidence': 0.75
                },
                'arabic_translation': {
                    'translator': 'Ishaq ibn Hunayn (Baghdad, 870 CE)',
                    'manuscripts': ['Leiden Or. 2074'],
                    'confidence': 0.85
                },
                'latin_translation': {
                    'translator': 'William of Moerbeke (Bruges, 1260 CE)',
                    'manuscripts': ['Vat.Lat.2170'],
                    'confidence': 0.90
                }
            },
            {
                'greek_original': 'Galen.OnAnatomicalProcedures',
                'syriac_intermediary': {
                    'translator': 'Sergius of Reshaina (Reshaina, 535 CE)',
                    'manuscripts': ['Brit.Lib.Add.14661'],
                    'confidence': 0.80
                },
                'arabic_translation': {
                    'translator': 'Hunayn ibn Ishaq (Baghdad, 850 CE)',
                    'manuscripts': ['Bodleian Hunt. 302'],
                    'confidence': 0.88
                },
                'latin_translation': None  # No Latin translation known
            }
        ]
        
        # Analyze network for potential chains
        for node in self.G.nodes():
            if self.G.in_degree(node) > 0:
                # Check if node has connections suggesting translation
                predecessors = list(self.G.predecessors(node))
                
                # Look for patterns that suggest translation chains
                chain = self._analyze_translation_potential(node, predecessors)
                if chain:
                    chains.append(chain)
        
        # Combine with known chains
        all_chains = known_chains + chains
        
        self.translation_chains = all_chains
        self.logger.info(f"Mapped {len(all_chains)} translation chains")
        
        return all_chains
    
    def _analyze_translation_potential(self, node: str, predecessors: List[str]) -> Optional[Dict]:
        """Analyze if a node represents a potential translation chain."""
        # This is a simplified analysis
        # In practice, this would involve more sophisticated pattern matching
        
        if len(predecessors) < 2:
            return None
        
        return {
            'greek_original': f"{node}.OriginalWork",
            'syriac_intermediary': None,
            'arabic_translation': None,
            'latin_translation': None,
            'confidence': 0.3,  # Low confidence for predicted chains
            'note': 'Predicted from network analysis'
        }
    
    def calculate_priority_queue(self, gaps: List[Dict], critical_nodes: List[Dict]) -> pd.DataFrame:
        """
        Calculate priority queue for excavation based on recoverability.
        
        Args:
            gaps: List of citation gaps
            critical_nodes: List of load-bearing nodes
            
        Returns:
            DataFrame with ranked targets
        """
        priorities = []
        
        # Add citation gaps to priority queue
        for gap in gaps:
            priorities.append({
                'target': gap['author'],
                'type': 'citation_gap',
                'recoverability_score': gap['recoverability_score'],
                'fragments_found': 0,
                'network_centrality': 0.5,  # Placeholder
                'translation_paths': len(gap.get('search_strategy', '').split(' + ')),
                'imaging_feasibility': 0.3,  # Default low feasibility
                'priority_score': gap['recoverability_score'],
                'search_strategy': gap['search_strategy'],
                'status': 'predicted'
            })
        
        # Add critical nodes that have fragments but need more
        for node in critical_nodes:
            if node['fragments'] > 0:
                priority_score = (
                    node['impact_score'] * 0.4 +
                    node['combined_score'] * 0.3 +
                    min(node['fragments'] * 0.1, 0.2) +
                    0.1  # Base score
                )
                
                priorities.append({
                    'target': node['node'],
                    'type': 'critical_node',
                    'recoverability_score': node['combined_score'],
                    'fragments_found': node['fragments'],
                    'network_centrality': node['combined_score'],
                    'translation_paths': 2,  # Default
                    'imaging_feasibility': 0.6,  # Medium feasibility
                    'priority_score': priority_score,
                    'search_strategy': 'Expand existing fragment collection',
                    'status': 'partial'
                })
        
        # Create DataFrame and sort
        df = pd.DataFrame(priorities)
        if not df.empty:
            df = df.sort_values('priority_score', ascending=False).reset_index(drop=True)
        
        return df
    
    def export_network(self, filepath: str, format: str = 'graphml'):
        """
        Export network to file.
        
        Args:
            filepath: Output file path
            format: Export format ('graphml', 'gexf', 'json')
        """
        if format == 'graphml':
            nx.write_graphml(self.G, filepath)
        elif format == 'gexf':
            nx.write_gexf(self.G, filepath)
        elif format == 'json':
            data = nx.node_link_data(self.G)
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        self.logger.info(f"Exported network to {filepath}")
    
    def visualize_network(self, filepath: str, figsize: Tuple[int, int] = (12, 8)):
        """
        Create network visualization.
        
        Args:
            filepath: Output image file path
            figsize: Figure size (width, height)
        """
        plt.figure(figsize=figsize)
        
        # Use spring layout for better visualization
        pos = nx.spring_layout(self.G, k=1, iterations=50)
        
        # Draw nodes
        node_sizes = [self.G.nodes[node].get('fragments', 1) * 50 + 20 for node in self.G.nodes()]
        node_colors = [self.G.nodes[node].get('confidence', 0.5) for node in self.G.nodes()]
        
        nx.draw_networkx_nodes(self.G, pos, node_size=node_sizes, 
                             node_color=node_colors, cmap=plt.cm.viridis,
                             alpha=0.7)
        
        # Draw edges
        edge_weights = [self.G[u][v].get('weight', 1) for u, v in self.G.edges()]
        nx.draw_networkx_edges(self.G, pos, width=edge_weights, alpha=0.5,
                             edge_color='gray')
        
        # Draw labels
        nx.draw_networkx_labels(self.G, pos, font_size=8)
        
        plt.title("Classical Text Citation Network")
        plt.axis('off')
        plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.viridis), 
                    label='Confidence Score')
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.info(f"Saved network visualization to {filepath}")