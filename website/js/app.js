// CALLIMACHINA Main Application
// Handles UI interactions and data visualization

class CallimachusApp {
    constructor() {
        this.api = null;
        this.currentView = 'overview';
        this.init();
    }

    async init() {
        // Wait for API to be available
        if (window.callimachinaAPI) {
            this.api = window.callimachinaAPI;
            await this.api.init();
            this.setupEventListeners();
            this.renderCurrentView();
        } else {
            console.error('CALLIMACHINA API not available');
        }
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.main-nav a').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = e.target.getAttribute('href').substring(1);
                this.navigateTo(target);
            });
        });

        // Reconstruction buttons
        document.querySelectorAll('.btn[data-action]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.target.getAttribute('data-action');
                const work = e.target.getAttribute('data-work');
                this.handleAction(action, work);
            });
        });

        // Search functionality
        const searchInput = document.getElementById('fragment-search');
        if (searchInput) {
            searchInput.addEventListener('keyup', () => {
                this.searchFragments();
            });
        }

        const filterSelect = document.getElementById('collection-filter');
        if (filterSelect) {
            filterSelect.addEventListener('change', () => {
                this.filterFragments();
            });
        }
    }

    navigateTo(view) {
        this.currentView = view;
        this.renderCurrentView();
        
        // Update active nav item
        document.querySelectorAll('.main-nav a').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelector(`.main-nav a[href="#${view}"]`).classList.add('active');
    }

    renderCurrentView() {
        switch (this.currentView) {
            case 'reconstructions':
                this.renderReconstructions();
                break;
            case 'fragments':
                this.renderFragments();
                break;
            case 'network':
                this.renderNetwork();
                break;
            case 'translations':
                this.renderTranslations();
                break;
            default:
                // Overview is static HTML
                break;
        }
    }

    renderReconstructions() {
        const container = document.getElementById('reconstructions');
        if (!container) return;

        const reconstructions = [
            {
                title: 'Eratosthenes Geographika',
                confidence: 0.996,
                fragments: 4,
                sources: ['Strabo', 'Cleomedes', 'Ptolemy', 'Stobaeus'],
                translations: ['Arabic (Yusuf al-Khuri)', 'Latin (William of Moerbeke)'],
                network: 'Degree centrality: 4'
            },
            {
                title: 'Hippolytus On Heraclitus',
                confidence: 0.986,
                fragments: 2,
                sources: ['Greek', 'Arabic via Syriac'],
                translations: ['Syriac (Sergius of Reshaina)', 'Arabic (Unknown)'],
                network: 'Cross-cultural transmission'
            },
            {
                title: 'Posidippus Epigrams',
                confidence: 0.965,
                fragments: 2,
                sources: ['Athenaeus', 'Palatine Anthology'],
                translations: ['None identified'],
                network: 'Greek direct transmission'
            },
            {
                title: 'Callimachus Aetia',
                confidence: 0.959,
                fragments: 2,
                sources: ['Papyrus', 'Scholia'],
                translations: ['None identified'],
                network: 'High priority reconstruction'
            }
        ];

        // Reconstructions are already rendered in HTML
        // This method can be used for dynamic updates
    }

    renderFragments() {
        const container = document.getElementById('fragment-list');
        if (!container || !this.api) return;

        const fragments = this.api.getFragments().fragments || [];
        
        container.innerHTML = fragments.map(fragment => `
            <div class="fragment-item">
                <div class="id">${fragment.id || 'Unknown'}</div>
                <div class="text">${fragment.text || 'No text available'}</div>
                <div class="metadata">
                    <span><strong>Collection:</strong> ${fragment.collection || 'Unknown'}</span>
                    <span><strong>Author:</strong> ${fragment.author || 'Unknown'}</span>
                    <span><strong>Date:</strong> ${fragment.date_range || 'Unknown'}</span>
                    <span><strong>Language:</strong> ${fragment.language || 'Unknown'}</span>
                </div>
            </div>
        `).join('');
    }

    searchFragments() {
        const query = document.getElementById('fragment-search').value;
        const fragments = this.api ? this.api.searchFragments(query) : [];
        
        const container = document.getElementById('fragment-list');
        if (!container) return;

        container.innerHTML = fragments.map(fragment => `
            <div class="fragment-item">
                <div class="id">${fragment.id || 'Unknown'}</div>
                <div class="text">${fragment.text || 'No text available'}</div>
                <div class="metadata">
                    <span><strong>Collection:</strong> ${fragment.collection || 'Unknown'}</span>
                    <span><strong>Author:</strong> ${fragment.author || 'Unknown'}</span>
                    <span><strong>Date:</strong> ${fragment.date_range || 'Unknown'}</span>
                </div>
            </div>
        `).join('');
    }

    filterFragments() {
        const collection = document.getElementById('collection-filter').value;
        const fragments = this.api ? this.api.filterFragmentsByCollection(collection) : [];
        
        const container = document.getElementById('fragment-list');
        if (!container) return;

        container.innerHTML = fragments.map(fragment => `
            <div class="fragment-item">
                <div class="id">${fragment.id || 'Unknown'}</div>
                <div class="text">${fragment.text || 'No text available'}</div>
                <div class="metadata">
                    <span><strong>Collection:</strong> ${fragment.collection || 'Unknown'}</span>
                    <span><strong>Author:</strong> ${fragment.author || 'Unknown'}</span>
                    <span><strong>Date:</strong> ${fragment.date_range || 'Unknown'}</span>
                </div>
            </div>
        `).join('');
    }

    renderNetwork() {
        const container = document.getElementById('network-visualization');
        if (!container || !this.api) return;

        const network = this.api.getNetwork();
        const nodes = network.elements?.nodes || [];
        const edges = network.elements?.edges || [];

        // Clear container
        container.innerHTML = '';

        // Create SVG
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('width', '100%');
        svg.setAttribute('height', '500');
        svg.style.background = '#f8f9fa';

        // Simple force-directed layout
        const width = container.offsetWidth || 800;
        const height = 500;

        // Position nodes in a circle
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = Math.min(width, height) * 0.3;

        nodes.forEach((node, i) => {
            const angle = (i / nodes.length) * 2 * Math.PI;
            node.x = centerX + radius * Math.cos(angle);
            node.y = centerY + radius * Math.sin(angle);
        });

        // Draw edges
        edges.forEach(edge => {
            const source = nodes.find(n => n.data.id === edge.data.source);
            const target = nodes.find(n => n.data.id === edge.data.target);
            
            if (source && target) {
                const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                line.setAttribute('x1', source.x);
                line.setAttribute('y1', source.y);
                line.setAttribute('x2', target.x);
                line.setAttribute('y2', target.y);
                line.setAttribute('stroke', '#999');
                line.setAttribute('stroke-width', '2');
                svg.appendChild(line);
            }
        });

        // Draw nodes
        nodes.forEach(node => {
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('cx', node.x);
            circle.setAttribute('cy', node.y);
            circle.setAttribute('r', '20');
            circle.setAttribute('fill', this.getNodeColor(node.data));
            circle.setAttribute('stroke', '#fff');
            circle.setAttribute('stroke-width', '3');
            
            // Add hover effect
            circle.addEventListener('mouseenter', () => {
                this.showNodeTooltip(node.data, node.x, node.y);
            });
            
            svg.appendChild(circle);

            // Add label
            const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            text.setAttribute('x', node.x);
            text.setAttribute('y', node.y + 35);
            text.setAttribute('text-anchor', 'middle');
            text.setAttribute('font-size', '12');
            text.setAttribute('fill', '#333');
            text.textContent = node.data.label || node.data.id;
            svg.appendChild(text);
        });

        container.appendChild(svg);
    }

    getNodeColor(nodeData) {
        const type = nodeData.type;
        switch (type) {
            case 'lost_work':
                return '#e74c3c'; // Red
            case 'citation_source':
                return '#3498db'; // Blue
            case 'key_transmitter':
                return '#f39c12'; // Gold
            default:
                return '#95a5a6'; // Gray
        }
    }

    showNodeTooltip(nodeData, x, y) {
        // Simple tooltip implementation
        const tooltip = document.createElement('div');
        tooltip.className = 'network-tooltip';
        tooltip.style.position = 'absolute';
        tooltip.style.left = x + 'px';
        tooltip.style.top = (y - 40) + 'px';
        tooltip.style.background = 'rgba(0,0,0,0.8)';
        tooltip.style.color = 'white';
        tooltip.style.padding = '0.5rem';
        tooltip.style.borderRadius = '4px';
        tooltip.style.fontSize = '0.9rem';
        tooltip.textContent = `${nodeData.label || nodeData.id} (${nodeData.type})`;
        
        document.body.appendChild(tooltip);
        
        setTimeout(() => {
            document.body.removeChild(tooltip);
        }, 2000);
    }

    renderTranslations() {
        const container = document.getElementById('translations');
        if (!container) return;

        // Translations are static content in HTML
        // This method can be used for dynamic updates
    }

    handleAction(action, work) {
        switch (action) {
            case 'view':
                this.viewReconstruction(work);
                break;
            case 'download':
                this.downloadYAML(work);
                break;
            default:
                console.log(`Action ${action} not implemented`);
        }
    }

    viewReconstruction(work) {
        const modal = document.createElement('div');
        modal.className = 'reconstruction-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        `;

        const content = document.createElement('div');
        content.style.cssText = `
            background: white;
            padding: 2rem;
            border-radius: 8px;
            max-width: 800px;
            max-height: 80vh;
            overflow-y: auto;
        `;

        content.innerHTML = `
            <h2>${work}</h2>
            <p>Reconstruction details would be loaded here...</p>
            <button onclick="this.closest('.reconstruction-modal').remove()">Close</button>
        `;

        modal.appendChild(content);
        document.body.appendChild(modal);
    }

    downloadYAML(work) {
        // Create sample YAML content
        const yamlContent = `
title: "${work}"
confidence: "99.6%"
fragments: 4
critical_apparatus: "Stadium length ambiguous"
next_steps:
  - "Query multispectral imaging"
  - "Cross-reference with Oxyrhynchus papyri"
`;

        const blob = new Blob([yamlContent], { type: 'text/yaml' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${work.replace(/[^a-z0-9]/gi, '_').toLowerCase()}_reconstruction.yml`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    exportNetwork(format) {
        if (this.api) {
            this.api.exportNetwork(format);
        }
    }

    loadNetwork(type) {
        // Network loading logic
        console.log(`Loading ${type} network`);
        this.renderNetwork();
    }

    // Utility methods
    formatConfidence(confidence) {
        return `${(confidence * 100).toFixed(1)}%`;
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString();
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.callimachinaApp = new CallimachusApp();
});

// Global functions for onclick handlers
function viewReconstruction(work) {
    if (window.callimachinaApp) {
        window.callimachinaApp.viewReconstruction(work);
    }
}

function downloadYAML(work) {
    if (window.callimachinaApp) {
        window.callimachinaApp.downloadYAML(work);
    }
}

function exportNetwork(format) {
    if (window.callimachinaApp) {
        window.callimachinaApp.exportNetwork(format);
    }
}

function loadNetwork(type) {
    if (window.callimachinaApp) {
        window.callimachinaApp.loadNetwork(type);
    }
}

function searchFragments() {
    if (window.callimachinaApp) {
        window.callimachinaApp.searchFragments();
    }
}

function filterFragments() {
    if (window.callimachinaApp) {
        window.callimachinaApp.filterFragments();
    }
}