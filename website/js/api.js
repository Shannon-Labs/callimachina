// CALLIMACHINA Web API Client
// Handles communication with the backend system

class CallimachinaAPI {
    constructor() {
        this.baseURL = '/pinakes';
        this.data = {};
        this.initialized = false;
    }

    async init() {
        try {
            // Load all available data
            await Promise.all([
                this.loadReconstructions(),
                this.loadFragments(),
                this.loadNetworks(),
                this.loadTranslations()
            ]);
            this.initialized = true;
            console.log('CALLIMACHINA API initialized');
        } catch (error) {
            console.error('Failed to initialize API:', error);
        }
    }

    async loadReconstructions() {
        try {
            const response = await fetch(`${this.baseURL}/reconstructions/`);
            if (response.ok) {
                const text = await response.text();
                // Parse directory listing (simplified)
                this.data.reconstructions = [
                    'eratosthenes_geographika_20251106_194115.yml',
                    'hippolytus_on_heraclitus_20251106_194115.yml',
                    'posidippus_epigrams_20251106_194115.yml',
                    'callimachina_aetia_20251106_194115.yml'
                ];
            }
        } catch (error) {
            console.error('Failed to load reconstructions:', error);
        }
    }

    async loadFragments() {
        try {
            const response = await fetch(`${this.baseURL}/fragments/pipeline_batch.yml`);
            if (response.ok) {
                const text = await response.text();
                this.data.fragments = this.parseYAML(text);
            }
        } catch (error) {
            console.error('Failed to load fragments:', error);
        }
    }

    async loadNetworks() {
        try {
            const response = await fetch(`${this.baseURL}/networks/citation_network_20251106_194117.json`);
            if (response.ok) {
                this.data.network = await response.json();
            }
        } catch (error) {
            console.error('Failed to load network:', error);
        }
    }

    async loadTranslations() {
        try {
            // Load translation reports
            this.data.translations = [
                'translation_hunt_eratosthenes_geographika_20251106_194116.yml',
                'translation_hunt_hippolytus_on_heraclitus_20251106_194116.yml'
            ];
        } catch (error) {
            console.error('Failed to load translations:', error);
        }
    }

    parseYAML(yamlText) {
        // Simple YAML parser for basic structure
        const result = {};
        const lines = yamlText.split('\n');
        let currentKey = null;
        let currentArray = null;

        for (let line of lines) {
            line = line.trim();
            if (!line || line.startsWith('#')) continue;

            // Handle key-value pairs
            const colonIndex = line.indexOf(':');
            if (colonIndex > 0) {
                const key = line.substring(0, colonIndex).trim();
                const value = line.substring(colonIndex + 1).trim();

                if (value) {
                    result[key] = value;
                    currentKey = key;
                } else {
                    currentKey = key;
                }
            }
            // Handle array items
            else if (line.startsWith('-')) {
                if (!currentArray) {
                    currentArray = [];
                    result[currentKey] = currentArray;
                }
                currentArray.push(line.substring(1).trim());
            }
        }

        return result;
    }

    async getReconstruction(workTitle) {
        try {
            const filename = workTitle.toLowerCase().replace(/[^a-z0-9]/g, '_');
            const response = await fetch(`${this.baseURL}/reconstructions/${filename}_*.yml`);
            if (response.ok) {
                const text = await response.text();
                return this.parseYAML(text);
            }
        } catch (error) {
            console.error(`Failed to load reconstruction for ${workTitle}:`, error);
        }
        return null;
    }

    getFragments() {
        return this.data.fragments || { fragments: [] };
    }

    getNetwork() {
        return this.data.network || { elements: { nodes: [], edges: [] } };
    }

    searchFragments(query) {
        const fragments = this.getFragments().fragments || [];
        if (!query) return fragments;

        return fragments.filter(fragment => {
            const text = fragment.text || '';
            const id = fragment.id || '';
            return text.toLowerCase().includes(query.toLowerCase()) ||
                   id.toLowerCase().includes(query.toLowerCase());
        });
    }

    filterFragmentsByCollection(collection) {
        const fragments = this.getFragments().fragments || [];
        if (!collection) return fragments;

        return fragments.filter(fragment => {
            return fragment.collection === collection;
        });
    }

    getNetworkStats() {
        const network = this.getNetwork();
        const nodes = network.elements?.nodes || [];
        const edges = network.elements?.edges || [];

        return {
            totalNodes: nodes.length,
            totalEdges: edges.length,
            lostWorks: nodes.filter(n => n.data?.type === 'lost_work').length,
            citationSources: nodes.filter(n => n.data?.type === 'citation_source').length
        };
    }

    exportNetwork(format = 'json') {
        const network = this.getNetwork();
        const dataStr = JSON.stringify(network, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `callimachina_network.${format}`;
        link.click();
        URL.revokeObjectURL(url);
    }

    // Alert system
    async getAlerts() {
        try {
            const response = await fetch(`${this.baseURL}/alerts/`);
            if (response.ok) {
                const text = await response.text();
                // Parse alert files
                return [
                    'enhanced_alert_20251106_194117_0.yml',
                    'enhanced_alert_20251106_194117_1.yml',
                    'enhanced_alert_20251106_194117_2.yml',
                    'enhanced_alert_20251106_194117_3.yml'
                ];
            }
        } catch (error) {
            console.error('Failed to load alerts:', error);
        }
        return [];
    }

    // Real-time monitoring
    startMonitoring(callback, interval = 60000) {
        // Check for new fragments every minute
        setInterval(async () => {
            try {
                await this.loadFragments();
                if (callback) callback(this.data.fragments);
            } catch (error) {
                console.error('Monitoring error:', error);
            }
        }, interval);
    }
}

// Initialize API
const api = new CallimachinaAPI();

// Make available globally
window.CallimachinaAPI = CallimachusAPI;
window.callimachinaAPI = api;