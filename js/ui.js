export class UIManager {
    constructor() {
        this.container = document.getElementById('results-container');
        this.statsBar = document.getElementById('stats-bar');
    }

    renderStats(stats) {
        this.statsBar.innerHTML = `
            <div class="stat-item">Vendors: <b>${stats.vendors}</b></div>
            <div class="stat-item">Series: <b>${stats.products}</b></div>
            <div class="stat-item">Plans: <b>${stats.plans}</b></div>
        `;
    }

    renderResults(groupedData) {
        this.container.innerHTML = '';
        const vendors = Object.keys(groupedData).sort();

        if (vendors.length === 0) {
            this.container.innerHTML = `<div style="text-align:center; grid-column: 1/-1; padding: 4rem; color: var(--text-muted);">No products match your criteria.</div>`;
            return;
        }

        vendors.forEach(vendor => {
            const products = groupedData[vendor];
            const group = document.createElement('div');
            group.className = 'vendor-group';

            group.innerHTML = `
                <div class="vendor-header">
                    <h3>${vendor}</h3>
                    <span class="badge">${products.length} Products</span>
                </div>
                <div class="vendor-grid"></div>
            `;

            const grid = group.querySelector('.vendor-grid');
            products.forEach(p => {
                grid.appendChild(this.createProductCard(p));
            });

            this.container.appendChild(group);
        });

        lucide.createIcons();
    }

    createProductCard(product) {
        const card = document.createElement('div');
        card.className = 'product-card';

        // Header
        const header = document.createElement('div');
        header.className = 'card-header';
        header.innerHTML = `
            <div>
                <div class="product-title">${product.product_name || 'Unknown Product'}</div>
                <div class="product-location">
                    <i data-lucide="map-pin" style="width:14px; height:14px;"></i>
                    ${product.location || 'Global'}
                </div>
            </div>
            <button class="toggle-btn" aria-label="Toggle Details">
                <i data-lucide="chevron-down"></i>
            </button>
        `;

        // Body (Plans)
        const body = document.createElement('div');
        body.className = 'card-body';
        const planList = document.createElement('div');
        planList.className = 'plan-list';

        if (product.plans) {
            product.plans.forEach(plan => {
                planList.innerHTML += this.createPlanItem(plan);
            });
        }

        body.appendChild(planList);

        // Footer (Actions)
        const footer = document.createElement('div');
        footer.className = 'card-actions';
        footer.innerHTML = `
            <a href="${product.source_url || '#'}" target="_blank" class="action-btn">
                <i data-lucide="file-text" style="width:16px;"></i> Review
            </a>
            <a href="${product.purchase_url || '#'}" target="_blank" class="action-btn primary">
                <i data-lucide="shopping-cart" style="width:16px;"></i> Buy
            </a>
        `;

        card.appendChild(header);
        card.appendChild(body);
        card.appendChild(footer);

        // Toggle logic
        // We can just use a simple class toggle on body
        // But the requirement says "Expand/Collapse".
        // Let's implement interaction in app.js or here.
        // I'll attach listener here.
        const toggleBtn = header.querySelector('.toggle-btn');
        toggleBtn.onclick = (e) => {
            e.stopPropagation();
            const isHidden = body.style.display === 'none';
            body.style.display = isHidden ? 'block' : 'none';
            toggleBtn.style.transform = isHidden ? 'rotate(0deg)' : 'rotate(180deg)';
        };

        // Default expanded? Yes.

        return card;
    }

    createPlanItem(plan) {
        // Stats
        const cpu = plan.cpu ? `${plan.cpu.cores}C` : '-';
        const ram = plan.memory ? `${plan.memory.val_norm}${plan.memory.unit === 'MB' && plan.memory.val_norm < 1 ? 'MB' : 'GB'}` : '-';
        // Logic fix: normalizePlan already converted to GB if unit was MB. 
        // Actually normalizePlan sets val_norm. 
        // Let's render from original or normalized.
        // I set val_norm = value / 1024 if MB. So val_norm is in GB.
        // display: if val_norm < 1, maybe show MB? But let's stick to GB for consistency or use original.
        // Requirement: "Memory auto convert MB -> GB". So always show GB usually.

        const ramDisp = plan.memory ? `${plan.memory.val_norm}G` : '-';

        const ssd = plan.storage ? `${plan.storage.value}G ${plan.storage.type || ''}` : '-';

        // Bandwidth
        const bw = plan.bandwidth ? `${plan.bandwidth.value}${plan.bandwidth.unit}` : '-';
        // Wait, normalizePlan handles unit conversion to Mbps? 
        // I didn't change the original unit in normalizePlan, I set `disp_unit`.
        // Let's use that if available.
        const bwDisp = plan.bandwidth?.disp_val ? `${plan.bandwidth.disp_val}Mbps` : bw;

        // Traffic
        let traffic = '-';
        if (plan.traffic) {
            if (plan.traffic.value === -1) {
                traffic = '∞';
            } else {
                traffic = `${plan.traffic.value}${plan.traffic.unit}`;
            }
        }

        // Price
        // Use first price or all? 
        // "Price rendering: Support array".
        // Let's show the first one or a formatted text.
        // If multiple, maybe show "From $X".
        // Let's list them stacked if multiple? Or just the first one (usually monthly).
        // Let's just show the first one for the grid line item to save space.
        let priceHtml = '';
        if (plan.price_list && plan.price_list.length > 0) {
            const p = plan.price_list[0];
            const sym = p.currency === 'USD' ? '$' : '¥';
            priceHtml = `
                <div class="price-val">${sym}${p.value}</div>
                <div class="price-period">/${p.period}</div>
            `;
        }

        return `
            <div class="plan-item">
                <div class="plan-specs">
                    <div class="spec-row" title="CPU"><i data-lucide="cpu" style="width:14px; opacity:0.7"></i> ${cpu}</div>
                    <div class="spec-row" title="RAM"><i data-lucide="memory-stick" style="width:14px; opacity:0.7"></i> ${ramDisp}</div>
                    <div class="spec-row" title="Storage"><i data-lucide="hard-drive" style="width:14px; opacity:0.7"></i> ${ssd}</div>
                    <div class="spec-row" title="Bandwidth"><i data-lucide="activity" style="width:14px; opacity:0.7"></i> ${bwDisp}</div>
                    <div class="spec-row" title="Traffic"><i data-lucide="arrow-down-up" style="width:14px; opacity:0.7"></i> ${traffic}</div>
                </div>
                <div class="plan-price">
                    ${priceHtml}
                </div>
            </div>
        `;
    }
}
