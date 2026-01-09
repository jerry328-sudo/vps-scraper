
import { DATA_FILES, COUNTRY_DICT } from './config.js';

export class DataManager {
    constructor() {
        this.rawProducts = [];
        this.groupedData = {};
        this.stats = { vendors: 0, products: 0, plans: 0 };
        this.availableCountries = new Set();
    }

    async loadAll() {
        let files = [];
        try {
            files = await this.discoverFiles();
        } catch (e) {
            console.warn('Auto-discovery failed, falling back to config', e);
        }

        if (files.length === 0) {
            files = DATA_FILES;
        }

        console.log(`Loading ${files.length} files...`);

        const promises = files.map(file => fetch(`data/raw/${file}`).then(res => res.json()));
        try {
            const results = await Promise.all(promises);
            this.processData(results);
            return true;
        } catch (e) {
            console.error('Failed to load data', e);
            return false;
        }
    }

    async discoverFiles() {
        try {
            const response = await fetch('data/raw/');
            if (!response.ok) throw new Error('Directory listing not available');

            const text = await response.text();
            // Parse HTML to find .json links
            const parser = new DOMParser();
            const doc = parser.parseFromString(text, 'text/html');
            const links = Array.from(doc.querySelectorAll('a'));

            const jsonFiles = links
                .map(a => a.getAttribute('href'))
                .filter(href => href && href.toLowerCase().endsWith('.json'))
                .map(href => href.replace(/^\.?\/?data\/raw\//, '')); // Cleanup path if needed

            return [...new Set(jsonFiles)]; // Unique
        } catch (e) {
            console.warn('Could not list directory', e);
            return [];
        }
    }

    processData(results) {
        this.rawProducts = [];
        this.availableCountries.clear();

        results.forEach(fileData => {
            const sourceUrl = fileData.source_url;
            // Iterate products in file
            if (fileData.products && Array.isArray(fileData.products)) {
                fileData.products.forEach(p => {
                    // Inject source_url and original article info if needed
                    p.source_url = sourceUrl;
                    p.source_title = fileData.article_title;

                    // Normalize Country
                    p.country_norm = this.matchCountry(p.location);
                    if (p.country_norm) {
                        this.availableCountries.add(p.country_norm);
                    }

                    // Normalize plans
                    if (p.plans) {
                        p.plans.forEach(plan => this.normalizePlan(plan));
                    }
                    this.rawProducts.push(p);
                });
            }
        });

        this.calculateStats();
    }

    matchCountry(locationStr) {
        if (!locationStr) return null;
        for (const [country, keywords] of Object.entries(COUNTRY_DICT)) {
            // Case insensitive check
            const lowerLoc = locationStr.toLowerCase();
            for (const keyword of keywords) {
                if (lowerLoc.includes(keyword.toLowerCase())) {
                    return country;
                }
            }
        }
        return 'Other';
    }

    getCountries() {
        return Array.from(this.availableCountries).sort();
    }

    normalizePlan(plan) {
        // Memory: MB -> GB
        if (plan.memory && plan.memory.unit && plan.memory.unit.toUpperCase() === 'MB') {
            plan.memory.val_norm = plan.memory.value / 1024;
        } else if (plan.memory) {
            plan.memory.val_norm = plan.memory.value;
        }

        // Bandwidth: Gbps -> Mbps
        if (plan.bandwidth && plan.bandwidth.unit) {
            const u = plan.bandwidth.unit.toLowerCase();
            if (u.includes('gbps')) {
                plan.bandwidth.val_norm = plan.bandwidth.value * 1000;
                plan.bandwidth.disp_unit = 'Mbps';
                plan.bandwidth.disp_val = plan.bandwidth.value * 1000;
            } else {
                plan.bandwidth.val_norm = plan.bandwidth.value;
                plan.bandwidth.disp_unit = 'Mbps';
                plan.bandwidth.disp_val = plan.bandwidth.value;
            }
        }

        // Price formatting helpers
        if (!Array.isArray(plan.price)) {
            plan.price_list = [plan.price];
        } else {
            plan.price_list = plan.price;
        }
    }

    calculateStats() {
        const vendors = new Set();
        let planCount = 0;

        this.rawProducts.forEach(p => {
            if (p.vendor) vendors.add(p.vendor);
            if (p.plans) planCount += p.plans.length;
        });

        this.stats = {
            vendors: vendors.size,
            products: this.rawProducts.length,
            plans: planCount
        };
    }

    getVendors() {
        // Return sorted list of vendors
        const vendors = [...new Set(this.rawProducts.map(p => p.vendor))];
        return vendors.sort();
    }

    filter(criteria) {
        // criteria: { vendor, region, maxPrice, minRam, minCpu, minBw }
        let filtered = this.rawProducts;

        if (criteria.vendor) {
            filtered = filtered.filter(p => p.vendor === criteria.vendor);
        }

        if (criteria.region) {
            // Exact match on normalized country
            filtered = filtered.filter(p => p.country_norm === criteria.region);
        }

        // For Plan-level filters, we check if *any* plan in the product matches.
        // If it matches, we assume the whole product is relevant.
        // We could also filter the plans inside the product for display, but that modifies data structure.
        // Let's just return products that have qualifying plans.

        filtered = filtered.filter(p => {
            if (!p.plans || p.plans.length === 0) return false;
            return p.plans.some(plan => {
                let pass = true;

                // Min RAM (GB)
                if (criteria.minRam) {
                    if ((plan.memory?.val_norm || 0) < criteria.minRam) pass = false;
                }

                // Min CPU (Cores)
                if (criteria.minCpu) {
                    if ((plan.cpu?.cores || 0) < criteria.minCpu) pass = false;
                }

                // Min Bandwidth (Mbps)
                if (criteria.minBw) {
                    if ((plan.bandwidth?.val_norm || 0) < criteria.minBw) pass = false;
                }

                // Max Price (Yearly normalized? Or just check available periods check)
                // Requirement: "Input yearly price limit (CNY/Year)"
                // We need to normalize price to yearly to compare?
                // Or just if any price period * 12 (if month) <= limit?
                // Let's assume input is Yearly Budget.
                if (criteria.maxPrice) {
                    // Check if any price option fits budget
                    const fits = plan.price_list.some(pr => {
                        let yearlyPrice = 9999999;
                        if (pr.period === '年') yearlyPrice = pr.value;
                        else if (pr.period === '月') yearlyPrice = pr.value * 12;
                        else if (pr.period === '季') yearlyPrice = pr.value * 4;
                        else if (pr.period === '半年') yearlyPrice = pr.value * 2;

                        return yearlyPrice <= criteria.maxPrice;
                    });
                    if (!fits) pass = false;
                }

                return pass;
            });
        });

        // Group by vendor
        const grouped = {};
        filtered.forEach(p => {
            if (!grouped[p.vendor]) grouped[p.vendor] = [];
            grouped[p.vendor].push(p);
        });

        return grouped;
    }
}
