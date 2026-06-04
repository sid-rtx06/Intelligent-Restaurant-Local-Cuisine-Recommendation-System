// Authentication utilities

function isAuthenticated() {
    return localStorage.getItem('token') !== null;
}

function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    // Determine path to login
    const isInsidePages = window.location.pathname.includes('/pages/');
    window.location.href = isInsidePages ? 'login.html' : 'pages/login.html';
}

function requireAuth() {
    if (!isAuthenticated()) {
        const isInsidePages = window.location.pathname.includes('/pages/');
        window.location.href = isInsidePages ? 'login.html' : 'pages/login.html';
    }
}

// Update navbar based on auth status
function updateNavbar() {
    const user = getCurrentUser();
    const navMenu = document.getElementById('navbar-menu');

    if (!navMenu) return;

    const isInsidePages = window.location.pathname.includes('/pages/');
    const basePath = isInsidePages ? '' : 'pages/';
    const indexPrefix = isInsidePages ? '../' : '';

    const adminPath = isInsidePages ? '../admin/login.html' : 'admin/login.html';

    if (user) {
        navMenu.innerHTML = `
            <li><a href="${basePath}home.html" class="navbar-link">Home</a></li>
            <li><a href="${basePath}recommendations.html" class="navbar-link">Recommendations</a></li>
            <li><a href="${adminPath}" class="navbar-link text-red-500 font-bold" style="color: var(--accent);">Admin Panel</a></li>
            <li><a href="#" onclick="logout()" class="btn btn-outline" style="margin-left: 1rem;">Logout</a></li>
            <li>
                <button class="theme-toggle-btn" id="theme-toggle" onclick="toggleTheme()">
                    <span class="theme-icon">☀️</span>
                </button>
            </li>
        `;
    } else {
        navMenu.innerHTML = `
            <li><a href="${indexPrefix}index.html" class="navbar-link">Home</a></li>
            <li><a href="${basePath}login.html" class="navbar-link">Login</a></li>
            <li><a href="${adminPath}" class="navbar-link text-red-500 font-bold" style="color: var(--accent);">Admin Panel</a></li>
            <li><a href="${basePath}signup.html" class="btn btn-primary btn-sm">Sign Up</a></li>
            <li>
                <button class="theme-toggle-btn" id="theme-toggle" onclick="toggleTheme()">
                    <span class="theme-icon">☀️</span>
                </button>
            </li>
        `;
    }

    // Set active state
    const currentPath = window.location.pathname;
    const links = navMenu.querySelectorAll('.navbar-link');
    links.forEach(link => {
        if (currentPath.endsWith(link.getAttribute('href'))) {
            link.classList.add('active');
        }
    });
}

// Call on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateNavbar);
} else {
    updateNavbar();
}
