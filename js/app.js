import { DataManager } from './data.js';
import { UIManager } from './ui.js';
import { AUTH_KEY } from './config.js';
import { i18n } from './i18n.js';

const dataManager = new DataManager();
const uiManager = new UIManager(i18n);

// Auth State
let isAuthenticated = sessionStorage.getItem('vps_auth') === 'true';

// DOM Elements
const authOverlay = document.getElementById('auth-overlay');
const appContainer = document.getElementById('app');
const authInput = document.getElementById('auth-input');
const authBtn = document.getElementById('auth-btn');
const authError = document.getElementById('auth-error');

// Filter Elements
const filterVendor = document.getElementById('filter-vendor');
const filterRegion = document.getElementById('filter-region');
const filterPrice = document.getElementById('filter-price');
const filterRam = document.getElementById('filter-ram');
const filterCpu = document.getElementById('filter-cpu');
const filterBandwidth = document.getElementById('filter-bandwidth');
const resetBtn = document.getElementById('reset-filters-btn');
const langToggleBtn = document.getElementById('lang-toggle-btn');
const langText = document.getElementById('lang-text');

// --- Initialization ---

async function init() {
    // Initialize language
    i18n.updatePage();
    updateLangButton();
    setupLanguageToggle();
    
    checkUrlToken();
    if (isAuthenticated) {
        showApp();
    } else {
        setupAuthListeners();
    }
}

function checkUrlToken() {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');
    if (token === AUTH_KEY) {
        setAuthenticated();
    }
}

function setAuthenticated() {
    isAuthenticated = true;
    sessionStorage.setItem('vps_auth', 'true');
    showApp();
}

function setupAuthListeners() {
    authBtn.addEventListener('click', () => {
        if (authInput.value === AUTH_KEY) {
            setAuthenticated();
        } else {
            authError.classList.remove('hidden');
        }
    });

    authInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') authBtn.click();
    });
}

function showApp() {
    authOverlay.classList.add('hidden');
    appContainer.classList.remove('hidden');
    i18n.updatePage();
    loadData();
}

function setupLanguageToggle() {
    langToggleBtn.addEventListener('click', () => {
        const currentLang = i18n.getLanguage();
        const newLang = currentLang === 'zh' ? 'en' : 'zh';
        i18n.setLanguage(newLang);
        updateLangButton();
        updateUI(); // Re-render results with new language
    });
}

function updateLangButton() {
    const currentLang = i18n.getLanguage();
    langText.textContent = currentLang === 'zh' ? 'EN' : '中文';
}

async function loadData() {
    const success = await dataManager.loadAll();
    if (success) {
        setupFilters();
        updateUI();
    } else {
        alert('Failed to load data files. Please ensure you are running this on a local server (e.g., Live Server) to bypass CORS restrictions.');
    }
}

function setupFilters() {
    // Populate Vendor Dropdown
    const vendors = dataManager.getVendors();
    vendors.forEach(v => {
        const opt = document.createElement('option');
        opt.value = v;
        opt.textContent = v;
        filterVendor.appendChild(opt);
    });

    // Populate Region Dropdown
    const countries = dataManager.getCountries();
    countries.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.textContent = c;
        filterRegion.appendChild(opt);
    });

    // Listeners
    filterVendor.addEventListener('change', updateUI);
    filterRegion.addEventListener('change', updateUI);
    filterPrice.addEventListener('input', debounce(updateUI, 300));
    filterRam.addEventListener('change', updateUI);
    filterCpu.addEventListener('change', updateUI);
    filterBandwidth.addEventListener('change', updateUI);

    resetBtn.addEventListener('click', () => {
        filterVendor.value = '';
        filterRegion.value = '';
        filterPrice.value = '';
        filterRam.value = '0';
        filterCpu.value = '0';
        filterBandwidth.value = '0';
        updateUI();
    });
}

function updateUI() {
    const criteria = {
        vendor: filterVendor.value,
        region: filterRegion.value,
        maxPrice: filterPrice.value ? parseFloat(filterPrice.value) : null,
        minRam: parseFloat(filterRam.value),
        minCpu: parseInt(filterCpu.value),
        minBw: parseInt(filterBandwidth.value)
    };

    const grouped = dataManager.filter(criteria);
    uiManager.renderResults(grouped);
    uiManager.renderStats(dataManager.stats);
}

function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
}

// Start
init();
