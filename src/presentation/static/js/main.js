/**
 * ViewTrendsSL - Main JavaScript
 * Client-side functionality for the Streamlit application
 * Author: ViewTrendsSL Team
 * Date: 2025
 */

// ===== GLOBAL VARIABLES =====
const ViewTrendsSL = {
    version: '1.0.0',
    apiBaseUrl: 'http://localhost:5000',
    config: {
        chartColors: [
            '#667eea', '#764ba2', '#f093fb', '#4facfe',
            '#43e97b', '#38f9d7', '#ffecd2', '#fcb69f'
        ],
        animationDuration: 300,
        debounceDelay: 500
    },
    cache: new Map(),
    utils: {},
    components: {},
    api: {}
};

// ===== UTILITY FUNCTIONS =====
ViewTrendsSL.utils = {
    /**
     * Debounce function to limit API calls
     */
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Format numbers with appropriate suffixes
     */
    formatNumber: function(num) {
        if (num >= 1000000000) {
            return (num / 1000000000).toFixed(1) + 'B';
        }
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        }
        if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    },

    /**
     * Format duration from seconds to readable format
     */
    formatDuration: function(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;

        if (hours > 0) {
            return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    },

    /**
     * Validate YouTube URL
     */
    isValidYouTubeUrl: function(url) {
        const patterns = [
            /^https?:\/\/(www\.)?youtube\.com\/watch\?v=[\w-]+/,
            /^https?:\/\/youtu\.be\/[\w-]+/,
            /^https?:\/\/(www\.)?youtube\.com\/embed\/[\w-]+/
        ];
        return patterns.some(pattern => pattern.test(url));
    },

    /**
     * Extract video ID from YouTube URL
     */
    extractVideoId: function(url) {
        const patterns = [
            /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/
        ];
        
        for (const pattern of patterns) {
            const match = url.match(pattern);
            if (match) return match[1];
        }
        return null;
    },

    /**
     * Show loading spinner
     */
    showLoading: function(element) {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        if (element) {
            element.innerHTML = '<div class="loading-spinner"></div>';
        }
    },

    /**
     * Hide loading spinner
     */
    hideLoading: function(element) {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        if (element) {
            const spinner = element.querySelector('.loading-spinner');
            if (spinner) {
                spinner.remove();
            }
        }
    },

    /**
     * Show notification
     */
    showNotification: function(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `alert ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
            animation: slideIn 0.3s ease-out;
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, duration);
    },

    /**
     * Copy text to clipboard
     */
    copyToClipboard: function(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                this.showNotification('Copied to clipboard!', 'success', 2000);
            });
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.showNotification('Copied to clipboard!', 'success', 2000);
        }
    },

    /**
     * Generate random color from palette
     */
    getRandomColor: function() {
        const colors = ViewTrendsSL.config.chartColors;
        return colors[Math.floor(Math.random() * colors.length)];
    }
};

// ===== API FUNCTIONS =====
ViewTrendsSL.api = {
    /**
     * Make authenticated API request
     */
    request: async function(endpoint, options = {}) {
        const url = `${ViewTrendsSL.apiBaseUrl}${endpoint}`;
        const token = localStorage.getItem('access_token');
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `Bearer ${token}` })
            }
        };

        const finalOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        };

        try {
            const response = await fetch(url, finalOptions);
            
            if (response.status === 401) {
                // Token expired, redirect to login
                this.handleAuthError();
                return null;
            }

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            ViewTrendsSL.utils.showNotification('API request failed', 'error');
            throw error;
        }
    },

    /**
     * Handle authentication errors
     */
    handleAuthError: function() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        ViewTrendsSL.utils.showNotification('Session expired. Please log in again.', 'warning');
        // Redirect to login page (this would be handled by Streamlit)
    },

    /**
     * Predict video performance
     */
    predictVideo: async function(videoData) {
        return await this.request('/api/v1/prediction/predict', {
            method: 'POST',
            body: JSON.stringify(videoData)
        });
    },

    /**
     * Get analytics data
     */
    getAnalytics: async function(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return await this.request(`/api/v1/analytics/dashboard?${queryString}`);
    },

    /**
     * Get prediction history
     */
    getPredictionHistory: async function(limit = 10) {
        return await this.request(`/api/v1/prediction/history?limit=${limit}`);
    }
};

// ===== COMPONENT FUNCTIONS =====
ViewTrendsSL.components = {
    /**
     * Initialize chart with default options
     */
    initChart: function(elementId, data, options = {}) {
        const defaultOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true
                    }
                }
            }
        };

        const finalOptions = {
            ...defaultOptions,
            ...options
        };

        // This would integrate with Chart.js if available
        console.log('Chart initialized:', elementId, data, finalOptions);
    },

    /**
     * Create progress bar
     */
    createProgressBar: function(container, value, max = 100) {
        const progressBar = document.createElement('div');
        progressBar.className = 'progress-bar';
        
        const progressFill = document.createElement('div');
        progressFill.className = 'progress-fill';
        progressFill.style.width = `${(value / max) * 100}%`;
        
        progressBar.appendChild(progressFill);
        
        if (typeof container === 'string') {
            container = document.querySelector(container);
        }
        
        if (container) {
            container.appendChild(progressBar);
        }
        
        return progressBar;
    },

    /**
     * Create metric card
     */
    createMetricCard: function(container, title, value, change = null) {
        const card = document.createElement('div');
        card.className = 'metric-card';
        
        const valueElement = document.createElement('div');
        valueElement.className = 'metric-value';
        valueElement.textContent = ViewTrendsSL.utils.formatNumber(value);
        
        const labelElement = document.createElement('div');
        labelElement.className = 'metric-label';
        labelElement.textContent = title;
        
        card.appendChild(valueElement);
        card.appendChild(labelElement);
        
        if (change !== null) {
            const changeElement = document.createElement('div');
            changeElement.className = `metric-change ${change >= 0 ? 'positive' : 'negative'}`;
            changeElement.textContent = `${change >= 0 ? '+' : ''}${change}%`;
            card.appendChild(changeElement);
        }
        
        if (typeof container === 'string') {
            container = document.querySelector(container);
        }
        
        if (container) {
            container.appendChild(card);
        }
        
        return card;
    }
};

// ===== EVENT HANDLERS =====
ViewTrendsSL.events = {
    /**
     * Initialize event listeners
     */
    init: function() {
        // URL validation for prediction forms
        document.addEventListener('input', function(e) {
            if (e.target.classList.contains('youtube-url-input')) {
                ViewTrendsSL.events.validateYouTubeUrl(e.target);
            }
        });

        // Copy buttons
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('copy-button')) {
                const textToCopy = e.target.dataset.copy || e.target.textContent;
                ViewTrendsSL.utils.copyToClipboard(textToCopy);
            }
        });

        // Chart export buttons
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('export-chart')) {
                ViewTrendsSL.events.exportChart(e.target);
            }
        });

        // Auto-save form data
        document.addEventListener('input', ViewTrendsSL.utils.debounce(function(e) {
            if (e.target.classList.contains('auto-save')) {
                ViewTrendsSL.events.autoSaveForm(e.target);
            }
        }, ViewTrendsSL.config.debounceDelay));
    },

    /**
     * Validate YouTube URL input
     */
    validateYouTubeUrl: function(input) {
        const isValid = ViewTrendsSL.utils.isValidYouTubeUrl(input.value);
        
        if (input.value && !isValid) {
            input.classList.add('invalid');
            input.classList.remove('valid');
        } else if (input.value && isValid) {
            input.classList.add('valid');
            input.classList.remove('invalid');
        } else {
            input.classList.remove('valid', 'invalid');
        }
    },

    /**
     * Export chart functionality
     */
    exportChart: function(button) {
        const chartContainer = button.closest('.chart-container');
        const chartTitle = chartContainer.querySelector('.chart-title')?.textContent || 'chart';
        
        // This would integrate with the actual chart library
        ViewTrendsSL.utils.showNotification(`Exporting ${chartTitle}...`, 'info', 2000);
    },

    /**
     * Auto-save form data to localStorage
     */
    autoSaveForm: function(input) {
        const form = input.closest('form');
        if (form) {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            localStorage.setItem(`form_${form.id || 'default'}`, JSON.stringify(data));
        }
    },

    /**
     * Restore form data from localStorage
     */
    restoreFormData: function(formId) {
        const savedData = localStorage.getItem(`form_${formId}`);
        if (savedData) {
            const data = JSON.parse(savedData);
            const form = document.getElementById(formId);
            
            if (form) {
                Object.entries(data).forEach(([name, value]) => {
                    const input = form.querySelector(`[name="${name}"]`);
                    if (input) {
                        input.value = value;
                    }
                });
            }
        }
    }
};

// ===== CACHE MANAGEMENT =====
ViewTrendsSL.cache = {
    /**
     * Set cache item with expiration
     */
    set: function(key, value, ttl = 300000) { // 5 minutes default
        const item = {
            value: value,
            expiry: Date.now() + ttl
        };
        ViewTrendsSL.cache.set(key, item);
    },

    /**
     * Get cache item
     */
    get: function(key) {
        const item = ViewTrendsSL.cache.get(key);
        if (!item) return null;
        
        if (Date.now() > item.expiry) {
            ViewTrendsSL.cache.delete(key);
            return null;
        }
        
        return item.value;
    },

    /**
     * Clear expired cache items
     */
    cleanup: function() {
        const now = Date.now();
        for (const [key, item] of ViewTrendsSL.cache.entries()) {
            if (now > item.expiry) {
                ViewTrendsSL.cache.delete(key);
            }
        }
    }
};

// ===== PERFORMANCE MONITORING =====
ViewTrendsSL.performance = {
    /**
     * Measure function execution time
     */
    measure: function(name, fn) {
        return function(...args) {
            const start = performance.now();
            const result = fn.apply(this, args);
            const end = performance.now();
            console.log(`${name} took ${end - start} milliseconds`);
            return result;
        };
    },

    /**
     * Monitor page load performance
     */
    monitorPageLoad: function() {
        window.addEventListener('load', function() {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('Page load performance:', {
                domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
                loadComplete: perfData.loadEventEnd - perfData.loadEventStart,
                totalTime: perfData.loadEventEnd - perfData.fetchStart
            });
        });
    }
};

// ===== ACCESSIBILITY HELPERS =====
ViewTrendsSL.accessibility = {
    /**
     * Add keyboard navigation support
     */
    addKeyboardNavigation: function() {
        document.addEventListener('keydown', function(e) {
            // Tab navigation for custom components
            if (e.key === 'Tab') {
                const focusableElements = document.querySelectorAll(
                    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
                );
                
                // Handle custom focus management if needed
            }
            
            // Escape key to close modals/dropdowns
            if (e.key === 'Escape') {
                const openModals = document.querySelectorAll('.modal.open, .dropdown.open');
                openModals.forEach(modal => modal.classList.remove('open'));
            }
        });
    },

    /**
     * Announce changes to screen readers
     */
    announce: function(message) {
        const announcer = document.getElementById('sr-announcer') || 
                         this.createAnnouncer();
        announcer.textContent = message;
    },

    /**
     * Create screen reader announcer element
     */
    createAnnouncer: function() {
        const announcer = document.createElement('div');
        announcer.id = 'sr-announcer';
        announcer.setAttribute('aria-live', 'polite');
        announcer.setAttribute('aria-atomic', 'true');
        announcer.style.cssText = `
            position: absolute;
            left: -10000px;
            width: 1px;
            height: 1px;
            overflow: hidden;
        `;
        document.body.appendChild(announcer);
        return announcer;
    }
};

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    console.log(`ViewTrendsSL v${ViewTrendsSL.version} initialized`);
    
    // Initialize event listeners
    ViewTrendsSL.events.init();
    
    // Add keyboard navigation
    ViewTrendsSL.accessibility.addKeyboardNavigation();
    
    // Monitor performance
    ViewTrendsSL.performance.monitorPageLoad();
    
    // Clean up cache periodically
    setInterval(ViewTrendsSL.cache.cleanup, 60000); // Every minute
    
    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
        
        .youtube-url-input.valid {
            border-color: var(--success-color);
        }
        
        .youtube-url-input.invalid {
            border-color: var(--error-color);
        }
        
        .fade-in {
            animation: fadeIn 0.3s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    `;
    document.head.appendChild(style);
});

// ===== EXPORT FOR MODULE SYSTEMS =====
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ViewTrendsSL;
}

// ===== GLOBAL EXPOSURE =====
window.ViewTrendsSL = ViewTrendsSL;
