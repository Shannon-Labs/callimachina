#!/usr/bin/env python3
"""
Citation Network Builder for CALLIMACHINA Protocol
Visualizes transmission chains and knowledge survival paths

Creates Gephi-compatible graph files for scholarly analysis
"""

import json
import yaml
import re
from datetime import datetime
from typing import Dict, List, Set, Tuple, Any
from collections import defaultdict
import xml.etree.ElementTree as ET

class NetworkBuilder:
    def __init__(self):
        self.graph = {
            'nodes': {},
            'edges': [],
            'metadata': {
                'created': datetime.now().isoformat(),
                'format': 'citation_network',
                'version': '2.0'
            }
        }
        self.lost_works_index = {}
        self.citation_chains = defaultdict(list)
        
        print("[NETWORK BUILDER] Initializing citation network system...")
    
    def build_transmission_network(self, lost_works: List[Dict]) -> Dict:
        """
        Build complete citation network from lost works data
        """
        print(f"[NETWORK BUILD] Processing {len(lost_works)} lost works...")
        
        for work in lost_works:
            self._add_lost_work_to_network(work)
        
        # Add transmission edges
        self._add_transmission_edges()
        
        # Calculate network metrics
        self._calculate_network_metrics()
        
        print(f"[NETWORK BUILD] Created network with {len(self.graph['nodes'])} nodes and {len(self.graph['edges'])} edges")
        
        return self.graph
    
    def _add_lost_work_to_network(self, lost_work: Dict):
        """Add a lost work and its citations to the network"""
        work_id = lost_work['title'].replace(' ', '_').lower()
        
        # Add lost work node
        self.graph['nodes'][work_id] = {
            'id': work_id,
            'label': lost_work['title'],
            'type': 'lost_work',
            'priority_score': lost_work.get('priority_score', 0),
            'confidence': lost_work.get('confidence', 0),
            'citation_count': lost_work.get('citation_count', 0),
            'survival_paths': lost_work.get('survival_paths', []),
            'status': lost_work.get('status', 'lost_confirmed'),
            'fragments': lost_work.get('fragments', 0),
            'color': '#FF0000',  # Red for lost works
            'size': 20 + lost_work.get('priority_score', 0) / 5  # Size by importance
        }
        
        # Store in index
        self.lost_works_index[work_id] = lost_work
        
        # Add citation source nodes and edges
        for citation in lost_work.get('citations', []):
            self._add_citation_edge(work_id, citation)
    
    def _add_citation_edge(self, work_id: str, citation: Dict):
        """Add a citation source node and edge"""
        source = citation['source']
        source_id = source.replace(' ', '_').lower()
        
        # Add source node if not exists
        if source_id not in self.graph['nodes']:
            self.graph['nodes'][source_id] = {
                'id': source_id,
                'label': source,
                'type': 'citation_source',
                'date_range': citation.get('date_range', 'unknown'),
                'language': citation.get('language', 'unknown'),
                'color': '#4169E1',  # Blue for sources
                'size': 15
            }
        
        # Add citation edge
        edge_id = f"{source_id}_to_{work_id}_{len(self.graph['edges'])}"
        
        edge = {
            'id': edge_id,
            'source': source_id,
            'target': work_id,
            'type': 'cites',
            'citation_type': citation.get('citation_type', 'unknown'),
            'confidence': citation.get('independence_score', 0.5),
            'date_range': citation.get('date_range', 'unknown'),
            'weight': citation.get('independence_score', 0.5) * 2
        }
        
        self.graph['edges'].append(edge)
        self.citation_chains[work_id].append(citation)
    
    def _add_transmission_edges(self):
        """Add edges showing transmission between sources"""
        # Create temporal chains based on date ranges
        sources = [node for node in self.graph['nodes'].values() 
                  if node['type'] == 'citation_source']
        
        # Sort sources by estimated date
        dated_sources = []
        for source in sources:
            date_range = source.get('date_range', 'unknown')
            century = self._extract_century(date_range)
            if century:
                dated_sources.append((source, century))
        
        dated_sources.sort(key=lambda x: x[1])
        
        # Add temporal edges between consecutive sources
        for i in range(len(dated_sources) - 1):
            source1, century1 = dated_sources[i]
            source2, century2 = dated_sources[i + 1]
            
            # Only connect if they're citing the same work
            common_works = self._find_common_citations(source1['id'], source2['id'])
            
            if common_works:
                edge_id = f"transmission_{source1['id']}_to_{source2['id']}"
                
                edge = {
                    'id': edge_id,
                    'source': source1['id'],
                    'target': source2['id'],
                    'type': 'transmission',
                    'relationship': 'temporal_succession',
                    'century_gap': century2 - century1,
                    'weight': len(common_works),
                    'common_works': common_works
                }
                
                self.graph['edges'].append(edge)
    
    def _find_common_citations(self, source1_id: str, source2_id: str) -> List[str]:
        """Find works commonly cited by two sources"""
        works1 = set()
        works2 = set()
        
        for work_id, citations in self.citation_chains.items():
            sources = [c['source'].replace(' ', '_').lower() for c in citations]
            if source1_id in sources:
                works1.add(work_id)
            if source2_id in sources:
                works2.add(work_id)
        
        return list(works1 & works2)
    
    def _extract_century(self, date_range: str) -> int:
        """Extract century number from date range"""
        if not date_range or date_range == 'unknown':
            return None
        
        # Look for patterns like "c. 5th century CE" or "c. 100-170 CE"
        patterns = [
            r'(\d+)(?:st|nd|rd|th)\s+century',
            r'c\.\s*(\d+)\s+century',
            r'(\d+)(?:st|nd|rd|th)\s+century\s+(BCE|CE)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, date_range, re.IGNORECASE)
            if match:
                century = int(match.group(1))
                if 'BCE' in date_range:
                    return -century
                return century
        
        # Try to extract from year ranges
        year_patterns = [r'(\d+)\s*(?:BCE|CE)', r'(\d+)-\d+\s*(?:BCE|CE)']
        for pattern in year_patterns:
            match = re.search(pattern, date_range)
            if match:
                year = int(match.group(1))
                century = (year + 99) // 100
                if 'BCE' in date_range:
                    return -century
                return century
        
        return None
    
    def _calculate_network_metrics(self):
        """Calculate network centrality and importance metrics"""
        # Calculate degree centrality for each node
        degree_counts = defaultdict(int)
        
        for edge in self.graph['edges']:
            degree_counts[edge['source']] += 1
            degree_counts[edge['target']] += 1
        
        # Update nodes with centrality scores
        for node_id, node in self.graph['nodes'].items():
            node['degree_centrality'] = degree_counts.get(node_id, 0)
            
            # Identify key transmission nodes
            if node['type'] == 'citation_source' and degree_counts.get(node_id, 0) > 3:
                node['role'] = 'key_transmitter'
                node['color'] = '#FFD700'  # Gold for key transmitters
            
            # Identify lost works with high citation density
            if node['type'] == 'lost_work' and degree_counts.get(node_id, 0) > 5:
                node['role'] = 'well_attested'
                node['color'] = '#FF69B4'  # Pink for well-attested lost works
    
    def export_gephi(self, filename: str = None) -> str:
        """Export network to Gephi-compatible GEXF format"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/Volumes/VIXinSSD/callimachina/pinakes/networks/citation_network_{timestamp}.gexf"
        
        # Ensure directory exists
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Create GEXF XML
        gexf = ET.Element('gexf', {'xmlns': 'http://www.gexf.net/1.2draft',
                                   'version': '1.2'})
        
        # Meta
        meta = ET.SubElement(gexf, 'meta')
        ET.SubElement(meta, 'creator').text = 'CALLIMACHINA Alexandria Reconstruction Protocol'
        ET.SubElement(meta, 'description').text = f'Citation network for lost classical works - {self.graph["metadata"]["created"]}'
        
        # Graph
        graph = ET.SubElement(gexf, 'graph', {'defaultedgetype': 'directed', 'mode': 'static'})
        
        # Attributes
        attributes = ET.SubElement(graph, 'attributes', {'class': 'node'})
        attr_defs = [
            ('label', 'string'),
            ('type', 'string'),
            ('priority_score', 'float'),
            ('confidence', 'float'),
            ('citation_count', 'integer'),
            ('color', 'string'),
            ('size', 'float'),
            ('role', 'string'),
            ('degree_centrality', 'integer')
        ]
        
        for i, (attr_name, attr_type) in enumerate(attr_defs):
            ET.SubElement(attributes, 'attribute', {'id': str(i), 'title': attr_name, 'type': attr_type})
        
        # Nodes
        nodes_elem = ET.SubElement(graph, 'nodes')
        
        for node_id, node in self.graph['nodes'].items():
            node_elem = ET.SubElement(nodes_elem, 'node', {'id': node_id, 'label': node['label']})
            attvalues = ET.SubElement(node_elem, 'attvalues')
            
            for i, (attr_name, _) in enumerate(attr_defs):
                if attr_name in node:
                    ET.SubElement(attvalues, 'attvalue', {'for': str(i), 'value': str(node[attr_name])})
        
        # Edges
        edges_elem = ET.SubElement(graph, 'edges')
        
        for i, edge in enumerate(self.graph['edges']):
            edge_elem = ET.SubElement(edges_elem, 'edge', {
                'id': str(i),
                'source': edge['source'],
                'target': edge['target'],
                'label': edge['type']
            })
        
        # Write to file
        tree = ET.ElementTree(gexf)
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        
        print(f"[GEPHI EXPORT] Network saved to {filename}")
        print(f"  Nodes: {len(self.graph['nodes'])}")
        print(f"  Edges: {len(self.graph['edges'])}")
        
        return filename
    
    def export_cytoscape(self, filename: str = None) -> str:
        """Export network to Cytoscape JSON format"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/Volumes/VIXinSSD/callimachina/pinakes/networks/citation_network_{timestamp}.json"
        
        # Ensure directory exists
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Convert to Cytoscape format
        cytoscape = {
            'format_version': '1.0',
            'generated_by': 'callimachina_network_builder',
            'target_cytoscapejs_version': '~2.1',
            'data': {
                'shared_name': 'CALLIMACHINA Citation Network',
                'name': 'CALLIMACHINA Citation Network',
                'created': self.graph['metadata']['created']
            },
            'elements': {
                'nodes': [],
                'edges': []
            }
        }
        
        # Add nodes
        for node_id, node in self.graph['nodes'].items():
            cytoscape_node = {
                'data': {
                    'id': node_id,
                    'shared_name': node['label'],
                    'name': node['label'],
                    **{k: v for k, v in node.items() if k != 'label'}
                }
            }
            cytoscape['elements']['nodes'].append(cytoscape_node)
        
        # Add edges
        for i, edge in enumerate(self.graph['edges']):
            cytoscape_edge = {
                'data': {
                    'id': f"edge_{i}",
                    'source': edge['source'],
                    'target': edge['target'],
                    'shared_name': f"{edge['source']} to {edge['target']}",
                    **{k: v for k, v in edge.items() if k not in ['source', 'target']}
                }
            }
            cytoscape['elements']['edges'].append(cytoscape_edge)
        
        # Write JSON
        with open(filename, 'w') as f:
            json.dump(cytoscape, f, indent=2, default=str)
        
        print(f"[CYTOSCAPE EXPORT] Network saved to {filename}")
        
        return filename
    
    def generate_network_report(self, filename: str = None) -> str:
        """Generate human-readable network analysis report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/Volumes/VIXinSSD/callimachina/pinakes/networks/network_report_{timestamp}.yml"
        
        # Ensure directory exists
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Calculate network statistics
        lost_works = [n for n in self.graph['nodes'].values() if n['type'] == 'lost_work']
        sources = [n for n in self.graph['nodes'].values() if n['type'] == 'citation_source']
        
        # Find key transmitters
        key_transmitters = [n for n in sources if n.get('role') == 'key_transmitter']
        
        # Find most cited works
        most_cited = sorted(lost_works, key=lambda x: x.get('degree_centrality', 0), reverse=True)[:5]
        
        report = {
            'report_timestamp': datetime.now().isoformat(),
            'network_summary': {
                'total_nodes': len(self.graph['nodes']),
                'total_edges': len(self.graph['edges']),
                'lost_works': len(lost_works),
                'citation_sources': len(sources),
                'key_transmitters': len(key_transmitters)
            },
            'most_cited_lost_works': [
                {
                    'title': work['label'],
                    'citations': work.get('degree_centrality', 0),
                    'priority_score': work.get('priority_score', 0),
                    'confidence': work.get('confidence', 0)
                }
                for work in most_cited
            ],
            'key_transmitters': [
                {
                    'source': transmitter['label'],
                    'citations': transmitter.get('degree_centrality', 0),
                    'date_range': transmitter.get('date_range', 'unknown')
                }
                for transmitter in key_transmitters
            ],
            'survival_paths': self._analyze_survival_paths(),
            'transmission_gaps': self._identify_gaps(),
            'recommendations': self._generate_network_recommendations()
        }
        
        with open(filename, 'w') as f:
            yaml.dump(report, f, default_flow_style=False, allow_unicode=True)
        
        print(f"[NETWORK REPORT] Analysis saved to {filename}")
        
        return filename
    
    def _analyze_survival_paths(self) -> Dict:
        """Analyze knowledge survival paths through the network"""
        paths = {
            'greek_direct': 0,
            'greek_indirect': 0,
            'arabic_translation': 0,
            'latin_translation': 0,
            'syriac_translation': 0,
            'cross_cultural': 0
        }
        
        for work in self.lost_works_index.values():
            survival_paths = work.get('survival_paths', [])
            for path in survival_paths:
                if path in paths:
                    paths[path] += 1
            
            # Count cross-cultural paths
            if len(survival_paths) > 1:
                paths['cross_cultural'] += 1
        
        return paths
    
    def _identify_gaps(self) -> List[Dict]:
        """Identify gaps in the transmission record"""
        gaps = []
        
        # Look for lost works with few citations
        for work_id, work in self.lost_works_index.items():
            citations = work.get('citations', [])
            if len(citations) <= 2:
                gaps.append({
                    'work': work['title'],
                    'citations': len(citations),
                    'gap_type': 'under_attested',
                    'priority': 'find_additional_sources'
                })
        
        # Look for temporal gaps in transmission
        dated_sources = []
        for node in self.graph['nodes'].values():
            if node['type'] == 'citation_source':
                century = self._extract_century(node.get('date_range', ''))
                if century:
                    dated_sources.append((node['label'], century))
        
        dated_sources.sort(key=lambda x: x[1])
        
        # Find gaps > 2 centuries
        for i in range(len(dated_sources) - 1):
            name1, cent1 = dated_sources[i]
            name2, cent2 = dated_sources[i + 1]
            gap = cent2 - cent1
            
            if gap > 2:
                gaps.append({
                    'gap_type': 'temporal',
                    'period': f"{cent1}th to {cent2}th century",
                    'duration': gap,
                    'sources': [name1, name2],
                    'priority': 'investigate_gap'
                })
        
        return gaps
    
    def _generate_network_recommendations(self) -> List[str]:
        """Generate recommendations based on network analysis"""
        recommendations = []
        
        # Find works that need more citations
        under_attested = [w for w in self.lost_works_index.values() 
                         if len(w.get('citations', [])) <= 2]
        
        if under_attested:
            recommendations.append(f"Search for additional citations for {len(under_attested)} under-attested works")
        
        # Recommend Arabic/Latin translation hunting
        greek_only = [w for w in self.lost_works_index.values() 
                     if w.get('survival_paths') == ['greek_direct']]
        
        if greek_only:
            recommendations.append(f"Investigate Arabic/Latin translations for {len(greek_only)} Greek-only works")
        
        # Recommend stylometric analysis for anonymous fragments
        recommendations.append("Apply stylometric fingerprinting to anonymous papyrus fragments")
        
        # Recommend multispectral imaging for key transmitters
        key_transmitters = [n for n in self.graph['nodes'].values() 
                           if n.get('role') == 'key_transmitter']
        
        if key_transmitters:
            recommendations.append(f"Consider multispectral imaging of manuscripts from {len(key_transmitters)} key transmitters")
        
        return recommendations

if __name__ == "__main__":
    print("=" * 60)
    print("CALLIMACHINA CITATION NETWORK BUILDER")
    print("=" * 60)
    
    builder = NetworkBuilder()
    
    # Load lost works data
    import yaml
    with open('/Volumes/VIXinSSD/callimachina/pinakes/triangulation_results.yml', 'r') as f:
        triangulation_data = yaml.safe_load(f)
    
    lost_works = triangulation_data['lost_works']
    
    print(f"\n[NETWORK CONSTRUCTION] Building citation network for {len(lost_works)} lost works...")
    
    # Build network
    network = builder.build_transmission_network(lost_works)
    
    # Export formats
    print("\n[EXPORTING NETWORK] Multiple formats...")
    
    gexf_file = builder.export_gephi()
    json_file = builder.export_cytoscape()
    report_file = builder.generate_network_report()
    
    print(f"\n[NETWORK ANALYSIS COMPLETE]")
    print(f"  Gephi format: {gexf_file}")
    print(f"  Cytoscape format: {json_file}")
    print(f"  Analysis report: {report_file}")
    
    # Print key findings
    print(f"\n[KEY FINDINGS]")
    print(f"  Lost works: {len([n for n in network['nodes'].values() if n['type'] == 'lost_work'])}")
    print(f"  Citation sources: {len([n for n in network['nodes'].values() if n['type'] == 'citation_source'])}")
    print(f"  Transmission edges: {len([e for e in network['edges'] if e['type'] == 'transmission'])}")
    
    key_transmitters = [n for n in network['nodes'].values() if n.get('role') == 'key_transmitter']
    if key_transmitters:
        print(f"  Key transmitters: {', '.join([k['label'] for k in key_transmitters])}")
