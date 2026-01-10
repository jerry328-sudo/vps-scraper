export const translations = {
    zh: {
        // Page title
        title: "VPS Scout Pro",
        
        // Auth
        authTitle: "VPS Scout Pro",
        authSubtitle: "访问受限，需要验证",
        authPlaceholder: "输入访问密钥",
        authButton: "解锁",
        authError: "无效的访问密钥",
        
        // Header
        statsVendors: "厂商",
        statsSeries: "系列",
        statsPlans: "方案",
        resetFilters: "重置筛选",
        
        // Filters
        filterVendor: "厂商",
        filterVendorAll: "所有厂商",
        filterRegion: "地区",
        filterRegionAll: "所有地区",
        filterPrice: "最大预算（年付）",
        filterPricePlaceholder: "最高价格",
        filterRam: "最小内存",
        filterRamAny: "任意",
        filterCpu: "最小CPU",
        filterCpuAny: "任意",
        filterBandwidth: "最小带宽",
        filterBandwidthAny: "任意",
        
        // Results
        noResults: "没有符合条件的产品",
        products: "个产品",
        unknownProduct: "未知产品",
        global: "全球",
        review: "测评",
        buy: "购买",
        
        // Disclaimer
        disclaimerTitle: "免责声明 & 侵权删除",
        disclaimerSource: "数据来源：",
        disclaimerSourceText: "本站所有 VPS 测评数据均来自公开渠道（狗汪 VPS 测评网等），仅供学习参考，不构成任何购买建议。数据可能存在时效性问题，请以官方最新信息为准。",
        disclaimerLiability: "免责声明：",
        disclaimerLiabilityText: "本项目为技术学习项目，不承担因使用本站信息而产生的任何直接或间接损失。用户应自行判断并承担使用风险。",
        disclaimerRemoval: "侵权删除：",
        disclaimerRemovalText: "如果本站内容侵犯了您的合法权益，请通过 GitHub Issues 或邮件联系我，我们将在收到通知后 24 小时内删除相关内容。",
        disclaimerContact: "联系方式：",
        disclaimerContactText: "GitHub 项目地址"
    },
    en: {
        // Page title
        title: "VPS Scout Pro",
        
        // Auth
        authTitle: "VPS Scout Pro",
        authSubtitle: "Access Restricted. Verification Required.",
        authPlaceholder: "Enter Access Key",
        authButton: "Unlock",
        authError: "Invalid Access Key",
        
        // Header
        statsVendors: "Vendors",
        statsSeries: "Series",
        statsPlans: "Plans",
        resetFilters: "Reset Filters",
        
        // Filters
        filterVendor: "Vendor",
        filterVendorAll: "All Vendors",
        filterRegion: "Region",
        filterRegionAll: "All Regions",
        filterPrice: "Max Budget (Yearly)",
        filterPricePlaceholder: "Max Price",
        filterRam: "Min RAM",
        filterRamAny: "Any",
        filterCpu: "Min CPU",
        filterCpuAny: "Any",
        filterBandwidth: "Min Bandwidth",
        filterBandwidthAny: "Any",
        
        // Results
        noResults: "No products match your criteria",
        products: "Products",
        unknownProduct: "Unknown Product",
        global: "Global",
        review: "Review",
        buy: "Buy",
        
        // Disclaimer
        disclaimerTitle: "Disclaimer & Content Removal",
        disclaimerSource: "Data Source:",
        disclaimerSourceText: "All VPS benchmark data on this site comes from public sources (e.g., Gouwang VPS Benchmark), for learning and reference only, and does not constitute any purchase advice. Data may have timeliness issues; please refer to official information for the most accurate details.",
        disclaimerLiability: "Disclaimer:",
        disclaimerLiabilityText: "This project is for technical learning purposes only. We do not assume any direct or indirect liability for losses resulting from the use of information on this site. Users should make their own judgments and bear the risks of use.",
        disclaimerRemoval: "Content Removal:",
        disclaimerRemovalText: "If the content on this site infringes upon your legitimate rights and interests, please contact me via GitHub Issues or email, and we will remove the relevant content within 24 hours of receiving notice.",
        disclaimerContact: "Contact:",
        disclaimerContactText: "GitHub Project"
    }
};

export class I18n {
    constructor() {
        this.currentLang = localStorage.getItem('language') || 'zh';
        this.translations = translations;
    }

    setLanguage(lang) {
        if (this.translations[lang]) {
            this.currentLang = lang;
            localStorage.setItem('language', lang);
            this.updatePage();
        }
    }

    getLanguage() {
        return this.currentLang;
    }

    t(key) {
        return this.translations[this.currentLang][key] || key;
    }

    updatePage() {
        // Update page title
        document.title = this.t('title');
        
        // Update auth section
        const authTitle = document.querySelector('.auth-card .logo-text');
        if (authTitle) {
            authTitle.innerHTML = `VPS Scout <span class="accent-text">Pro</span>`;
        }
        
        const authSubtitle = document.querySelector('.auth-card p');
        if (authSubtitle) {
            authSubtitle.textContent = this.t('authSubtitle');
        }
        
        const authInput = document.getElementById('auth-input');
        if (authInput) {
            authInput.placeholder = this.t('authPlaceholder');
        }
        
        const authBtn = document.getElementById('auth-btn');
        if (authBtn) {
            authBtn.textContent = this.t('authButton');
        }
        
        const authError = document.getElementById('auth-error');
        if (authError) {
            authError.textContent = this.t('authError');
        }
        
        // Update header
        const resetFiltersBtn = document.getElementById('reset-filters-btn');
        if (resetFiltersBtn) {
            resetFiltersBtn.innerHTML = `<i data-lucide="rotate-ccw"></i> ${this.t('resetFilters')}`;
        }
        
        // Update filters
        const filterVendorLabel = document.querySelector('label[for="filter-vendor"]');
        if (filterVendorLabel) {
            filterVendorLabel.textContent = this.t('filterVendor');
        }
        
        const filterVendorSelect = document.getElementById('filter-vendor');
        if (filterVendorSelect) {
            const options = filterVendorSelect.querySelectorAll('option');
            options.forEach((opt, index) => {
                if (index === 0) {
                    opt.textContent = this.t('filterVendorAll');
                }
            });
        }
        
        const filterRegionLabel = document.querySelector('label[for="filter-region"]');
        if (filterRegionLabel) {
            filterRegionLabel.textContent = this.t('filterRegion');
        }
        
        const filterRegionSelect = document.getElementById('filter-region');
        if (filterRegionSelect) {
            const options = filterRegionSelect.querySelectorAll('option');
            options.forEach((opt, index) => {
                if (index === 0) {
                    opt.textContent = this.t('filterRegionAll');
                }
            });
        }
        
        const filterPriceLabel = document.querySelector('label[for="filter-price"]');
        if (filterPriceLabel) {
            filterPriceLabel.textContent = this.t('filterPrice');
        }
        
        const filterPriceInput = document.getElementById('filter-price');
        if (filterPriceInput) {
            filterPriceInput.placeholder = this.t('filterPricePlaceholder');
        }
        
        const filterRamLabel = document.querySelector('label[for="filter-ram"]');
        if (filterRamLabel) {
            filterRamLabel.textContent = this.t('filterRam');
        }
        
        const filterRamSelect = document.getElementById('filter-ram');
        if (filterRamSelect) {
            const options = filterRamSelect.querySelectorAll('option');
            options.forEach((opt, index) => {
                if (index === 0) {
                    opt.textContent = this.t('filterRamAny');
                }
            });
        }
        
        const filterCpuLabel = document.querySelector('label[for="filter-cpu"]');
        if (filterCpuLabel) {
            filterCpuLabel.textContent = this.t('filterCpu');
        }
        
        const filterCpuSelect = document.getElementById('filter-cpu');
        if (filterCpuSelect) {
            const options = filterCpuSelect.querySelectorAll('option');
            options.forEach((opt, index) => {
                if (index === 0) {
                    opt.textContent = this.t('filterCpuAny');
                }
            });
        }
        
        const filterBandwidthLabel = document.querySelector('label[for="filter-bandwidth"]');
        if (filterBandwidthLabel) {
            filterBandwidthLabel.textContent = this.t('filterBandwidth');
        }
        
        const filterBandwidthSelect = document.getElementById('filter-bandwidth');
        if (filterBandwidthSelect) {
            const options = filterBandwidthSelect.querySelectorAll('option');
            options.forEach((opt, index) => {
                if (index === 0) {
                    opt.textContent = this.t('filterBandwidthAny');
                }
            });
        }
        
        // Update disclaimer
        const disclaimerTitle = document.querySelector('.disclaimer-content h3');
        if (disclaimerTitle) {
            disclaimerTitle.innerHTML = `<i data-lucide="alert-circle"></i> ${this.t('disclaimerTitle')}`;
        }
        
        const disclaimerText = document.querySelector('.disclaimer-text');
        if (disclaimerText) {
            const paragraphs = disclaimerText.querySelectorAll('p');
            if (paragraphs[0]) {
                paragraphs[0].innerHTML = `<strong>${this.t('disclaimerSource')}</strong>${this.t('disclaimerSourceText')}`;
            }
            if (paragraphs[1]) {
                paragraphs[1].innerHTML = `<strong>${this.t('disclaimerLiability')}</strong>${this.t('disclaimerLiabilityText')}`;
            }
            if (paragraphs[2]) {
                paragraphs[2].innerHTML = `<strong>${this.t('disclaimerRemoval')}</strong>${this.t('disclaimerRemovalText')}`;
            }
            if (paragraphs[3]) {
                paragraphs[3].innerHTML = `<strong>${this.t('disclaimerContact')}</strong><a href="https://github.com/jerry328-sudo/vps-scraper" target="_blank" rel="noopener noreferrer">${this.t('disclaimerContactText')}</a>`;
            }
        }
        
        // Re-create icons
        lucide.createIcons();
    }
}

// Export singleton instance
export const i18n = new I18n();
