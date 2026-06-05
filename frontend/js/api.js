// API Configuration
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000/api'
    : '/api';

// Browser-Native Mode: Fallback to local data if server is unreachable
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;

    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                ...options.headers
            }
        });

        if (response.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/pages/login.html';
            return;
        }

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.message || `API Request failed: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.warn(`Server request to ${endpoint} failed. Checking local fallback...`, error);

        // Handle specific endpoints with local data fallback
        const cleanEndpoint = endpoint.split('?')[0];
        const allRestaurants = await getLocalData();

        // 1. All or Popular Restaurants
        if (cleanEndpoint === '/restaurants' || cleanEndpoint === '/restaurants/popular') {
            const seen = new Set();
            const unique = allRestaurants.filter(r => {
                const key = normalizeName(r.name);
                if (seen.has(key)) return false;
                seen.add(key);
                return true;
            });

            return {
                success: true,
                data: {
                    restaurants: unique.slice(0, 50),
                    count: unique.length
                }
            };
        }

        // 2. Recommendations or Nearby
        if (cleanEndpoint.startsWith('/recommendations/nearby') || cleanEndpoint === '/recommendations') {
            const requestData = options.body ? JSON.parse(options.body) : {};
            const recommendations = recommendOffline(allRestaurants, requestData);
            return {
                success: true,
                data: {
                    recommendations: recommendations,
                    restaurants: recommendations,
                    count: recommendations.length
                }
            };
        }

        // 3. Restaurant Reviews
        if (cleanEndpoint.includes('/reviews')) {
            const parts = cleanEndpoint.split('/');
            const restaurantId = parseInt(parts[parts.indexOf('restaurants') + 1]);
            const reviews = await getLocalReviews(restaurantId);
            return {
                success: true,
                data: { reviews, count: reviews.length }
            };
        }

        // 4. Single Restaurant Detail
        if (cleanEndpoint.startsWith('/restaurants/')) {
            const id = parseInt(cleanEndpoint.split('/').pop());
            const restaurant = allRestaurants.find(r => r.id === id) || allRestaurants[0];
            return {
                success: true,
                data: { restaurant }
            };
        }

        // 5. Auth Demo Mode (Offline Fallback)
        if (cleanEndpoint.startsWith('/auth/')) {
            console.log("Demo Mode: Simulating successful authentication");
            const requestData = options.body ? JSON.parse(options.body) : {};
            const mockUser = {
                id: 1,
                name: requestData.name || "Demo User",
                email: requestData.email || "demo@example.com",
                access_token: "demo-token-" + Date.now()
            };
            return {
                success: true,
                message: "Demo login successful (Offline Mode)",
                data: mockUser
            };
        }

        throw error;
    }
}

// Helper to get reviews for a specific restaurant when offline
async function getLocalReviews(restaurantId) {
    const names = [
        "Aravind Kumar", "Srujana Reddy", "Rahul Verma", "Priya Sharma", "Sai Teja",
        "Ananya Rao", "Vikram Rathore", "Sneha Kapoor", "Karthik Raja", "Meghana Bhat"
    ];
    const texts = [
        "Absolutely amazing Biryani! The spices were perfect.",
        "The service was a bit slow, but the food made up for it.",
        "Authentic Hyderabadi flavors. Highly recommended!",
        "Poor quality food. Not worth the price.",
        "Best place for family dinner. The kebabs are juicy.",
        "I've had better. Overrated but still okay.",
        "The best South Indian breakfast in the city.",
        "The Irani chai here is legendary.",
        "Must try the Zafrani Biryani!",
        "The tandoori chicken was perfectly cooked."
    ];

    // Generate 5 mock reviews for the ID
    return [1, 2, 3, 4, 5].map(i => {
        const nameIdx = (restaurantId * i) % names.length;
        return {
            id: i,
            restaurant_id: restaurantId,
            user_id: 100 + i,
            user_name: names[nameIdx], // Added readable name
            text: texts[(restaurantId + i) % texts.length],
            rating: 4 + (i % 2),
            sentiment: { label: 'Positive', polarity: 0.8 },
            authenticity_score: 0.9 + (i * 0.01)
        };
    });
}

// Fetch local JSON data as a fallback when server is offline
async function getLocalData() {
    // Check if data is already loaded via script tag (most reliable for file://)
    if (typeof RESTAURANTS_DATA !== 'undefined' && RESTAURANTS_DATA.length > 0) {
        console.log('Using pre-loaded RESTAURANTS_DATA script');
        return RESTAURANTS_DATA;
    }

    try {
        console.log('Fetching local sample_restaurants.json...');

        let prefix = '';
        const path = window.location.pathname;
        if (path.includes('/frontend/pages/')) {
            prefix = '../../';
        } else if (path.includes('/frontend/')) {
            prefix = '../';
        } else {
            prefix = './';
        }

        const response = await fetch(`${prefix}backend/data/sample_restaurants.json`);
        if (!response.ok) throw new Error('Local file not found');
        const data = await response.json();
        return data.map((r, index) => ({ 
            ...r, 
            id: r.id || (index + 1),
            image_url: getLocalImage(r.image_url, r.cuisine_type)
        }));
    } catch (e) {
        console.error('Local data fetch failed:', e);
        return typeof RESTAURANTS_DATA !== 'undefined' ? RESTAURANTS_DATA : [];
    }
}

// Helper to normalize restaurant names for deduplication
function normalizeName(name) {
    if (!name) return '';
    let norm = name.toLowerCase().trim();

    // Handle curly quotes
    norm = norm.replace(/[‘’]/g, "'").replace(/[“”]/g, '"');

    // Handle specific aliases
    if (norm.includes('sawagth')) norm = norm.replace('sawagth', 'swagath');
    if (norm.includes('mefil')) norm = norm.replace('mefil', 'mehfil');

    // Remove common business suffixes
    const noise = /\b(restaurant|hotel|cafe|bar|grill|multicuisine|bakery|sweets|junction|kitchen|point)\b/g;
    norm = norm.replace(noise, '');

    // Remove all non-alphanumeric for strict brand matching
    return norm.replace(/[^a-z0-9]/g, '') || norm;
}

// Simple client-side recommendation engine for offline mode
function recommendOffline(restaurants, criteria) {
    const {
        latitude, longitude, cuisine_preferences,
        budget_min, budget_max, max_distance_km
    } = criteria || {};

    const userLat = latitude || 17.3850;
    const userLon = longitude || 78.4867;
    const maxDist = max_distance_km || 25;

    const seenNames = new Set();
    const uniqueRestaurants = restaurants.filter(r => {
        const key = normalizeName(r.name);
        if (seenNames.has(key)) return false;
        seenNames.add(key);
        return true;
    });

    const priceMap = { '$': 300, '$$': 700, '$$$': 1500, '$$$$': 3000 };

    const results = uniqueRestaurants.filter(r => {
        // Apply only basic hard filters to avoid empty results
        if (cuisine_preferences && cuisine_preferences.length > 0 && !cuisine_preferences.includes(r.cuisine_type)) return false;
        
        const avgPrice = priceMap[r.price_range] || 700;
        if (budget_max && avgPrice > budget_max) return false;
        if (budget_min && avgPrice < budget_min) return false;
        
        return true;
    }).map(r => {
        let score = 0;
        let explanation = [];

        // Cuisine match (Preference learning simulation)
        const isMatch = cuisine_preferences && cuisine_preferences.length > 0 && cuisine_preferences.includes(r.cuisine_type);
        if (isMatch) {
            score += 0.4;
            explanation.push(`Matches your ${r.cuisine_type} preference`);
        }

        // Distance match (GPS awareness)
        const dist = calculateDistance(userLat, userLon, r.latitude, r.longitude);
        r.distance_km = dist;

        if (dist <= maxDist) {
            const distScore = 0.3 * (1 - dist / maxDist);
            score += distScore;
        }

        // Authenticity boost (AI Authenticity Scoring)
        const auth = r.authenticity_score || 0.8;
        score += auth * 0.2;

        // Popularity boost
        score += (r.popularity_score || 0.5) * 0.1;

        return {
            ...r,
            recommendation_score: score,
            explanation: explanation.join('. ') || '',
            score_breakdown: {
                preference: isMatch ? 1 : 0.5,
                authenticity: auth,
                distance: Math.max(0.1, 1 - dist / maxDist),
                popularity: r.popularity_score || 0.7
            }
        };
    });

    // Sort by score
    results.sort((a, b) => b.recommendation_score - a.recommendation_score);

    // If no good matches, return top popular ones
    return results.slice(0, 50);
}

// Haversine formula for distance
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Radius of the earth in km
    const dLat = deg2rad(lat2 - lat1);
    const dLon = deg2rad(lon2 - lon1);
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
}

function deg2rad(deg) {
    return deg * (Math.PI / 180);
}

// Auth API
const authAPI = {
    login: (email, password) =>
        apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        }),

    signup: (name, email, password, phone) =>
        apiRequest('/auth/signup', {
            method: 'POST',
            body: JSON.stringify({ name, email, password, phone })
        }),

    getProfile: () =>
        apiRequest('/auth/profile', { method: 'GET' }),

    updateProfile: (data) =>
        apiRequest('/auth/profile', {
            method: 'PUT',
            body: JSON.stringify(data)
        })
};

// Restaurant API
const restaurantAPI = {
    getAll: (params = {}) => {
        const queryString = new URLSearchParams(params).toString();
        return apiRequest(`/restaurants?${queryString}`, { method: 'GET' });
    },

    getById: (id) =>
        apiRequest(`/restaurants/${id}`, { method: 'GET' }),

    getReviews: (id, authenticOnly = true) =>
        apiRequest(`/restaurants/${id}/reviews?authentic_only=${authenticOnly}`, { method: 'GET' }),

    getPopular: (limit = 10) =>
        apiRequest(`/restaurants/popular?limit=${limit}`, { method: 'GET' }),

    getCuisines: () =>
        apiRequest('/restaurants/cuisines', { method: 'GET' })
};

// Recommendation API
const recommendationAPI = {
    getRecommendations: (data) =>
        apiRequest('/recommendations', {
            method: 'POST',
            body: JSON.stringify(data)
        }),

    getNearby: (latitude, longitude, maxDistance = 10) =>
        apiRequest('/recommendations/nearby', {
            method: 'POST',
            body: JSON.stringify({ latitude, longitude, max_distance_km: maxDistance })
        })
};

// Review API
const reviewAPI = {
    create: (restaurantId, text, rating) =>
        apiRequest('/reviews', {
            method: 'POST',
            body: JSON.stringify({ restaurant_id: restaurantId, text, rating })
        }),

    getUserReviews: () =>
        apiRequest('/reviews/user', { method: 'GET' }),

    getById: (id) =>
        apiRequest(`/reviews/${id}`, { method: 'GET' }),

    analyze: (id) =>
        apiRequest(`/reviews/${id}/analyze`, { method: 'POST' })
};

// Utility Functions
function showAlert(message, type = 'info') {
    const alertHTML = `
    <div class="alert alert-${type}" style="padding: 1rem; border-radius: 8px; margin-bottom: 1rem; background: ${type === 'danger' ? '#fee2e2' : type === 'warning' ? '#fef3c7' : '#e0f2fe'}; color: ${type === 'danger' ? '#991b1b' : type === 'warning' ? '#92400e' : '#075985'}; border: 1px solid currentColor;">
        ${message}
    </div>
    `;

    const container = document.getElementById('alert-container');
    if (container) {
        container.innerHTML = alertHTML;
        setTimeout(() => {
            container.innerHTML = '';
        }, 6000);
    }
}

function formatDistance(km) {
    if (!km || isNaN(km)) return 'Local';
    if (km < 1) {
        return `${Math.round(km * 1000)}m`;
    }
    return `${km.toFixed(1)}km`;
}

function formatPrice(priceRange) {
    const mapping = {
        '$': '₹200',
        '$$': '₹500',
        '$$$': '₹1200',
        '$$$$': '₹2500'
    };
    if (!priceRange) return '₹500';
    // Handle both $ and ₹ input symbols
    const cleanRange = priceRange.replace(/₹/g, '$');
    return mapping[cleanRange] || mapping['$$'];
}

// Local Image Fallback (Offline Support)
function getLocalImage(url, cuisine = '') {
    if (!url) return '../assets/images/generic_food.png';
    
    // If it's already a local path, return it (but ensure correct prefix)
    if (url.startsWith('../') || url.startsWith('./') || url.startsWith('assets/')) {
        return url;
    }

    // Mapping for major restaurants
    const nameMap = {
        'paradise': '../assets/images/paradise_biryani_1772185606150.png',
        'bawarchi': '../assets/images/bawarchi_biryani_1772185625232.png',
        'niloufer': '../assets/images/cafe_niloufer_tea_1772185658915.png',
        'chutney': '../assets/images/chutneys_dosa_thali_1772185674047.png',
        'shah ghouse': '../assets/images/shah_ghouse_haleem_1772185695470.png'
    };

    // Check if the URL or cuisine suggests a specific local image
    const lowCuisine = cuisine.toLowerCase();
    
    // Existing local high-quality assets
    if (lowCuisine.includes('biryani')) return '../assets/images/paradise_biryani_1772185606150.png';
    if (lowCuisine.includes('south indian') || lowCuisine.includes('andhra')) return '../assets/images/chutneys_dosa_thali_1772185674047.png';
    if (lowCuisine.includes('tea') || lowCuisine.includes('cafe') || lowCuisine.includes('irani')) return '../assets/images/cafe_niloufer_tea_1772185658915.png';
    if (lowCuisine.includes('mughlai')) return '../assets/images/shah_ghouse_haleem_1772185695470.png';

    // Premium Unsplash fallbacks for other categories to avoid "all look the same" issue
    if (lowCuisine.includes('north indian')) return 'https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=800';
    if (lowCuisine.includes('chinese')) return 'https://images.unsplash.com/photo-1552611052-33e04de081de?w=800';
    if (lowCuisine.includes('japanese')) return 'https://images.unsplash.com/photo-1580822184713-fc5400e7fe10?w=800';
    if (lowCuisine.includes('arabic')) return 'https://images.unsplash.com/photo-1544124499-58912cbddaad?w=800';
    if (lowCuisine.includes('seafood')) return 'https://images.unsplash.com/photo-1615141982883-c7ad0e69fd62?w=800';

    // Default to the generated generic high-quality food image
    return '../assets/images/generic_food.png';
}

// AI Location Awareness
async function getUserLocation() {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject(new Error("Geolocation not supported"));
            return;
        }
        navigator.geolocation.getCurrentPosition(
            (pos) => resolve({ lat: pos.coords.latitude, lon: pos.coords.longitude }),
            (err) => reject(err),
            { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
        );
    });
}

// Regional Popularity Analysis (AI Simulated)
function getRegionalTrends(city = "Hyderabad") {
    const trends = {
        "Hyderabad": ["Biryani", "Haleem", "Irani Chai"],
        "Delhi": ["Chaat", "Butter Chicken", "Chole Bhature"],
        "Mumbai": ["Vada Pav", "Pav Bhaji", "Sea Food"],
        "Bangalore": ["Dosa", "Craft Beer", "Filter Coffee"]
    };
    return trends[city] || trends["Hyderabad"];
}

// Check backend health on startup
async function checkBackendHealth() {
    try {
        const health = await apiRequest('/health');
        if (health && health.status === 'degraded') {
            let msg = 'Some AI features (Authentication/Reviews) might be limited.';
            showAlert(msg, 'warning');
        }
    } catch (error) {
        console.warn('Backend server offline. Running in Browser-Native mode.');
    }
}

// Simple star rating generator
/**
 * Generates HTML for star rating display
 * @param {number} rating - The rating value (0-5)
 * @returns {string} HTML string for the stars
 */
function getStars(rating) {
    const rawR = parseFloat(rating) || 0;
    // Round to nearest 0.5
    const r = Math.round(rawR * 2) / 2;
    const fullStars = Math.floor(r);
    const hasHalfStar = (r % 1) >= 0.5;
    const emptyStars = Math.max(0, 5 - fullStars - (hasHalfStar ? 1 : 0));

    let starsHtml = '<div class="star-rating" style="display: inline-flex; align-items: center; gap: 2px;" aria-label="Rating: ' + r + ' stars">';

    // SVG for full star
    const fullStarSvg = `<svg class="star-icon full" viewBox="0 0 24 24" width="16" height="16" fill="#FFD700" style="filter: drop-shadow(0 0 1px rgba(0,0,0,0.2));">
        <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
    </svg>`;

    // SVG for half star (using clipPath for better rendering)
    const halfStarSvg = `<svg class="star-icon half" viewBox="0 0 24 24" width="16" height="16" style="filter: drop-shadow(0 0 1px rgba(0,0,0,0.2));">
        <defs>
            <linearGradient id="halfGrad-${Math.random().toString(36).substr(2, 9)}">
                <stop offset="50%" stop-color="#FFD700"/>
                <stop offset="50%" stop-color="#D1D5DB"/>
            </linearGradient>
        </defs>
        <path fill="url(#${starsHtml.match(/halfGrad-[a-z0-9]+/)?.[0] || 'halfGrad'})" d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
    </svg>`;

    // Correcting the half star SVG to avoid circular dependency in regex or missing IDs
    const uniqueId = 'halfGrad-' + Math.random().toString(36).substr(2, 5);
    const actualHalfStarSvg = `<svg class="star-icon half" viewBox="0 0 24 24" width="16" height="16" style="filter: drop-shadow(0 0 1px rgba(0,0,0,0.2));">
        <defs>
            <linearGradient id="${uniqueId}">
                <stop offset="50%" stop-color="#FFD700"/>
                <stop offset="50%" stop-color="#D1D5DB"/>
            </linearGradient>
        </defs>
        <path fill="url(#${uniqueId})" d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
    </svg>`;

    // SVG for empty star
    const emptyStarSvg = `<svg class="star-icon empty" viewBox="0 0 24 24" width="16" height="16" fill="#D1D5DB" style="filter: drop-shadow(0 0 1px rgba(0,0,0,0.1));">
        <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
    </svg>`;

    for (let i = 0; i < fullStars; i++) starsHtml += fullStarSvg;
    if (hasHalfStar) starsHtml += actualHalfStarSvg;
    for (let i = 0; i < emptyStars; i++) starsHtml += emptyStarSvg;

    starsHtml += `<span class="rating-number" style="margin-left: 6px; font-weight: 500; font-size: 0.9rem; color: var(--text-muted);">(${r})</span>`;
    starsHtml += '</div>';

    return starsHtml;
}

// Global UI Initialization
if (typeof window !== 'undefined') {
    window.addEventListener('load', () => {
        // Mobile Menu Toggle
        const menuToggle = document.getElementById('menu-toggle');
        const navbarMenu = document.getElementById('navbar-menu');

        if (menuToggle && navbarMenu) {
            menuToggle.addEventListener('click', () => {
                navbarMenu.classList.toggle('active');
                menuToggle.classList.toggle('active');
            });

            // Close menu when clicking outside
            document.addEventListener('click', (e) => {
                if (!menuToggle.contains(e.target) && !navbarMenu.contains(e.target)) {
                    navbarMenu.classList.remove('active');
                    menuToggle.classList.remove('active');
                }
            });

            // Close menu on link click
            navbarMenu.querySelectorAll('.navbar-link').forEach(link => {
                link.addEventListener('click', () => {
                    navbarMenu.classList.remove('active');
                    menuToggle.classList.remove('active');
                });
            });
        }

        checkBackendHealth();
    });
}
