#!/usr/bin/env python3
"""
Network Analysis Example

Demonstrates citation network analysis and visualization.
"""

from pinakes.network_builder import CitationNetwork
import json

def main():
    """Analyze citation networks."""
    
    print("🏛️  CALLIMACHINA: Network Analysis Example")
    print("=" * 60)
    
    # Build network for Eratosthenes
    target_work = "Eratosthenes Geographika"
    
    print(f"\n📊 Building citation network for: {target_work}")
    
    network = CitationNetwork()
    network.build_from_work_id(target_work)
    
    # Get network metrics
    print(f"\n📈 Network Metrics:")
    print("-" * 60)
    
    metrics = network.get_centrality_metrics()
    
    print(f"Total Nodes: {metrics['node_count']}")
    print(f"Total Edges: {metrics['edge_count']}")
    print(f"Network Density: {metrics['density']:.3f}")
    print(f"Average Degree: {metrics['average_degree']:.2f}")
    
    # Top central nodes
    print(f"\n🏆 Most Central Sources:")
    print("-" * 60)
    
    centrality = metrics['degree_centrality']
    sorted_nodes = sorted(centrality.items(), 
                         key=lambda x: x[1], 
                         reverse=True)[:10]
    
    for node, centrality_score in sorted_nodes:
        print(f"   {node:<30} {centrality_score:.3f}")
    
    # Export for visualization
    print(f"\n💾 Exporting network data...")
    
    # Gephi format
    network.export_gephi(f"network_{target_work.replace(' ', '_')}.gexf")
    print(f"   - Gephi format: network_{target_work.replace(' ', '_')}.gexf")
    
    # JSON format for web visualization
    network_data = {
        'nodes': [{'id': node, 'label': node, 'centrality': centrality[node]} 
                 for node in centrality],
        'edges': [{'source': edge[0], 'target': edge[1]} 
                 for edge in network.edges]
    }
    
    with open(f"network_{target_work.replace(' ', '_')}.json", 'w') as f:
        json.dump(network_data, f, indent=2)
    print(f"   - JSON format: network_{target_work.replace(' ', '_')}.json")
    
    # CSV format for statistical analysis
    df = network.to_dataframe()
    df.to_csv(f"network_{target_work.replace(' ', '_')}.csv", index=False)
    print(f"   - CSV format: network_{target_work.replace(' ', '_')}.csv")
    
    print(f"\n📊 Network analysis complete!")
    print(f"   Use Gephi (https://gephi.org) to visualize the .gexf file")
    
    return 0

if __name__ == "__main__":
    exit(main())