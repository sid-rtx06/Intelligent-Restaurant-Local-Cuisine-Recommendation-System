// User preferences management

const CUISINES = [
    { name: 'South Indian', image: '../assets/images/chutneys_dosa_thali_1772185674047.png' },
    { name: 'Mughlai', image: '../assets/images/shah_ghouse_haleem_1772185695470.png' },
    { name: 'North Indian', image: 'https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=800' },
    { name: 'Chinese', image: 'https://images.unsplash.com/photo-1552611052-33e04de081de?w=800' },
    { name: 'Japanese', image: 'https://images.unsplash.com/photo-1580822184713-fc5400e7fe10?w=800' },
    { name: 'Continental', image: '../assets/images/cafe_niloufer_tea_1772185658915.png' },
    { name: 'Arabic', image: 'https://images.unsplash.com/photo-1544124499-58912cbddaad?w=800' },
    { name: 'Seafood', image: 'https://images.unsplash.com/photo-1615141982883-c7ad0e69fd62?w=800' }
];

const MOODS = [
    { name: 'Spicy', emoji: '🌶️' },
    { name: 'Royal', emoji: '👑' },
    { name: 'Authentic', emoji: '🍯' },
    { name: 'Healthy', emoji: '🥗' },
    { name: 'Street-style', emoji: '🍢' },
    { name: 'Premium', emoji: '💎' },
    { name: 'Comfort', emoji: '🥘' },
    { name: 'Quick Bite', emoji: '🍔' },
    { name: 'Fine Dining', emoji: '🍷' },
    { name: 'Casual', emoji: '🍽️' },
    { name: 'Traditional', emoji: '🕌' }
];

function savePreferences(preferences) {
    localStorage.setItem('preferences', JSON.stringify(preferences));
}

function getPreferences() {
    const prefsStr = localStorage.getItem('preferences');
    return prefsStr ? JSON.parse(prefsStr) : {
        cuisine_preferences: [],
        mood_preferences: [],
        budget_min: 0,
        budget_max: 5000,
        allow_gps: false,
        preferred_distance_km: 10
    };
}

function updatePreferences(updates) {
    const current = getPreferences();
    const updated = { ...current, ...updates };
    savePreferences(updated);
    return updated;
}
