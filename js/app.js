import { DataManager } from './data.js';
import { UIManager } from './ui.js';
import { AUTH_KEY } from './config.js';

const dataManager = new DataManager();
const uiManager = new UIManager();

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
const filterBandwidth = document.getElementById('filter-bandwidth');
const resetBtn = document.getElementById('reset-filters-btn');

// Chip Filters
const chipFilters = {
    ram: null,
    cpu: null
};

// --- Initialization ---

async function init() {
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
    loadData();
}

async function loadData() {
    const success = await dataManager.loadAll();
    if (success) {
        setupFilters();
        updateUI();
    } else {
        alert("Failed to load data files. Please ensure you are running this on a local server (e.g., Live Server) to bypass CORS restrictions.");
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

    // Listeners
    filterVendor.addEventListener('change', updateUI);
    filterRegion.addEventListener('input', debounce(updateUI, 300));
    filterPrice.addEventListener('input', debounce(updateUI, 300));
    filterBandwidth.addEventListener('change', updateUI);

    // Chip Listeners (RAM / CPU)
    document.querySelectorAll('.chip').forEach(chip => {
        chip.addEventListener('click', (e) => {
            const type = chip.dataset.filter; // 'ram' or 'cpu'
            const val = parseFloat(chip.dataset.val);

            // Toggle
            if (chipFilters[type] === val) {
                chipFilters[type] = null;
                chip.classList.remove('active');
            } else {
                chipFilters[type] = val;
                // Deactivate data-filter=same group
                document.querySelectorAll(`.chip[data-filter="${type}"]`).forEach(c => c.classList.remove('active'));
                chip.classList.add('active');
            }
            updateUI();
        });
    });

    resetBtn.addEventListener('click', () => {
        filterVendor.value = "";
        filterRegion.value = "";
        filterPrice.value = "";
        filterBandwidth.value = "0";
        chipFilters.ram = null;
        chipFilters.cpu = null;
        document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
        updateUI();
    });
}

function updateUI() {
    const criteria = {
        vendor: filterVendor.value,
        region: filterRegion.value,
        maxPrice: filterPrice.value ? parseFloat(filterPrice.value) : null,
        minRam: chipFilters.ram,
        minCpu: chipFilters.cpu,
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
